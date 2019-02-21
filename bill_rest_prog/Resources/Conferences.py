from flask_restful import Resource
from flask_restful import abort

class Conference( Resource ):
    def __init__(self):
       self.msg = {'name':'myname'}
       self.msg2 = {'name': 'othername'}


    def get(self, name):
      return {'nameis': name}


class Conferences( Resource ):
    def __init__(self):
       self.msg = {'name':'myname'}
       self.msg2 = {'name': 'othername'}


    def get(self):
      return {'nameis': 'allconference'}


class AllConferences( Resource ):
    def __init__(self):
       self.msg = {'name':'myname'}
       self.msg2 = {'name': 'othername'}


    def get(self):
      return {'nameis': 'allconference'}
