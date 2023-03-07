from model.config import predictions
from model.model import Model


class Language(Model):
    def __init__(self):
        super().__init__(predictions)

    def all(self):
        '\n'.join(super().all().values())
