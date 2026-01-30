import os
from fastapi import FastAPI, BackgroundTasks
from telethon import TelegramClient
from binance.spot import Spot as Client # مكتبة بينانس الضرورية

app = FastAPI()

# 1. بيانات تليجرام (لإرسال الرابط للفيتنامي)
API_ID = 30315684
API_HASH = '968fe024f58ebe6959ac6f57a5fc5ce3'
PHONE = '+213697796454'

# 2. بيانات بينانس (لفحص الدفع آلياً)
B_KEY = 'JdK3RLMPog77H8BNEUgKHEh76YvcRsNvN3soRp0n4wjSoOA9z3QzK5rlwl7OWxla'
B_SECRET = 'SVDHIXmp1r5XOqbNVkTkSaAUAJIUx0UUt0i7rzMDYEUdvgOhkFIYRBvNdHTo2R2L'

# إعداد المحركات
t_client = TelegramClient('zakizaki_session', API_ID, API_HASH)
b_client = Client(B_KEY, B_SECRET)

@app.get("/")
async def root():
    return {"status": "Zakizaki Engine Online", "binance_status": "Connected"}

@app.post("/activate")
async def activate(link: str, background_tasks: BackgroundTasks):
    """يستلم الرابط من Lovable ويرسله للتفعيل في الخلفية"""
    background_tasks.add_task(send_to_telegram, link)
    return {"status": "processing", "message": "Activation started"}

async def send_to_telegram(link: str):
    async with t_client:
        # إرسال الرابط مباشرة للبوت الفيتنامي الأصلي
        await t_client.send_message('SheerID_VN_Bot', f"/verify {link}")

@app.get("/verify-payment")
async def verify_payment(txid: str):
    """وظيفة جديدة لفحص حالة الدفع عبر بينانس"""
    try:
        # فحص سجل الدفعات باستخدام TXID
        status = b_client.deposit_history(txId=txid)
        return {"payment_status": status}
    except Exception as e:
        return {"error": str(e)}
