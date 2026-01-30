import os
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from telethon import TelegramClient
from binance.spot import Spot as Client

app = FastAPI()

# 🛡️ تصريح الدخول لربط Lovable بـ Railway
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    link: str

# 1. بيانات تليجرام
API_ID = 30315684
API_HASH = '968fe024f58ebe6959ac6f57a5fc5ce3'
PHONE = '+213697796454'

# 2. بيانات بينانس
B_KEY = 'JdK3RLMPog77H8BNEUgKHEh76YvcRsNvN3soRp0n4wjSoOA9z3QzK5rlwl7OWxla'
B_SECRET = 'SVDHIXmp1r5XOqbNVkTkSaAUAJIUx0UUt0i7rzMDYEUdvgOhkFIYRBvNdHTo2R2L'

t_client = TelegramClient('zakizaki_session', API_ID, API_HASH)
b_client = Client(B_KEY, B_SECRET)

@app.get("/")
async def root():
    return {"status": "Zakizaki Engine is Authenticating"}

@app.post("/activate")
async def activate(data: RequestData, background_tasks: BackgroundTasks):
    """يستلم الرابط من الموقع ويرسله للتفعيل فوراً"""
    background_tasks.add_task(send_to_telegram, data.link)
    return {"status": "processing", "message": "Login successful, sending message..."}

async def send_to_telegram(link: str):
    # 🔐 فتح الحساب باستخدام الكود الذي وصلك
    await t_client.start(phone=PHONE, code_callback=lambda: '75265') 
    async with t_client:
        # إرسال الرابط للبوت الفيتنامي
        await t_client.send_message('SheerID_VN_Bot', f"/verify {link}")

@app.get("/verify-payment")
async def verify_payment(txid: str):
    """لفحص حالة الدفع عبر بينانس"""
    try:
        status = b_client.deposit_history(txId=txid)
        return {"payment_status": status}
    except Exception as e:
        return {"error": str(e)}
