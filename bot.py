import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Включите логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Ваш токен бота
TOKEN = '7860849361:AAGBhe8yssIWvCtVCii2qTGpqWVg5sZc_rU'

# ID учителя
TEACHER_CHAT_ID = '1139235921'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Отправьте мне своё домашнее задание и я перешлю его учителю. '
                                     'При отправлении укажите группу, ФИО. Также стоит указать на какое число было задано домашнее задание, если это долг, то пишите на какую дату и то, что это долг. '
                                     'Также если вы отправляете код, то пишите его так: ```py (ваш код) ``` ')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    user_nickname = user.username if user.username else user.first_name
    date_time = update.message.date

    # Создаем сообщение для учителя
    message_text = f"Домашнее задание от {user_nickname}:\n\n{update.message.text}"

    # Отправляем сообщение учителю
    await context.bot.send_message(chat_id=TEACHER_CHAT_ID, text=message_text)
    await context.bot.send_message(chat_id=TEACHER_CHAT_ID, text=f"Дата и время отправки: {date_time}")

    # Подтверждаем получение сообщения от ученика
    await update.message.reply_text('Ваше домашнее задание отправлено учителю.')

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    user_nickname = user.username if user.username else user.first_name
    date_time = update.message.date

    # Получаем документ
    document = update.message.document
    file = await context.bot.get_file(document.file_id)
    await file.download_to_drive(document.file_name)

    # Отправляем документ учителю
    await context.bot.send_document(chat_id=TEACHER_CHAT_ID, document=InputFile(document.file_name),
                                    caption=f"Домашнее задание от {user_nickname}\nДата и время отправки: {date_time}")

    # Подтверждаем получение документа от ученика
    await update.message.reply_text('Ваше домашнее задание отправлено учителю.')

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    user_nickname = user.username if user.username else user.first_name
    date_time = update.message.date

    # Получаем фото
    photo = update.message.photo[-1]  # Берем самое большое изображение
    file = await context.bot.get_file(photo.file_id)
    await file.download_to_drive(f"{photo.file_id}.jpg")

    # Отправляем фото учителю
    await context.bot.send_photo(chat_id=TEACHER_CHAT_ID, photo=InputFile(f"{photo.file_id}.jpg"),
                                 caption=f"Домашнее задание от {user_nickname}\nДата и время отправки: {date_time}")

    # Подтверждаем получение фото от ученика
    await update.message.reply_text('Ваше домашнее задание отправлено учителю.')

def main() -> None:
    # Создаем приложение и передаем ему токен вашего бота.
    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.Document.MimeType("application/pdf"), handle_document))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
