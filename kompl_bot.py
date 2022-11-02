from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from sql import gen, kompl_token

import asyncio
import aioschedule as schedule

# подключаемся к боту
bot = Bot(token= kompl_token())
dp = Dispatcher(bot)
id = 1831835977


#Клиентская часть
async def command_utro():
        await bot.send_message(chat_id= id, text= "Доброе утро, надеюсь у тебя сегодня будет отличный день!")


async def command_kompl():
        await bot.send_message(chat_id= id, text= await gen())  


async def command_noch():
        await bot.send_message(chat_id= id, text= "Спокойной ночи, малышка")


async def scheduler():
    schedule.every().day.at("09:00").do(command_utro)
    schedule.every(3).seconds.do(command_kompl)
    schedule.every().day.at("23:30").do(command_noch)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

        
async def on_startup(dp): 
    print('Живой')
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)