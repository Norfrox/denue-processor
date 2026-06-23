# Copyright 2026 Norfrox
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import logging
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from typing import Dict, Any
from urllib.parse import urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)

class WebsiteVerifier:
    
    def __init__(self, config: Dict[str, Any]):
        self.enabled = config.get('enabled', False)
        self.timeout = config.get('timeout', 5)
        self.max_retries = config.get('max_retries', 1)
        self.user_agent = config.get('user_agent', 'Mozilla/5.0 (compatible; NorfroxBot/1.0; +https://norfrox.com/scout)')
        self.verify_ssl = config.get('verify_ssl', False)
        self.allowed_status_codes = config.get('allowed_status_codes', [200, 301, 302])
        self.session = None

    def _get_session(self):
        if self.session is None:
            self.session = requests.Session()
            self.session.headers.update({'User-Agent': self.user_agent})
        return self.session

    def _normalize_url(self, url: str) -> str:
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        return url

    def _check_url(self, url: str) -> Dict[str, Any]:
        result = {
            'url': url,
            'activo': False,
            'status_code': None,
            'error': None
        }

        if not url or pd.isna(url) or str(url).strip() == '':
            result['error'] = 'URL vacia'
            return result

        url = str(url).strip()

        url_normalized = self._normalize_url(url)
        parsed = urlparse(url_normalized)

        if not parsed.netloc:
            result['error'] = 'URL inválida'
            return result

        session = self._get_session()
        for attempt in range(self.max_retries + 1):
            try:
                response = session.get(
                    url_normalized,
                    timeout=self.timeout,
                    verify=self.verify_ssl,
                    allow_redirects=True,
                    stream=True
                )

                response.close()

                if response.status_code in self.allowed_status_codes:
                    result['activo'] = True
                result['status_code'] = response.status_code
                break

            except requests.exceptions.Timeout:
                result['error'] = f'Timeout ({self.timeout}s)'
            except requests.exceptions.ConnectionError:
                result['error'] = f'Error de conexión'
            except requests.exceptions.SSLError:
                result['error'] = f'Error SSL'
            except requests.exceptions.TooManyRedirects:
                result['error'] = f'Demasiadas redirecciones'
            except Exception as e:
                result['error'] = str(e)

            if attempt < self.max_retries:
                import time
                time.sleep(0.5)

        return result

    def verify_dataframe(self, df: pd.DataFrame, url_column: str = 'sitio_web') -> pd.DataFrame:
        if not self.enabled:
            logger.info("Web site verification disabled.")
            df['sitio_web_activo'] = False
            df['sitio_web_status'] = None
            df['sitio_web_error'] = None
            return df

        if url_column not in df.columns:
            logger.warning(f"Column '{url_column}' not found. Skiping verification.")
            df['sitio_web_activo'] = False
            df['sitio_web_status'] = None
            df['sitio_web_error'] = None            
            return df

        df['sitio_web_activo'] = False
        df['sitio_web_status'] = None
        df['sitio_web_error'] = None

        mask_valid = df[url_column].notna() & (df[url_column] != '') & (df[url_column] != 'SIN_WEB')
        urls = df.loc[mask_valid, url_column].to_list()

        if not urls:
            logger.info('There are not URLs to verify.')
            return df

        logger.info(f"Verifying {len(urls)} web sites...")
        results = {}

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(self._check_url, url): url for url in urls}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    results[url] = result
                except Exception as e:
                    logger.error(f"Error inesperado verificando {url}: {e}")
                    results[url] = {'activo': False, 'status_code': None, 'error': str(e)}

        for idx, row in df.iterrows():
            url = row[url_column]
            if pd.isna(url) or url == '' or url == 'SIN_WEB':
                continue
            result = results.get(url)
            if result:
                df.at[idx, 'sitio_web_activo'] = result['activo']
                df.at[idx, 'sitio_web_status'] = result['status_code']
                df.at[idx, 'sitio_web_error'] = result['error']

        activos = df['sitio_web_activo'].sum()
        total = mask_valid.sum()

        logger.info(f"Verification completed. Active sites: {activos}/{total}")

        return df