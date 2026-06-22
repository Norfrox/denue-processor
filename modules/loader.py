import pandas as pd
from typing import Iterator
from .config import DenueConfig
import logging

logger = logging.getLogger(__name__)

class DenueDataLoader:

    def __init__(self, config: DenueConfig):
        self.config = config

    def load(self) -> Iterator[pd.DataFrame]:
        logger.info(f"Loading File: {self.config.input_file}")
        if self.config.chunk_size:
            chunks = pd.read_csv(
                self.config.input_file,
                encoding=self.config.encoding,
                chunksize=self.config.chunk_size,
                low_memory=False
            )
            for chunk in chunks:
                yield chunk
        else:
            df = pd.read_csv(
                self.config.input_file,
                encoding=self.config.encoding,
                low_memory=False
            )
            yield df
