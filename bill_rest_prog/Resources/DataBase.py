from sqlalchemy import text
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

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


# Serialize sqlalchemy objects returned 
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

class ConferenceDataSchema(Schema):
    rec_id        = fields.Int()
    CoSpace_id    = fields.Str()
    Name          = fields.Str()
    Autogenerated = fields.Str()
    Uri           = fields.Str()
    CallId        = fields.Str()
    SecondaryUri  = fields.Str()
    date_received = fields.DateTime()
    Ip            = fields.Str()
    local_remote  = fields.Str()
    contract      = fields.Str()
    month         = fields.Str() 

############################################################

# get device data by contract number
def get_data_by_contract(contract_num=None):
    '''' get data for contract number, could be one or many '''
    try:
       session = Session()
       data = session.query(DeviceData).filter(DeviceData.contract == contract_num)
    except SQLAlchemyError as e: 
       session.close()
       return str(e.__dict__['orig'])

    session.close()
    device_schema = DeviceDataSchema(many=True)
    json_result = device_schema.dumps(data)
    return json_result.data 

# get device data by month and day
def get_data_by_mon_date(month=None, date=None):
    '''' get data by month and date, could be one or many '''
    try:
       session = Session()
       data = session.query(DeviceData).from_statement(
              text("SELECT * FROM device_data where \
                    DATE_FORMAT(date_received,'%Y-%m-%d') \
                    =:gdate and month=:gmonth")).params(gdate=date, gmonth=month).all()
    except SQLAlchemyError as e: 
       session.close()
       return str(e.__dict__['orig'])

    session.close()
    device_schema = DeviceDataSchema(many=True)
    json_result = device_schema.dumps(data)
    return json_result.data 

# get all device data
def get_all_device_data():
    '''' get all table data '''
    try:
       session = Session()
       data = session.query(DeviceData).all()
    except SQLAlchemyError as e:
       session.close()
       return str(e.__dict__['orig'])

    session.close()
    device_schema = DeviceDataSchema(many=True)
    json_result = device_schema.dumps(data)
    return json_result.data 


# get conference data by callId 
def get_conference_by_callId(call_id=None):
    '''' get data for contract number, could be one or many '''
    try:
       session = Session()
       data = session.query(ConfData).filter(ConfData.CallId == call_id)
    except SQLAlchemyError as e: 
       session.close()
       return str(e.__dict__['orig'])

    session.close()
    conf_schema = ConferenceDataSchema(many=True)
    json_result = conf_schema.dumps(data)
    return json_result.data 

# get conference data by local or remote ip 
def get_conference_local_remote(iptype=None):
    '''' get data for contract number, could be one or many '''

    try:
       session = Session()
       data = session.query(ConfData).filter(ConfData.local_remote == iptype)
    except SQLAlchemyError as e: 
       session.close()
       return str(e.__dict__['orig'])

    session.close()
    conf_schema = ConferenceDataSchema(many=True)
    json_result = conf_schema.dumps(data)
    return json_result.data 

# get all conference data
def get_all_conferences():
    '''' get data for contract number, could be one or many '''
    try:
       session = Session()
       data = session.query(ConfData).all()
    except SQLAlchemyError as e:
       session.close()
       return str(e.__dict__['orig'])

    session.close()
    conf_schema = ConferenceDataSchema(many=True)
    json_result = conf_schema.dumps(data)
    return json_result.data 
