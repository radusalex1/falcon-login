import os

DYNAMODB_URL = os.getenv("DYNAMODB_URL","http://localhost:8000")
DYNAMODB_REGION = os.getenv("REGION","test") # Fot local development, default can be anything
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME","accu_weather")


HOST = os.getenv("HOST","localhost")
PORT = os.getenv("PORT",8080)