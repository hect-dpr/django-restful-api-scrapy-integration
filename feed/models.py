from __future__ import absolute_import, division, print_function, unicode_literals

from mongoengine import *


class NiftyFifty(Document):

    meta            =   {'collection': 'niftyfifty'}

    symbol          =   StringField(required=False)
    open            =   StringField(required=False)
    high            =   StringField(required=False)
    low             =   StringField(required=False)
    ltp             =   StringField(required=False)
    chng            =   StringField(required=False)
    pcnt_chng       =   StringField(required=False)
    volume          =   StringField(required=False)
    turnover        =   StringField(required=False)
    ftwh            =   StringField(required=False)
    ftwl            =   StringField(required=False)
    tsfd_pcnt_chng  =   StringField(required=False)
    td_pcnt_chng    =   StringField(required=False)