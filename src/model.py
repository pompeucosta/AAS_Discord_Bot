from abc import ABC,abstractmethod
import joblib
import preprocessing

class Model(ABC):
    @abstractmethod
    def predict(self,message: str):
        pass

# mudar nome para algo mais significativo, por ex, BoWMLPModel (BoW pa pre processor and MLP pa ML model)
class MyTrainedModel(Model):
    def __init__(self,model_path: str):
        """An example of a model that uses BoW for pre-processing and MLP to predict the class"""
        super().__init__()
        self._model,self._pre_processor = self._load_model(model_path)

    def predict(self,message: str):
        message_pre_processed = ' '.join(preprocessing.text_pre_processing(message))
        message_pre_processed = self._pre_processor.transform(message_pre_processed)
        
        return self._model.predict(message_pre_processed)
    
    def _load_model(self,path: str):
        model_and_pre_processor = joblib.load(path)

        if model_and_pre_processor != None:
            return model_and_pre_processor["model"],model_and_pre_processor["pre-processor"]
        
        raise Exception(f"Model not found at {path}")