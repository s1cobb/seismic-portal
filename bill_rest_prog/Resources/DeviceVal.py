import re
from marshmallow import fields
from marshmallow import Schema
from marshmallow import validates
from marshmallow import ValidationError

################### validation def setup ###################
def validate_contract_num(n):
    if not n.isdigit():
       raise ValidationError('Contract number must be numeric only')

    if len(n) != 8:
       raise ValidationError('Contract number must be 8 digits only')

def validate_month(mon):
    months = ['January', 'February', 'March', 'April', 'May',
              'June', 'July', 'August', 'September', 'October',
              'November', 'December' ]
    if mon:
       if not mon in months:
          raise ValidationError('Invalid month given in input data')

def validate_date(dat):
    if dat:
       #             year - day - month
       if re.search('\d{4}-\d{2}-\d{2}', dat):
          pass
       else:
          raise ValidationError('Invalid date format give in input data')

#################### Classes #############################
class ContractSchema(Schema):
    contract = fields.Str(validate=validate_contract_num, required=True)

class DeviceMonSchema(Schema):
    month = fields.Str(validate=validate_month)

class DeviceDateSchema(Schema):
    date = fields.Str(validate=validate_date)
