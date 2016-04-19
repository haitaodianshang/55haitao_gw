#coding: utf8

"""
@author: Wanzhi Du
@email : duwanzhi@55haitao.com
@time  : 2/18/16 12:21 AM
"""

from api_common import exception as common_exception
from core import constants

class MissingArgument(common_exception.CoreError):
    def __init__(self, argument):
        super(MissingArgument, self).__init__(constants.E_ARGUMENT_MISSING, "Missing Argument:{}".format(argument))

