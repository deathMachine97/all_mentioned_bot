"""Сервер Telegram бота, запускаемый непосредственно"""
import os
import logging
import re


from aiogram import Bot, Dispatcher, executor, types
emojis = ['😀', '🤨', '😤', '🤩', '😐', '😦', '😮', '🤐', '😸', '🙀', '🤖', '😼', '👾', '😎']


logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['all'])
async def send_welcome(message: types.Message):
    answer_message = "Всем привет!"
    await message.answer(answer_message)


@dp.message_handler(commands=['ket_nafig'])
@dp.message_handler(lambda message: message.text and 'пздц' in message.text.lower())
async def ket_nafig(message: types.Message):
    await bot.send_sticker(message.chat.id, 'CAACAgIAAyEFAASHPL4FAAICR2cmX-z8Cj72BX7HA_O2LFZmisPnAAJPTwACduN4SmogabSEkVsWNgQ')

some = {
    r'\bахах\w*': 'не стони нах',
}
@dp.message_handler(lambda message: message.text and any(re.search(key, message.text.lower()) for key in some.keys()))
async def respond_to_keywords(message: types.Message):
    for key, response in some.items():
        if re.search(key, message.text.lower()):
            await message.reply(response)
            break


@dp.message_handler(commands=['members'])
async def send_group_members(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        admins = await bot.get_chat_administrators(message.chat.id)        
        admins_list = " ".join([admin.user.get_mention(emojis[index], False) for index, admin in enumerate(admins)])
        response = f"Не игнорим\n{admins_list}"
        if message.reply_to_message:
            await message.reply_to_message.reply(response, parse_mode='Markdown')
        else:
            await message.answer(response, parse_mode='Markdown')
    else:
        await message.reply("Эта команда доступна только в группах и супергруппах.")
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)