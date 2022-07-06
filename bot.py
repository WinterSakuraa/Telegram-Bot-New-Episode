import asyncio
from asyncore import loop
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from main import boruto, hero_shield


token = '5231321593:AAGEI2kbfOxLvjAbFc5j8Eu0aTMrHKO8OXE'

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(
        text="The Rising of the Shield Hero Season 2")
    keyboard.add(button_1)
    button_2 = "Boruto"
    keyboard.add(button_2)
    button_3 = "New Episodes"
    keyboard.add(button_3)
    await message.answer("Choose the option:", reply_markup=keyboard)


@dp.message_handler(Text(equals="The Rising of the Shield Hero Season 2"))
async def hero_shield_eps(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        text="Watch", url="https://animego.org/anime/voshozhdenie-geroya-schita-2-1993")
    keyboard.add(button1)

    with open('hero_shield.json') as file:
        episodes_dict = json.load(file)

    for key, value in sorted(episodes_dict.items()):
        number = value['episode_num']
        title = value['episode_title']
        if value['isPosted']:
            date = value['episode_date']
            episodes = f"<b>{number}</b>\n\nTitle: <b>{title}</b>"
            await message.answer(episodes, reply_markup=keyboard)
        else:
            episodes = f"<b>{number}</b>\n\nTitle: <b>{title}</b>\n\nPost Date: <b>{date}</b>"
            await message.answer(episodes)


@dp.message_handler(Text(equals="Boruto"))
async def boruto_eps(message: types.Message):
    with open('boruto.json') as file:
        episodes_dict = json.load(file)

    for key, value in sorted(episodes_dict.items()):
        number = value['episode_num']
        title = value['episode_title']
        link = value['episode_link']

        episodes = f"{number}\n{title}\n{link}"
        await message.answer(episodes)


@dp.message_handler(Text(equals="New Episodes"))
async def new_episodes(message: types.Message):
    new_eps_of_hero_shield = hero_shield()
    new_eps_of_boruto = boruto()

    if len(new_eps_of_hero_shield) > 0:
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            text="Watch", url="https://animego.org/anime/voshozhdenie-geroya-schita-2-1993")
        keyboard.add(button1)

        for key, value in sorted(new_eps_of_hero_shield.items()):
            number = value['episode_num']
            title = value['episode_title']
            if value['isPosted']:
                date = value['episode_date']
                episodes = f"<b>{number}</b>\n\nTitle: <b>{title}</b>"
                await message.answer(episodes, reply_markup=keyboard)
            else:
                episodes = f"<b>{number}</b>\n\nTitle: <b>{title}</b>\n\nPost Date: <b>{date}</b>"
                await message.answer(episodes)

    elif len(new_eps_of_boruto) >= 1:
        for key, value in sorted(new_eps_of_boruto.items()):
            number = value['episode_num']
            title = value['episode_title']
            link = value['episode_link']

            episodes = f"{number}\n{title}\n{link}"
            await message.answer(episodes)
    else:
        await message.answer("There are no new episodes")


async def every_day():
    while True:
        new_eps = boruto()
        if len(new_eps) >= 1:
            for key, value in sorted(new_eps.items()):
                number = value['episode_num']
                title = value['episode_title']
                link = value['episode_link']

                episodes = f"{number}\n{title}\n{link}"
                await bot.send_message(695076678, episodes)

        await asyncio.sleep(3600 * 12)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(every_day())
    executor.start_polling(dp)
