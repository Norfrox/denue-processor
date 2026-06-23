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

from .loader import DenueDataLoader
from .cleaner import DenueCleaner
from .analyzer import ClientFinder
from .verifier import WebsiteVerifier
from .config import DenueConfig
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DenuePipeline:

    def __init__(self, config: DenueConfig):
        self.config = config
        self.loader = DenueDataLoader(config)
        self.cleaner = DenueCleaner(config)
        self.finder = ClientFinder(config)
        self.verifier = WebsiteVerifier(config.website_verification)

    def run(self, output_path: str = None) -> pd.DataFrame:
        all_clients = []

        for i, chunk in enumerate(self.loader.load()):
            logger.info(f"Processing chunk {i+1}...")
            chunk_clean = self.cleaner.clean(chunk)
            if chunk_clean.empty:
                continue
            
            chunk_verified = self.verifier.verify_dataframe(chunk_clean)

            clients = self.finder.find_potential_clients(chunk_verified)
            if not clients.empty:
                all_clients.append(clients)

        if all_clients:

            final_df = pd.concat(all_clients, ignore_index=True)

            if 'id' in final_df.columns:
                final_df.drop_duplicates(subset=['id'], inplace=True)

            logger.info(f"Total Clients Found: {len(final_df)}")

            if output_path:
                final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
                logger.info(f"Results saved in: {output_path}")
            return final_df
        else:
            logger.info(f"No customers were found with the current filters.")
            return pd.DataFrame()