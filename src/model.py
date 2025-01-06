import joblib
import preprocessing
from re import findall,sub

class Model:

    def __init__(self,text_model_path: str,url_model_path: str):
        self._text_model,self._text_pre_processor = self._load_text_model(text_model_path)
        self._url_model,self._url_pre_processor = self._load_url_model(url_model_path)

        if self._text_model == None or self._text_pre_processor == None:
            raise Exception("Could not load model or pre-processor.")

    def predict(self,message: str):
        message,urls = self._separate_urls_from_text(message)
        # print(message)
        # print(urls)

        message_pre_processed = ' '.join(preprocessing.text_pre_processing(message))

        test = self._text_pre_processor.transform([message_pre_processed])

        prediction = self._text_model.predict(test)

        return prediction
    
    def _load_text_model(self,path: str):
        model_and_pre_processor = joblib.load(path)

        if model_and_pre_processor != None:
            return model_and_pre_processor["model"],model_and_pre_processor["pre-processor"]
        
        raise Exception(f"Model not found at {path}")
    
    def _load_url_model(self,path: str):
        return None, None
    
    def _separate_urls_from_text(self,message: str):
        URL_PATTERN = r"https?://\S+"

        if len(urls := findall(URL_PATTERN,message)) == 0:
            return message, []
        
        message = sub(URL_PATTERN,"",message)

        return message, urls
        

