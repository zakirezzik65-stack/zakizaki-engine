import os
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from telethon import TelegramClient
from binance.spot import Spot as Client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    link: str

# بياناتك المسحوبة من الصور
API_ID = 30315684
API_HASH = '968fe024f58ebe6959ac6f57a5fc5ce3'
PHONE = '+213697796454'
B_KEY = 'JdK3RLMPog77H8BNEUgKHEh76YvcRsNvN3soRp0n4wjSoOA9z3QzK5rlwl7OWxla'
B_SECRET = 'SVDHIXmp1r5XOqbNVkTkSaAUAJIUx0UUt0i7rzMDYEUdvgOhkFIYRBvNdHTo2R2L'

t_client = TelegramClient('zakizaki_session', API_ID, API_HASH)
b_client = Client(B_KEY, B_SECRET)

@app.get("/")
async def root():
    return {"status": "Waiting for Login Code"}

@app.post("/activate")
async def activate(data: RequestData, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_to_telegram, data.link)
    return {"status": "processing", "message": "Check your Telegram for login code"}

async def send_to_telegram(link: str):
    # هذه الخطوة ستجبر تليجرام على إرسال الكود فوراً
    await t_client.start(phone=PHONE) 
    async with t_client:
        await t_client.send_message('SheerID_VN_Bot', f"/verify {link}")
