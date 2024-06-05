import multiprocessing
from typing import Any, Dict

class DynamicHyperparameters:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.modifiable = False
        self._initialize()

    def _initialize(self):
        manager = multiprocessing.Manager()
        self.lock = manager.Lock()
        self.attributes = manager.dict()
        items = list(self.__dict__.items())
        for key, value in items:
            self.attributes[key] = value
            if key not in ['attributes', 'modifiable', 'lock']:
                del self.__dict__[key]
            
    def __getattr__(self, key: str):
        if key in ['attributes', 'modifiable', 'lock']:
            return super().__getattribute__(key)
        elif hasattr(self, 'attributes') and key in self.attributes:
            return self.attributes[key]
        else:
            return super().__getattribute__(key)
    
    def __setattr__(self, key: str, value) -> None:
        if key in ['attributes', 'modifiable', 'lock']:
            return super().__setattr__(key, value)
        elif hasattr(self, 'attributes') and key in self.attributes:
            if self.modifiable:
                with self.lock:
                    # TODO: handle non-primitive value type
                    self.attributes[key] = value
            else:
                print('Cannot modify the value outside the context manager')
                return
        else:
            return super().__setattr__(key, value)
    
    @staticmethod
    def from_dict(d: Dict):
        return DynamicHyperparameters(**d)

class DynamicRange:
    def __init__(self, config: DynamicHyperparameters):
        self.config = config

    def __call__(self, key: str, start:int = 0, step:int = 1) -> Any:
        i = start
        while i < getattr(self.config, key):
            yield i
            i += step