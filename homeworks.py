from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


homework_router = Router()


class Homework(StatesGroup):
    tg_id = State()
    name = State()
    group = State()
    hw_number = State()
    link = State()


groups = {
    "Python 38-3",
    "Frontend 32-3",
}


def groups_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for group in groups:
        kb.add(group)
    return kb


def homework_number_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(1, 10):
        kb.add(str(i))
    return kb


@homework_router.message(Command("homework"))
async def cmd_homework(message: types.Message, state: FSMContext):
    await state.set_state(Homework.tg_id)
    await state.update_data(tg_id=message.from_user.id)
    await state.set_state(Homework.name)
    await message.answer("Как вас зовут?")


@homework_router.message(Homework.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Homework.group)
    await message.answer("Какая у вас группа?", reply_markup=groups_keyboard)


@homework_router.message(Homework.group)
async def process_group(message: types.Message, state: FSMContext):
    if message.text in groups:
        await state.update_data(group=message.text)
        await state.set_state(Homework.hw_number)
        await message.answer("Какое домашнее задание?", reply_markup=homework_number_keyboard())
    else:
        return


@homework_router.message(Homework.hw_number)
async def process_hw_number(message: types.Message, state: FSMContext):
    number = message.text
    if not number.isdigit():
        return
    number = int(number)
    if number < 1 or number > 9:
        return
    await state.update_data(hw_number=message.text)
    await state.set_state(Homework.link)
    await message.answer("Ссылка на домашнее задание?")


@homework_router.message(Homework.link)
async def process_link(message: types.Message, state: FSMContext):
    if not message.text.startswith("https://github.com"):
        await message.answer("Введите ссылку на GitHub")
        return
    await state.update_data(link=message.text)
    data = await state.get_data()
    await message.answer("Спасибо за информацию!")
    await state.clear()