import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.datatransformation import DataTransformation
from src.components.datatransformation import DataTransformationConfig

from src.components.modeltrainer import ModelTrainerConfig
from src.components.modeltrainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")
    
class DataIngestation:
    def __init__(self):
        self.ingestation_config=DataIngestionConfig()
        
    def initiate_data_ingestation(self):
        logging.info("Entred the data ingestation Component")
        try:
            df=pd.read_csv('notebook\data\stud.csv')
            logging.info('Read the dataset as dataframe')
            
            os.makedirs(os.path.dirname(self.ingestation_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestation_config.raw_data_path,index=False,header=True)
            
            logging.info("Train test splitted")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            train_set.to_csv(self.ingestation_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestation_config.test_data_path,index=False,header=True)
            logging.info("Ingestation of Data Completed")
            
            return(
                self.ingestation_config.train_data_path,
                self.ingestation_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__=='__main__':
    obj=DataIngestation()
    train_data,test_data=obj.initiate_data_ingestation()
    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.init_data_transformation(train_data,test_data)
    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))