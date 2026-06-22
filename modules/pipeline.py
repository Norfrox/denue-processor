from .loader import DenueDataLoader
from .cleaner import DenueCleaner
from .analyzer import ClientFinder
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

    def run(self, output_path: str = None) -> pd.DataFrame:
        all_clients = []

        for i, chunk in enumerate(self.loader.load()):
            logger.info(f"Processing chunk {i+1}...")
            chunk_clean = self.cleaner.clean(chunk)
            if chunk_clean.empty:
                continue
            clients = self.finder.find_potential_clients(chunk_clean)
            if not clients.empty:
                all_clients.append(clients)

        if all_clients:
            final_df = pd.concat(all_clients, ignore_index=True)
            final_df.drop_duplicates(subset=['id', 'razon_social'], inplace=True)
            logger.info(f"Total Clients Found: {len(final_df)}")
            if output_path:
                final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
                logger.info(f"Results saved in: {output_path}")
            return final_df
        else:
            logger.info(f"No customers were found with the current filters.")
            return pd.DataFrame()