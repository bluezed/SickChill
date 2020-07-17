# coding=utf-8
# Author: Gonçalo M. (aka duramato/supergonkas) <supergonkas@gmail.com>
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
# Third Party Imports
from requests.compat import urljoin

# First Party Imports
from sickbeard import logger, tvcache
from sickchill.helper.common import convert_size, try_int
from sickchill.providers.media.torrent import TorrentProvider


class HD4FreeProvider(TorrentProvider):

    def __init__(self):

        TorrentProvider.__init__(self, "HD4Free")

        self.url = 'https://hd4free.xyz'
        self.urls = {'search': urljoin(self.url, '/searchapi.php')}

        self.cache = tvcache.TVCache(self, min_time=10)  # Only poll HD4Free every 10 minutes max

        self.supported_options = ('username', 'api_key', 'minseed', 'minleech', 'freeleech')

    def _check_auth(self):
        if self.config('username') and self.config('api_key'):
            return True

        logger.warning('Your authentication credentials for {0} are missing, check your config.'.format(self.name))
        return False

    def search(self, search_strings, age=0, ep_obj=None):
        results = []
        if not self._check_auth:
            return results

        search_params = {
            'tv': 'true',
            'username': self.config('username'),
            'apikey': self.config('api_key')
        }

        for mode in search_strings:
            items = []
            logger.debug("Search Mode: {0}".format(mode))
            for search_string in search_strings[mode]:
                if self.config('freeleech'):
                    search_params['fl'] = 'true'
                else:
                    search_params.pop('fl', '')

                if mode != 'RSS':
                    logger.debug("Search string: " + search_string.strip())
                    search_params['search'] = search_string
                else:
                    search_params.pop('search', '')

                try:
                    jdata = self.get_url(self.urls['search'], params=search_params, returns='json')
                except ValueError:
                    logger.debug("No data returned from provider")
                    continue

                if not jdata:
                    logger.debug("No data returned from provider")
                    continue

                error = jdata.get('error')
                if error:
                    logger.debug("{}".format(error))
                    return results

                try:
                    if jdata['0']['total_results'] == 0:
                        logger.debug("Provider has no results for this search")
                        continue
                except Exception:
                    continue

                for i in jdata:
                    try:
                        title = jdata[i]["release_name"]
                        download_url = jdata[i]["download_url"]
                        if not all([title, download_url]):
                            continue

                        seeders = jdata[i]["seeders"]
                        leechers = jdata[i]["leechers"]
                        if seeders < self.config('minseed') or leechers < self.config('minleech'):
                            if mode != 'RSS':
                                logger.debug("Discarding torrent because it doesn't meet the minimum seeders or leechers: {0} (S:{1} L:{2})".format
                                           (title, seeders, leechers))
                            continue

                        torrent_size = str(jdata[i]["size"]) + ' MB'
                        size = convert_size(torrent_size) or -1
                        item = {'title': title, 'link': download_url, 'size': size, 'seeders': seeders, 'leechers': leechers, 'hash': ''}

                        if mode != 'RSS':
                            logger.debug("Found result: {0} with {1} seeders and {2} leechers".format(title, seeders, leechers))

                        items.append(item)
                    except Exception:
                        continue

            # For each search mode sort all the items by seeders if available
            items.sort(key=lambda d: try_int(d.get('seeders', 0)), reverse=True)

            results += items

        return results


