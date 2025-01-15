from abc import ABC,abstractmethod
import joblib
import preprocessing
from os import getenv

class Model(ABC):
    @abstractmethod
    def predict(self,message: str,urls: list[str]):
        pass

# mudar nome para algo mais significativo, por ex, BoWMLPModel (BoW pa pre processor and MLP pa ML model)
class MyTrainedModel(Model):
    def __init__(self):
        super().__init__()
        model_path = getenv("TEXT_MODEL_PATH")
        if model_path == None:
            raise Exception("Text model path not set")

        self._model,self._pre_processor = self._load_model(model_path)

    def predict(self,message: str,urls: list[str]):
        message_pre_processed = ' '.join(preprocessing.text_pre_processing(message))
        message_pre_processed = self._pre_processor.transform(message_pre_processed)
        
        return self._model.predict(message_pre_processed)
    
    def _load_model(self,path: str):
        model_and_pre_processor = joblib.load(path)

        if model_and_pre_processor != None:
            return model_and_pre_processor["model"],model_and_pre_processor["pre-processor"]
        
        raise Exception(f"Model not found at {path}")
    
class PhisingURLModel(Model):
    def __init__(self):
        super().__init__()
        model_path = getenv("URL_MODEL_PATH")
        if model_path == None:
            raise Exception("URL model path not set")
    
        self._model = self._load_model(model_path)

    def predict(self,message: str,urls: list[str]):
        for url in urls:
            features = preprocessing.extract_features(url)
            # Model predicts 0 for phishing and 1 for non-phishing
            if self._model.predict(features) == 0:
                return True
        return False
    
    def _load_model(self,path: str):
        
        model = joblib.load(path)

        if model != None:
            return model
        
        raise Exception(f"Model not found at {path}")
