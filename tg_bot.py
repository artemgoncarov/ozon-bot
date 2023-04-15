import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from ozon import get_price, ws, tb, wb
from time import sleep


ws = ws
moscow_links = []
novosibirsk_links = []
chelyabinsk_links = []

for i in range(2, 9):
    moscow_links.append(ws[f'B{i}'].internal_value) # Moscow
    novosibirsk_links.append(ws[f'B{i}'].internal_value) # Novosibirsk
    chelyabinsk_links.append(ws[f'B{i}'].internal_value) # Chelyabinks

TOKEN = "5849532952:AAE9XUPSvXBtOtcYqnqwGhYLiI-jBNIKiSo"

router = Router()

@router.message(Command(commands=["start", "help", "hello"]))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>")

@router.message(Command(commands=["parse"]))
async def parser(message: Message) -> None:
    while 1:
        for i in range(0, len(moscow_links)):
            price = get_price(moscow_links[i])
            if price < int(ws[f'D{i+2}'].internal_value) or int(price) > int(ws[f'E{i+2}'].internal_value):
                # ws[f'D{i+2}'] = price
                await message.answer(f'{ws[f"C{i+2}"].internal_value} | {ws[f"A{i+2}"].internal_value} | Внимание! Цена вышла за диапазон: {price}')
            else:
                continue

        for i in range(0, len(novosibirsk_links)):
            price = get_price(novosibirsk_links[i])
            if price < int(ws[f'H{i+2}'].internal_value) or int(price) > int(ws[f'I{i+2}'].internal_value):
                # ws[f'J{i + 2}'] = price
                await message.answer(f'{ws[f"G{i+2}"].internal_value} | {ws[f"F{i+2}"].internal_value} | Внимание! Цена вышла за диапазон: {price}')
            else:
                continue

        for i in range(0, len(chelyabinsk_links)):
            price = get_price(chelyabinsk_links[i])
            if price < int(ws[f'H{i+2}'].internal_value) or int(price) > int(ws[f'I{i+2}'].internal_value):
                # ws[f'J{i + 2}'] = price
                await message.answer(f'{ws[f"K{i+2}"].internal_value} | {ws[f"J{i+2}"].internal_value} | Внимание! Цена вышла за диапазон: {price}')
            else:
                continue
        # wb.save(tb)

        sleep(15)


@router.message()
async def echo_handler(message: types.Message) -> None:
    try:
        # Send copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    bot = Bot(TOKEN, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())