import os
import sys
import logging
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('Deploy Model').getOrCreate()


sys.path.append(os.getcwd().rsplit("/src")[0])
from src.deployment.realtime_deployment import get_ready_for_realtime_inference, real_time_deploy
from src.config.configuration import datasets_path, catalog_name, bronze_schema_name, silver_schema_name, gold_schema_name, chain_model_name, serving_endpoint_name

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S"  # Date format
)

# Suppress Py4J logs
logging.getLogger("py4j").setLevel(logging.WARNING)

# Create logger instance
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    
    model_full_name = f"{catalog_name}.{gold_schema_name}.{chain_model_name}"

    logger.info(f"Getting the model {model_full_name} ready for Realtime Deployment")
    latest_model_version, endpoint_config = get_ready_for_realtime_inference(model_full_name)
    
    logger.info(f"Deploying the model {model_full_name} for Serving Endpoint")
    real_time_deploy(logger, serving_endpoint_name, latest_model_version, endpoint_config)