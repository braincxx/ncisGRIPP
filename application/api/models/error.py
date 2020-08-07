from __future__ import absolute_import
from datetime import date, datetime

from typing import List, Dict

from .base_model_ import Model
from application.api import util

class Error(Model):
    def __init__(self, message: str=None):
        self.swagger_types = {
            'message': str
        }

        self.attribute_map = {
            'message': 'message'
        }
        self._message = message

    @classmethod
    def from_dict(cls, attr_dict) -> 'Error':
        """Returns the dict as a model
        :param attr_dict: A dict.
        :type: dict
        :return: The Error of this Error.
        :rtype: Error
        """
        return util.deserialize_model(attr_dict, cls)

    @property
    def message(self) -> str:
        """Gets the message of this Error.
        :return: The message of this Error.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """Sets the message of this Error.
        :param message: The message of this Error.
        :type message: str
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")

        self._message = message
