import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# ตั้งค่า Logging ให้ละเอียด
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Token ของบอท Telegram
TOKEN = "8912139236:AAGBfjRWRw1yAZNt7nBNCkpTkYkIG-3r5pU"

# เก็บประวัติการสนทนาเบื้องต้นแยกตาม User (Memory)
user_histories = {}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    print(
        f"[Pro Max Agent] ได้รับข้อความจาก {user_name} (ID: {user_id}): {user_message}"
    )

    # ส่งสถานะกำลังพิมพ์ (Typing Action) ให้ดูสมจริงเหมือน AI ตัวท็อปกำลังคิด
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    # ส่งข้อความตั้งต้น
    sent_message = await update.message.reply_text(
        "⚡ กำลังวิเคราะห์และประมวลผลด้วยระบบ Pro Max..."
    )

    try:
        # จำลองการประมวลผลขั้นสูง (หรือเชื่อมต่อไปยังระบบแกนหลัก OpenJarvis / LLM API โดยตรง)
        # ตรงนี้เราสามารถต่อเข้ากับ Python SDK ของ OpenAI, Anthropic Claude, หรือ Groq เพื่อดึงความฉลาดระดับสูงสุดได้ทันที

        response_text = (
            f"🤖 **Jarvis Pro Max AI Agent**\n"
            f"───────────────────\n"
            f"สวัสดีครับคุณ {user_name}! ระบบได้รับคำสั่งเรียบร้อยแล้ว\n\n"
            f"💡 **วิเคราะห์คำสั่ง:** `{user_message}`\n"
            f"🚀 **สถานะระบบ:** เชื่อมต่อโครงข่าย 24/7 พร้อมลุยงานเต็มระบบ ไม่มีสะดุด\n\n"
            f"*(คุณสามารถสั่งงานระบบอัตโนมัติ, ดึงข้อมูลไฟล์, หรือให้ช่วยเขียนโค้ดเชิงลึกได้ทันทีครับ)*"
        )

        # อัปเดตข้อความกลับไปที่ Telegram
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=sent_message.message_id,
            text=response_text,
            parse_mode="Markdown",
        )

    except Exception as e:
        error_msg = f"❌ เกิดข้อผิดพลาดในระบบ Pro Max: {str(e)}"
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=sent_message.message_id,
            text=error_msg,
        )


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # ดักจับข้อความที่เป็นตัวหนังสือทั้งหมด
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🔥 Jarvis Telegram Bot [Pro Max Edition] กำลังรันสแตนด์บายออนไลน์แล้ว...")
    app.run_polling()
