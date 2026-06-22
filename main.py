import logging
from modules.config import DenueConfig
from modules.pipeline import DenuePipeline

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    config = DenueConfig.from_yaml("config.yaml")

    pipeline = DenuePipeline(config)
    result = pipeline.run(output_path="potential_clients.csv")

    if not result.empty:
        print("\n=== SAMPLE RESULTS ===")
        print(result[['razon_social', 'nombre_comercial', 'codigo_actividad',
            'entidad', 'municipio', 'telefono', 'email']].head(10))
        print(f"Total records exported: {len(result)}")
    else:
        print("No results were found. Adjust the filters in config.yaml")

if __name__ == "__main__"        :
    main()