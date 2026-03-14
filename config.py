import os
from dotenv import load_dotenv
load_dotenv()
# --- ตั้งค่าระบบ Security ---
SECRET_KEY = os.getenv("SECRET_KEY")
ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS = os.getenv("ADMIN_PASS")

# --- ตั้งค่า Router pfSense ---
ROUTER_IP = os.getenv("ROUTER_IP")
ROUTER_USER = os.getenv("ROUTER_USER")
ROUTER_PASS = os.getenv("ROUTER_PASS")

# --- ตั้งค่า MySQL Database (Docker) ---
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

