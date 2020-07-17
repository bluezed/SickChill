# coding=utf-8
# Author: Idan Gutman
# Modified by jkaberg, https://github.com/jkaberg for SceneAccess
# Modified by 7ca for HDSpace
# URL: https://sickchill.github.io
#
# This file is part of SickChill.
#
# SickChill is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickChill is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickChill. If not, see <http://www.gnu.org/licenses/>.
# Stdlib Imports
import re

# Third Party Imports
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from requests.utils import dict_from_cookiejar

# First Party Imports
from sickbeard import logger, tvcache
from sickchill.helper.common import convert_size, try_int
from sickchill.providers.media.torrent import TorrentProvider


class HDSpaceProvider(TorrentProvider):

    def __init__(self):

        TorrentProvider.__init__(self, "HDSpace")
        self.cache = tvcache.TVCache(self, min_time=10)  # only poll HDSpace every 10 minutes max

        self.urls = {'base_url': 'https://hd-space.org/',
                     'login': 'https://hd-space.org/index.php?page=login',
                     'search': 'https://hd-space.org/index.php?page=torrents&search=%s&active=1&options=0',
                     'rss': 'https://hd-space.org/rss_torrents.php?feed=dl'
                     }

        self.categories = [15, 21, 22, 24, 25, 40]  # HDTV/DOC 1080/720, bluray, remux
        self.urls['search'] += '&category='
        for cat in self.categories:
            self.urls['search'] += str(cat) + '%%3B'
            self.urls['rss'] += '&cat[]=' + str(cat)
        self.urls['search'] = self.urls['search'][:-4]  # remove extra %%3B

        self.url = self.urls['base_url']

        self.supported_options = ('username', 'password', 'minseed', 'minleech')

    def _check_auth(self):

        if not self.config('username') or not self.config('password'):
            logger.warning("Invalid username or password. Check your settings")

        return True

    def login(self):
        if any(dict_from_cookiejar(self.session.cookies).values()):
            return True

        if 'pass' in dict_from_cookiejar(self.session.cookies):
            return True

        login_params = {'uid': self.config('username'),
                        'pwd': self.config('password')}

        response = self.get_url(self.urls['login'], post_data=login_params, returns='text')
        if not response:
            logger.warning("Unable to connect to provider")
            return False

        if re.search('Password Incorrect', response):
            logger.warning("Invalid username or password. Check your settings")
            return False

        return True

    def search(self, search_strings, age=0, ep_obj=None):
        results = []
        if not self.login():
            return results

        for mode in search_strings:
            items = []
            logger.debug("Search Mode: {0}".format(mode))
            for search_string in search_strings[mode]:
                if mode != 'RSS':
                    search_url = self.urls['search'] % (quote_plus(search_string.replace('.', ' ')),)
                else:
                    search_url = self.urls['search'] % ''

                if mode != 'RSS':
                    logger.debug("Search string: {0}".format(search_string))

                data = self.get_url(search_url, returns='text')
                if not data or 'please try later' in data:
                    logger.debug("No data returned from provider")
                    continue

                # Search result page contains some invalid html that prevents html parser from returning all data.
                # We cut everything before the table that contains the data we are interested in thus eliminating
                # the invalid html portions
                try:
                    data = data.split('<div id="information"></div>')[1]
                    index = data.index('<table')
                except ValueError:
                    logger.exception("Could not find main torrent table")
                    continue
                except IndexError:
                    logger.debug("Could not parse data from provider")
                    continue

                html = BeautifulSoup(data[index:], 'html5lib')
                if not html:
                    logger.debug("No html data parsed from provider")
                    continue

                torrents = html('tr')
                if not torrents:
                    continue

                # Skip column headers
                for result in torrents[1:]:
                    if len(result.contents) < 10:
                        # skip extraneous rows at the end
                        continue

                    try:
                        dl_href = result.find('a', attrs={'href': re.compile(r'download.php.*')})['href']
                        title = re.search('f=(.*).torrent', dl_href).group(1).replace('+', '.')
                        download_url = self.urls['base_url'] + dl_href
                        seeders = int(result.find('span', class_='seedy').find('a').text)
                        leechers = int(result.find('span', class_='leechy').find('a').text)
                        torrent_size = re.match(r'.*?([0-9]+,?\.?[0-9]* [KkMmGg]+[Bb]+).*', str(result), re.DOTALL).group(1)
                        size = convert_size(torrent_size) or -1

                        if not all([title, download_url]):
                            continue

                        # Filter unseeded torrent
                        if seeders < self.config('minseed') or leechers < self.config('minleech'):
                            if mode != 'RSS':
                                logger.debug("Discarding torrent because it doesn't meet the minimum seeders or leechers: {0} (S:{1} L:{2})".format
                                           (title, seeders, leechers))
                            continue

                        item = {'title': title, 'link': download_url, 'size': size, 'seeders': seeders, 'leechers': leechers, 'hash': ''}
                        if mode != 'RSS':
                            logger.debug("Found result: {0} with {1} seeders and {2} leechers".format(title, seeders, leechers))

                        items.append(item)

                    except (AttributeError, TypeError, KeyError, ValueError):
                        continue

            # For each search mode sort all the items by seeders if available
            items.sort(key=lambda d: try_int(d.get('seeders', 0)), reverse=True)
            results += items

        return results


