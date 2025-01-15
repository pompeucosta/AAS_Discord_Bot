from abc import ABC,abstractmethod
import joblib
import preprocessing
from os import getenv
import numpy as np

class Model(ABC):
    @abstractmethod
    def predict(self,message: str,urls: list[str]):
        pass

class FastTextMLP(Model):
    def __init__(self):
        super().__init__()
        model_path = getenv("TEXT_MODEL_PATH")
        if model_path == None:
            raise Exception("Text model path not set")

        self._model,self._pre_processor = self._load_model(model_path)

    def predict(self,message: str,urls: list[str]):
        message_pre_processed = preprocessing.text_pre_processing(message)
        message_pre_processed = self._word_vector_to_sentence_vector(message_pre_processed,self._pre_processor.wv)
        
        x = self._model.predict([message_pre_processed])
        print(x)
        return x
    
    def _div_norm(self,x):
        norm_value = np.linalg.norm(x)
        if norm_value > 0:
            return x * ( 1.0 / norm_value)
        else:
            return x

    def _word_vector_to_sentence_vector(self,sentence:list, model):
        vectors = []
        # for all the tokens in the setence
        for token in sentence:
            if token in model:
                vectors.append(model[token])
        # add the EOS token
        if '\n' in model:
            vectors.append(model['\n'])
        # normalize all the vectors
        vectors = [self._div_norm(x) for x in vectors]
        return np.mean(vectors, axis=0)
    
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
