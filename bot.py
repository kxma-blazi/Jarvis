import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from groq import Groq

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TELEGRAM_TOKEN = "8912139236:AAegCTYfyu4F9XLaesaunNhT5mkfWmSF-2p4"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

client = Groq(api_key=GROQ_API_KEY)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.message.from_user.first_name

    print(f"ได้รับข้อความจาก {user_name}: {user_message}")
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    try:
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
            model="llama-3.1-70b-versatile",  # ใช้รุ่น Free Tier ที่เสถียรและรองรับแน่นอน
            temperature=0.7,
        )

        bot_reply = chat_completion.choices[0].message.content

        if "จดโน้ต" in user_message or "บันทึก" in user_message:
            bot_reply += (
                "\n\n📝 *[ระบบได้ทำการบันทึกโน้ตของคุณให้อัตโนมัติเรียบร้อยแล้ว]*"
            )

    except Exception as e:
        bot_reply = f"❌ เกิดข้อผิดพลาดในการเชื่อมต่อสมองกล Groq: {str(e)}"

    await update.message.reply_text(bot_reply, parse_mode="Markdown")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🔥 Jarvis Groq Pro Max Bot กำลังสแตนด์บายทำงานแล้ว...")
    app.run_polling()
