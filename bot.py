from aiogram import Bot, Dispatcher, executor, types
from loguru import logger
from aiogram.filters.command import Command
import re

from config import TOKEN
import sqlite3
import os

from youtube import dowload_video

bot = Bot(token=TOKEN)
dp = Dispatcher(bot) # https://habr.com/ru/articles/732136/, говорят надо использовать роутер

con = sqlite3.connect(r"Person_files.db")
cursor = con.cursor()
sql = 'INSERT INTO Person_files(person_id, name_files) VALUES(?, ?)'

# pattern = r"^(https?:\/\/)?([\w-]{1,32}\.[\w-]{1,32})[^\s@]*$"
# pattern = r"^(https?:\/\/)?(vm.tiktok.com\/)[^\s@]*$"
pattern = r"^(https?:\/\/)?(www.youtube.com\/)[^\s@]*$"


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(f'Привет! Приятно познакомиться {message.from_user.first_name}. Чем я могу помочь?)')

# @dp.message_handler(commands=['help'])
# async def bot_help(message: types.Message):
#     text = ("Список команд: ",
#             "/start - Начать диалог",
#             "/help - Получить справку",
#             "/audio - это команда для скачивания видео и отправка вам аудио сообщением",
#             "/video - это команда для скачивания видео и отправки вам видео сообщением")
#
#     await message.answer("\n".join(text))
# https://vm.tiktok.com/ZMYhdq2yG/ https://www.youtube.com/watch?v=4II3l3QXXo0
async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("audio", "Скачать видео из ютуба и переести в аудио")
        ]
    )


@dp.message_handler(commands=["answer"])
async def cmd_answer(message: types.Message):
    await message.answer("Это простой ответ")

@logger.catch
@dp.message_handler(Command('audio')) # @dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    logger.debug(msg.text)
    cursor.execute("SELECT * FROM Person_files")
    #logger.debug(cursor.fetchall())
    if re.match(pattern, msg.text):
        con.executemany(sql, [(msg.from_user.id, msg.text)])
        await msg.answer('This is TikTok link!')
        title = dowload_video(msg.text, type="video")
        audio = open(f'audio/{title}', 'rb')
        await msg.answer(text="Все скачалось держи аудио")
        try:
            await bot.send_video(msg.chat.id, audio)
            await bot.send_message(msg.chat.id, text='👍')
        except:
            await msg.answer(text="Файл слишком большой")
        os.remove(f'audio/{title}')
        # await state.finish()


# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text)

if __name__ == '__main__':
    executor.start_polling(dp)
