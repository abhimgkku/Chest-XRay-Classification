import sys
from Xray.components.data_ingestion import DataIngestion
from Xray.components.data_transformation import DataTransformation
#from Xray.components.model_training import ModelTrainer
#from Xray.components.model_evaluation import ModelEvaluation
#from Xray.components.model_pusher import ModelPusher
from Xray.exception import XRayException
from Xray.logger import logging
from Xray.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
#    ModelTrainerArtifact,
#    ModelEvaluationArtifact,
#    ModelPusherArtifact
    )

from Xray.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
  #  ModelTrainerConfig,
   # ModelEvaluationConfig,
    #ModelPusherConfig
)

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_transformation_config = DataTransformationConfig()
      #  self.model_trainer_config = ModelTrainerConfig()
       # self.model_evaluation_config=ModelEvaluationConfig()
        #self.model_pusher_config = ModelPusherConfig()
        
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:

            logging.info("Getting the data from s3 bucket")

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config,
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Got the train_set and test_set from s3")

            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise XRayException(e, sys)
    
    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataTransformationArtifact:
        
        logging.info("Entered the start_data_transformation method of TrainPipeline class")

        try:
            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_transformation_config=self.data_transformation_config,
            )

            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )

            logging.info(
                "Exited the start_data_transformation method of TrainPipeline class"
            )

            return data_transformation_artifact

        except Exception as e:
            raise XRayException(e, sys)
        
    
    def run_pipeline(self) -> None:
        logging.info("Entered the run_pipeline method of TrainPipeline class")

        try:
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()
            data_transformation_artifact: DataTransformationArtifact = (
                self.start_data_transformation(
                    data_ingestion_artifact=data_ingestion_artifact
                )
            )
        except Exception as e:
            raise XRayException(e,sys)

