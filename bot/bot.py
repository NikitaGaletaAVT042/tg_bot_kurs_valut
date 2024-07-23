from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import redis
import logging
import asyncio

API_TOKEN = '7369090499:AAHWMDOJRrb3qouBMr5yM0qcsG14jFwZZ8Y'
REDIS_HOST = 'redis'
REDIS_PORT = 6379

# Настройка бота и Redis
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@dp.message(Command('rates'))
async def send_rates(message: types.Message):
    rates = []
    for key in redis_client.scan_iter('currency:*'):
        currency = key.split(':')[1]
        value = redis_client.get(key)
        rates.append(f'{currency}: {value}')
    await message.answer('\n'.join(rates))


@dp.message(Command('exchange'))
async def exchange_rate(message: types.Message):
    parts = message.text.split()
    if len(parts) != 4:
        await message.answer("Используйте команду в формате: /exchange <FROM> <TO> <AMOUNT>")
        return

    from_currency, to_currency, amount = parts[1], parts[2], float(parts[3])
    from_rate = redis_client.get(f'currency:{from_currency}')
    to_rate = redis_client.get(f'currency:{to_currency}')

    if from_rate is None:
        await message.answer(f"Курс для валюты {from_currency} не найден.")
        return

    if to_rate is None:
        await message.answer(f"Курс для валюты {to_currency} не найден.")
        return

    converted_amount = (amount * float(from_rate)) / float(to_rate)
    await message.answer(f'{amount} {from_currency} = {converted_amount:.2f} {to_currency}')


async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
