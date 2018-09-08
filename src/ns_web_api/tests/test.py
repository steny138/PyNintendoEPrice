
import os
import jieba
# load dotenv in the base root
from dotenv import load_dotenv, find_dotenv

APP_ROOT = os.path.dirname(__file__)
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path, override=True)

import sys
sys.path.append('../web')
from events.traffic import TrafficEvent


traffic_event = TrafficEvent()
vocabulary = ", ".join(jieba.cut('高鐵台中到台北有座位嗎')).split(', ')
print(vocabulary)

message = traffic_event.occurs(vocabulary)
print(message)