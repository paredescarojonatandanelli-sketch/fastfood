import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # --- Configuración de Flask ---
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-por-defecto-insegura')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Datos del negocio ---
    BUSINESS_NAME = os.environ.get('BUSINESS_NAME', 'Mi Fast Food')
    BUSINESS_PHONE = os.environ.get('BUSINESS_PHONE', '51999999999')
    BUSINESS_ADDRESS = os.environ.get('BUSINESS_ADDRESS', 'Av. Ejemplo 123')
    BUSINESS_HOURS = os.environ.get('BUSINESS_HOURS', 'Lun a Dom: 12:00 pm - 10:00 pm')
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '51999999999')
    DELIVERY_COST = float(os.environ.get('DELIVERY_COST', 5.00))
    CURRENCY = 'S/'

    # --- Redes sociales (opcional) ---
    FACEBOOK_URL = os.environ.get('FACEBOOK_URL', '')
    INSTAGRAM_URL = os.environ.get('INSTAGRAM_URL', '')

    # --- Administración ---
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH', '')