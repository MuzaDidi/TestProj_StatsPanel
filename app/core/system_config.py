from dotenv import load_dotenv
import os

load_dotenv()

app_host = os.getenv('APP_HOST')
app_port = os.getenv('APP_PORT')

db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')

postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")

db_url = f"postgresql+asyncpg://{db_user}:{db_password}@{postgres_host}:{postgres_port}/{db_name}?async_fallback=True"
db_port = os.getenv('DB_PORT')
# db_url = f"postgresql+asyncpg://{db_user}:{db_password}@{postgres_host}:{db_port}/{db_name}?async_fallback=True"

access_token_expire_minutes = 240
algorithm = "HS256"
secret_key = os.getenv("SECRET_KEY")
