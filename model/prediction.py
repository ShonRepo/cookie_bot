from model.config import predictions
from model.model import Model


class Prediction(Model):
    def __init__(self, lang):
        super().__init__(predictions.child(str(lang).lower()))

    def all(self, page=0, per_page=10):
        predictions = []

        offset = page * per_page
        index = 0
        for prediction in reversed(super().all().values()):
            if index >= offset and index <= offset + per_page:
                predictions.append(str(index) + ". " + prediction['title'])

            index = index + 1

        return [len(predictions) - offset >= per_page, '\n'.join(predictions)]

    def ids(self):
        return list(reversed(list(super().all().keys())))
