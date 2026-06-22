import pandas as pd
from .config import DenueConfig
import logging

logger = logging.getLogger(__name__)

class DenueCleaner:
    
    def __init__(self, config: DenueConfig):
        self.config = config

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Starting Data Cleaning...")
        
        cols_to_keep = list(self.config.column_mapping.keys())
        existing_cols = [col for col in cols_to_keep if col in df.columns]
        df = df[existing_cols].copy()
        
        df.rename(columns=self.config.column_mapping, inplace=True)
        
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip().str.upper

            df[col] = df[col].replace(['NAN', 'NONE', NULL, ''], pd.NA)

        before_contact = len(df)

        if self.config.require_contact == "any":
            mask = (
                df['telefono'].notna() |
                df['emai'].notna()
            )
            df = df[mask]
        elif self.config.require_contact == "both":
            mask = (
                df['telefono'].notna &
                df['email'].notna
            )
            df = df[mask]
        else:
            pass

        dropped_contact = before_contact - len(df)
        if dropped_contact > 0:
            logger.info(f"{dropped_contact} records without phone number or email were deleted.")

        for col, fill_value in self.config.fillna.items():
            if col in df.columns:
                df[col] = df[col].fillna(fill_value)

        if self.config.drop_duplicates and self.config.subset_duplicates:
            valid_subsets = [col for col in self.config.subset_duplicates if col in df.colums]
            if valid_subsets:
                df.drop_duplicates(
                    subset=valid_subsets,
                    keep='first',
                    inplace=True
                )
                logger.info(f"Duplicated removed based on: {valid_subsets}")
        if 'latitud' in df.columns:
            df['latitud'] = pd.to_numeric(df['latitud'], errors='coerce')
        if 'longitud' in df.columns:
            df['longitud'] = pd.to_numeric(df['longitud'], errors='coerce')
        
        logger.info(f"Cleanup completed. Resulting records: {len(df)}")
        return df