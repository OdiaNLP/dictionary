"""
@author: Soumendra Kumar Sahoo
@date: August 2021
@function: Process English to Odia language word translations
@license: MIT License
"""
from abc import ABC, abstractmethod


class BaseTranslate(ABC):
    """
    Base class for translation
    """

    def __init__(self, text):
        self.text = text

    @abstractmethod
    async def validate(self):
        """
        Validate the provided text
        """
        pass

    @abstractmethod
    async def preprocess(self):
        """
        Preprocess the provided text
        """
