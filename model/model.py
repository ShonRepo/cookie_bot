import datetime
import uuid


class Model:
    __reference = None

    def __init__(self, reference):
        self.__reference = reference

    def all(self, order='created_at'):
        return self.__reference.order_by_child(order).get()

    def find_qeury(self, id):
        return self.__reference.child(str(id))

    def find(self, id):
        return self.find_qeury(id).get()

    def add(self, object):
        object['created_at'] = str(datetime.datetime.now())

        self.__reference.child(str(uuid.uuid4())).set(object)

    def update(self, id, object):
        self.__reference.child(str(id)).set(object)

    def delete(self, id):
        self.__reference.child(str(id)).set({})
