import os
from dotenv import load_dotenv

load_dotenv()

myplan_cookie = os.getenv("MYPLAN_COOKIE")
user_agent = os.getenv("USER_AGENT")
