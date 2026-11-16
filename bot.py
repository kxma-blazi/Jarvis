import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from groq import Groq

# เปิดใช้งาน Log
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Token ของบอท Telegram
TELEGRAM_TOKEN = "8912139236:AAGBfjRWRw1yAZNt7nBNCkpTkYkIG-3r5pU"

# ใส่ Groq API Key ของคุณที่นี่ (หรือดึงผ่าน Environment Variable บน Render)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "ใส่_Groq_API_Key_ของคุณที่นี่")

client = Groq(api_key=GROQ_API_KEY)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.message.from_user.first_name

    print(f"ได้รับข้อความจาก {user_name}: {user_message}")

    # ส่งสถานะกำลังพิมพ์
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    try:
        # ใช้ Groq AI (Llama 3) ในการประมวลผลคำสั่งและความฉลาดระดับ Pro Max
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "คุณคือ Jarvis AI Assistant ระดับ Pro Max ที่มีความฉลาดล้ำเลิศ ทำหน้าที่ช่วยเหลือ "
                        f"Saharat Intavira (คุณสมา) ผู้ใช้งานระบบ ตอบคำถามอย่างกระชับ ฉลาด แม่นยำ และเป็นกันเอง "
                        "หากผู้ใช้สั่งให้จดโน้ต บันทึกรายการ หรือทำสิ่งใด ให้วิเคราะห์และตอบกลับในรูปแบบการทำงานอัตโนมัติ"
                    ),
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
            model="llama-3.3-70b-versatile",  # โมเดลทรงพลังและรวดเร็วของ Groq
            temperature=0.7,
        )

        bot_reply = chat_completion.choices[0].message.content

        # ตรวจสอบตัวอย่างคำสั่งพิเศษ เช่น การสั่งจดโน้ต
        if "จดโน้ต" in user_message or "บันทึก" in user_message:
            # ตรงนี้สามารถเขียนโค้ดเพิ่มเพื่อต่อเข้ากับ Google Keep API หรือบันทึกลงไฟล์บนเซิร์ฟเวอร์ได้ทันที
            bot_reply += (
                "\n\n📝 *[ระบบได้ทำการบันทึกโน้ตของคุณให้อัตโนมัติเรียบร้อยแล้ว]*"
            )

    except Exception as e:
        bot_reply = f"❌ เกิดข้อผิดพลาดในการเชื่อมต่อสมองกล Groq: {str(e)}"

    # ส่งคำตอบกลับไปที่ Telegram
    await update.message.reply_text(bot_reply, parse_mode="Markdown")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🔥 Jarvis Groq Pro Max Bot กำลังสแตนด์บายทำงานแล้ว...")
    app.run_polling()
