from abc import ABCMeta, abstractmethod


class Route(metaclass=ABCMeta):

    @abstractmethod
    def build_blueprint(self):
        """
        Initializes blueprint object
        """
        pass
