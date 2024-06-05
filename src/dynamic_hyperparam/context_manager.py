from .dynamic import DynamicHyperparameters
class AllowModify:
    def __init__(self, o: DynamicHyperparameters):
        self.o = o
        self.o.modifiable = False

    def __enter__(self):
        self.o.modifiable = True
        return self

    def __exit__(self, type, value, traceback):
        self.o.modifiable = False
        return self