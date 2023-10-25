import logging
import asyncio
import datetime
# from datetime import datatime

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
# from aiogram.types import FSInputFile
from aiogram.types import ChatPermissions
from random import randint

TELEGRAM_TOKEN ="6667356167:AAGoqomIW4g65ak1RmabhGK5NedL42OcsKg"

GROUP_ID = '-1001674247269' 


# вывод отладочных сообщений в терминал
logging.basicConfig(level=logging.INFO)

# создали обьект bot
bot = Bot(token=TELEGRAM_TOKEN)

# создаем обьект диспетчер 
dp = Dispatcher()

# обрабатываем команду старт
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    image_from_pc = FSInputFile('hello.webp')
    await message.answer_photo(image_from_pc, caption='Пообщаемся?)')
    await asyncio.sleep(2)
    await message.answer("Рад тебя видеть, <b> {0.first_name} </b> !".format(message.from_user), parse_mode='html')

# обработчик команды рандом 
#  /rnd 1-30
# /random 5-10
@dp.message(Command(commands=['random', 'rand', 'rnd']))
async def get_random(message: types.Message, command: CommandObject, bot: Bot):
    # разбиваем аргументы команды символом "-"
    a, b = [int(n) for n in command.args.split('-')]
    rnum = randint(a, b)
    # в личку
    await message.reply(f'Случайное число от {a} до {b} получилось: \t {rnum}')
    # в группу



@dp.message(Command('image'))
async def upload_photo(message: types.Message):
    image_from_pc = FSInputFile('hello.webp')
    await message.answer_photo(image_from_pc, caption='Пообщаемся?)')

@dp.message(Command('mygroup'))
async def cmd_to_group(message: types.Message, bot: Bot):
    await bot.send_message(message.chat.id, 'hello from Nurullo ')

# команда забанить пользователя 
@dp.message(Command('ban'))
async def funkciya_zabanit(message: types.Message):
    # ''''''''''''''''''''''''''''''''проверка на админа''''''''''''''''''''''''''''''''
    user_status = await bot.get_chat_member(chat_id= message.chat.id, user_id=message.from_user.id)
    # если в обьекте user_status есть флаг ChatMemberOwner или ChatMemberAdministrator
    if isinstance(user_status, types.chat_member_owner.ChatMemberOwner) or isinstance(user_status, types.chat_member_administrator.ChatMemberAdministrator):

        # await message.reply(f'пользователь {message.from_user.username} имеет права')
        print (f'Админ {message.from_user.first_name} банит {message.reply_to_message.from_user.first_name} ')
    else: 
        print (f'пользователь {message.from_user.username} НЕ имеет прав')
        await message.reply(f' {message.from_user.username} у тебя нет таких прав')
        return
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    # если команда без цитаты 
    if not message.reply_to_message:
        await message.reply('пиши команду ban в ответ на сообщение')
        return
    # await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    # await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
    
    who_banned = message.reply_to_message.from_user.first_name
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
    await message.reply_to_message.reply (f'Пользователь <b>{who_banned} </b> забанен', parse_mode='html')

@dp.message(Command('mute'))
async def cmd_mute(message: types.Message, command: CommandObject, bot: Bot):
     adminNAME = message.from_user.first_name
     usrID=message.reply_to_message.from_user.id
     usrNAME = message.reply_to_message.from_user.first_name
     long, kak_dolga = [n for n in command.args.split('-')]
     kak_dolga = int(kak_dolga)
     vremiaMuta= cherez_tri_chasa = datetime.datetime.now() + datetime.timedelta(hours= kak_dolga)
     await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=usrID, permissions=ChatPermissions(can_send_messages=False), until_date =vremiaMuta)
     await message.reply(f'{adminNAME} замутировал {usrNAME} на {kak_dolga} часов')
     
# ping pong 
@dp.message()
async def echo(message: types.Message):
    print('message listened')
    # await message.reply('сообщение ботом не обработано')

    # await message.answer('бот Сергея услышал: ' + message.text)



# непрерывный режим работы бота в АССИНХРОННОМ режиме 
async def main():
    await dp.start_polling(bot)
    # del all unhandled messages 
    await bot.delete_webhook(drop_pending_updates=True)

# основной цикл
if __name__ == '__main__':
    asyncio.run(main())