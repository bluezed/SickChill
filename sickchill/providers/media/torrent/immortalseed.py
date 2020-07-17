# coding=utf-8
# Author: Bart Sommer <bart.sommer88@gmail.com>
#
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
from requests.compat import urljoin
from requests.utils import dict_from_cookiejar

# First Party Imports
from sickbeard import logger, tvcache
from sickbeard.bs4_parser import BS4Parser
from sickchill.helper.common import convert_size, try_int
from sickchill.helper.exceptions import AuthException
from sickchill.providers.media.torrent import TorrentProvider


class ImmortalseedProvider(TorrentProvider):

    def __init__(self):

        # Provider Init
        TorrentProvider.__init__(self, "Immortalseed")

        # URLs
        self.url = 'https://immortalseed.me/'
        self.urls = {
            'login': urljoin(self.url, 'takelogin.php'),
            'search': urljoin(self.url, 'browse.php'),
            'rss': urljoin(self.url, 'rss.php'),
        }

        # Proper Strings
        self.proper_strings = ['PROPER', 'REPACK']

        # Cache
        self.cache = ImmortalseedCache(self, min_time=20)

        self.supported_options = ('username', 'password', 'passkey', 'minseed', 'minleech', 'freeleech')

    def _check_auth(self):

        if not self.config('username') or not self.config('password'):
            raise AuthException("Your authentication credentials for " + self.name + " are missing, check your config.")

        return True

    def _check_auth_from_data(self, data):
        if not self.config('passkey'):
            logger.warning('Invalid passkey. Check your settings')

        return True

    def login(self):
        if any(dict_from_cookiejar(self.session.cookies).values()):
            return True

        login_params = {
            'username': self.config('username'),
            'password': self.config('password'),
        }

        response = self.get_url(self.urls['login'], post_data=login_params, returns='text')
        if not response:
            logger.warning("Unable to connect to provider")
            return False

        if re.search('Username or password incorrect!', response):
            logger.warning("Invalid username or password. Check your settings")
            return False

        return True

    def search(self, search_strings, age=0, ep_obj=None):
        results = []
        if not self.login():
            return results

        # Search Params
        search_params = {
            'do': 'search',
            'include_dead_torrents': 'no',
            'search_type': 't_name',
            'category': 0,
            'keywords': ''
        }

        # Units
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

        def process_column_header(td):
            td_title = ''
            if td.img:
                td_title = td.img.get('title', td.get_text(strip=True))
            if not td_title:
                td_title = td.get_text(strip=True)
            return td_title

        for mode in search_strings:
            items = []
            logger.debug("Search Mode: {0}".format(mode))

            for search_string in search_strings[mode]:
                if mode != 'RSS':
                    logger.debug("Search string: {0}".format(search_string))
                    search_params['keywords'] = search_string

                data = self.get_url(self.urls['search'], params=search_params, returns='text')
                if not data:
                    logger.debug("No data returned from provider")
                    continue

                with BS4Parser(data, 'html5lib') as html:
                    torrent_table = html.find('table', id='sortabletable')
                    torrent_rows = torrent_table('tr') if torrent_table else []

                    # Continue only if at least one Release is found
                    if len(torrent_rows) < 2:
                        logger.debug("Data returned from provider does not contain any torrents")
                        continue

                    labels = [process_column_header(label) for label in torrent_rows[0]('td')]

                    # Skip column headers
                    for result in torrent_rows[1:]:
                        try:
                            title = result.find('div', class_='tooltip-target').get_text(strip=True)
                            # skip if torrent has been nuked due to poor quality
                            if title.startswith('Nuked.'):
                                continue
                            download_url = result.find(
                                'img', title='Click to Download this Torrent in SSL!').parent['href']
                            if not all([title, download_url]):
                                continue

                            cells = result('td')
                            seeders = try_int(cells[labels.index('Seeders')].get_text(strip=True))
                            leechers = try_int(cells[labels.index('Leechers')].get_text(strip=True))

                            # Filter unseeded torrent
                            if seeders < self.config('minseed') or leechers < self.config('minleech'):
                                if mode != 'RSS':
                                    logger.debug("Discarding torrent because it doesn't meet the"
                                               " minimum seeders or leechers: {0} (S:{1} L:{2})".format
                                               (title, seeders, leechers))
                                continue

                            torrent_size = cells[labels.index('Size')].get_text(strip=True)
                            size = convert_size(torrent_size, units=units) or -1

                            item = {'title': title, 'link': download_url, 'size': size, 'seeders': seeders,
                                    'leechers': leechers, 'hash': ''}
                            if mode != 'RSS':
                                logger.debug("Found result: {0} with {1} seeders and {2} leechers".format
                                           (title, seeders, leechers))

                            items.append(item)
                        except Exception:
                            continue

            # For each search mode sort all the items by seeders if available
            items.sort(key=lambda d: try_int(d.get('seeders', 0)), reverse=True)
            results += items

        return results


class ImmortalseedCache(tvcache.TVCache):
    def get_rss_data(self):
        params = {
            'secret_key': self.provider.config('passkey'),
            'feedtype': 'downloadssl',
            'timezone': '-5',
            'categories': '44,32,7,47,8,48,9',
            'showrows': '50',
        }

        return self.get_rss_feed(self.provider.urls['rss'], params=params)

    def _check_auth(self, data):
        return self.provider._check_auth_from_data(data)


