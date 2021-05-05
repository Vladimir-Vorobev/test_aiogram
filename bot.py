# -*- coding: utf-8 -*-
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

# Объект бота
bot = Bot(token="1770602296:AAGUQCL-5MrSoNf4ByyhAxakYLnww7c0-zA")
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# импортируем класс ответов
from messages import mes


# Хэндлер на команду /test1
@dp.message_handler(commands=['start', 'restart'])
async def cmd_test1(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Квест', 'Прогулка']
    keyboard.add(*buttons)
    user = message.from_user.first_name
    if user:
        if message.from_user.last_name:
            user += ' ' + message.from_user.last_name
        await message.answer("{}, т{}".format(user, mes.welcome()))
    else:
        await message.answer("Т{}".format(mes.welcome()))
    await message.answer("Вот и первая развилка 🗺")
    await message.answer(mes.describe_quest_walk(), reply_markup=keyboard)


@dp.message_handler(Text(equals="Квест"))
async def with_puree(message: types.Message):
    await message.reply(mes.start_quest(), reply_markup=types.ReplyKeyboardRemove())
    await message.answer(mes.restart())


@dp.message_handler(Text(equals="Прогулка"))
async def without_puree(message: types.Message):
    with open("media/images/museum.jpg", "rb") as file:
        data = file.read()
    await message.reply(mes.start_walk(), reply_markup=types.ReplyKeyboardRemove())
    await bot.send_photo(message.from_user.id, photo=data)
    await message.answer(mes.restart())


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
