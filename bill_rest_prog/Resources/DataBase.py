from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from marshmallow import Schema
from marshmallow import fields
from marshmallow import pprint

####### sqlalchemy setup #######
Base = declarative_base()
db_engine = create_engine('mysql+pymysql://localhost/Billing', echo=True)
Session = sessionmaker(bind=db_engine)

####### mappping of classes to database tables ########
class DeviceData(Base):
    __tablename__ = 'device_data'

    rec_id = Column(Integer, primary_key=True) 
    TotalDevices = Column(Integer)
    TotalUsers   = Column(Integer)
    EnhancedPlus = Column(Integer)
    Enhanced     = Column(Integer)
    TelePresence = Column(Integer)
    CuwlStandard = Column(Integer)
    Basic        = Column(Integer)
    Essential    = Column(Integer)
    Timestamp    = Column(DateTime)
    Elm          = Column(String(50))
    ElmLastContact = Column(String(50))
    date_received  = Column(DateTime) 
    Ip           = Column(String(20))
    local_remote = Column(String(12))
    contract     = Column(String(12))
    month        = Column(String(12))


class ConfData(Base):
    __tablename__ = 'conference_data'

    rec_id = Column(Integer, primary_key=True)
    CoSpace_id    = Column(String(45))
    Name          = Column(String(100))
    Autogenerated = Column(String(6))
    Uri           = Column(String(30))
    CallId        = Column(String(30))
    SecondaryUri  = Column(String(30))
    date_received = Column(DateTime)
    Ip            = Column(String(20))
    local_remote  = Column(String(10))
    contract      = Column(String(12))
    month         = Column(String(12)) 
################################################################

######################### Serialize here #######################
class DeviceDataSchema(Schema):
    rec_id       = fields.Int()
    TotalDevices = fields.Int()
    TotalUsers   = fields.Int()
    EnhancedPlus = fields.Int()
    Enhanced     = fields.Int()
    TelePresence = fields.Int()
    CuwlStandard = fields.Int()
    Basic        = fields.Int()
    Essential    = fields.Int()
    Timestamp    = fields.DateTime() 
    Elm          = fields.Str()
    ElmLastContact = fields.Str()
    date_received  = fields.DateTime()
    Ip           = fields.Str()
    local_remote = fields.Str()
    contract     = fields.Str()
    month        = fields.Str()


def get_data_by_contract(contract_num=None):
    '''' get data for contract number, could be one or many '''

    session = Session()
    data = session.query(DeviceData).filter(DeviceData.contract == contract_num) 
    device_schema = DeviceDataSchema(many=True)

    json_result = device_schema.dumps(data)
    return json_result.data 
