from flask_restful import Resource
from flask_restful import abort

import DataBase

class Conference( Resource ):
    def get(self, callid):
       ''' returns information on single record '''

       # setup sqlalchemy here
       rsp = DataBase.get_conference_by_callId(callid)
       return rsp


class Conferences( Resource ):
  def get(self, iptype ):
      ''' returns information on a local or remote ip address '''

      #   setup the select, sqlalchemy
      rsp = DataBase.get_conference_local_remote(iptype)
      return rsp


class AllConferences( Resource ):
    def get(self):
        rsp = DataBase.get_all_conferences()
        return rsp

