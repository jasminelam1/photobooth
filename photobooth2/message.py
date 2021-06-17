import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
import requests
import time
from twilio.rest import Client
from rpi_camera import RPiCamera
import base64
import cloudinary.uploader
import cloudinary
import cloudinary.api


cam = RPiCamera()

account_id = "AC7dc9522a056142318ab0305ae59473dc"
auth_token = "fc4ed9c3025427a58f722a9cee4f3cc7"
client = Client(account_id, auth_token)
key = "185356582776223"	
secret = "TwuggB-HUh7N1Fru_xjqjM48aDA"
cloudinary.config(
  cloud_name = "dvkpjyj0w",
  api_key = key,
  api_secret = secret
)

@anvil.server.callable
def send_message(recipient, message):
  image = cam.get_frame()
  url = cloudinary.uploader.upload("image.jpg")["secure_url"]
  encoded = base64.b64encode(image)
  account_id = "AC7dc9522a056142318ab0305ae59473dc"
  auth_token = "fc4ed9c3025427a58f722a9cee4f3cc7"
  phone_number = "+14143124358"
  client.messages.create(
        body = message,
        from_ = phone_number,
        to = recipient,
        media_url = [url]
  )


  
@anvil.server.callable
def save_new_number(number):
  print("save new number")
  """Save a new number. This runs when the UI box is checked"""
  status = ""
  
  """get all the numbers from our DB"""
  existing_numbers = app_tables.phone_numbers.search()
  
  for row in existing_numbers:
      
    if row['phone_number'] == number:
      status = "The number already exists"
      return status
  
  """Anvil Data Tables don't have an auto-increment feature, so we store a new ID here"""
  new_index = len(app_tables.phone_numbers.search()) + 1
  timestamp = time.time()
    
  if timestamp > 0:
    new_row = app_tables.phone_numbers.add_row(index=new_index, phone_number=number)
    status = "adding number " + str(number)
    
  return status

@anvil.server.callable
def get_numbers():
  number_list = []
  
  for number in app_tables.phone_numbers.search():
    
    number_list.append(number['phone_number'])  
  return number_list

anvil.server.connect("7JKMTX5R2N5BSH5UWROO2X3L-YDKTJLVMSCV4ZIKF")
anvil.server.wait_forever()