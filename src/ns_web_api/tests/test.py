
import os
# load dotenv in the base root
from dotenv import load_dotenv, find_dotenv

APP_ROOT = os.path.dirname(__file__)
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path, override=True)

import sys
sys.path.append('../web')
from events.traffic import TrafficEvent


traffic_event = TrafficEvent()
message = traffic_event.occurs(['高鐵', '台北', '左營', '有', '空位'])
print(message)