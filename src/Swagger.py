import uvicorn
from  kafka3 import KafkaConsumer
from fastapi import FastAPI,Request,Form,HTTPException,APIRouter
from fastapi.responses import JSONResponse
from kafka3 import KafkaProducer


app= FastAPI(title='Msg',description='This is desc')

mq1 = APIRouter()

@mq1.get('/api/queuename')
def queuesAvailable():
    vals = ["Solace","Kafka"]
