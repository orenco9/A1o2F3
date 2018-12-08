from abc import ABCMeta, abstractmethod


class Strategy:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def allin_or_fold(self, hand, balances, position, looseness_factors):
        raise NotImplementedError("Please Implement this method")
