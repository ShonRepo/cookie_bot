from model.config import predictions
from model.model import Model


class Prediction(Model):
    def __init__(self, lang):
        super().__init__(self, predictions.child(str(lang)))

    def all(self):
        super().all().values()