from re import findall,sub
from model import Model

class ModelHandler:
    def __init__(self,text_model: Model,url_model: Model):
        self.text_model = text_model
        self.url_model = url_model
        
    def predict(self,message: str):
        message,urls = self._separate_urls_from_text(message)

        url_prediction = False
        if len(urls) > 0 and self.url_model != None:
            url_prediction = self.url_model.predict(message,urls)

        message_prediction = False

        if self.text_model != None:
            message_prediction = self.text_model.predict(message,urls)

        return message_prediction and url_prediction
    
    def _separate_urls_from_text(self,message: str):
        URL_PATTERN = r"https?://\S+"

        if len(urls := findall(URL_PATTERN,message)) == 0:
            return message, []
        
        message = sub(URL_PATTERN,"",message)

        return message, urls
        

