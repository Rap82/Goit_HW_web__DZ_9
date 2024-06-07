import configparser
from mongoengine import connect
from pathlib import Path


file_config = Path(__file__).parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

mongo_user = config.get("DB", "USER")
mongodb_pass = config.get("DB", "PASSWORD")
db_name = config.get("DB", "DB_NAME")
domain = config.get("DB", "DOMAIN")

# connect to cluster on AtlasDB

# Загалний запис звернення до Бази даних MongoDB (mongodb+srv://userweb16:<password>@cluster0.fm2rljp.mongodb.net/)
# Примітка : Конкертні значення вказано в файлі config.ini
connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True,) 

# Access to connect from other files
def get_database():
    from mongoengine import get_db

    return get_db()
