from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.googleapi_utils import spreadsheet_id, service
router = Router()


class MainCallback(CallbackData, prefix='main'):
    foo: str
    bar: str


class ComandsCallback(CallbackData, prefix='commands'):
    foo: str


builder = InlineKeyboardBuilder()
builder.button(
    text = "В главное меню",
    callback_data = MainCallback(foo="demo", bar="smth")
)

builder_commands = InlineKeyboardBuilder()
button1 = builder_commands.button(
    text = "Оставить заявку",
    callback_data = ComandsCallback(foo="/submit")
)
button2 = builder_commands.button(
    text = "Узнать статус заявки",
    callback_data = ComandsCallback(foo="/status")
)
button3 = builder_commands.button(
    text = "Получить контакты",
    callback_data = ComandsCallback(foo="/contacts")
)
builder_commands.adjust(1)
@router.message(CommandStart())
async def cmd_start(msg: types.Message) -> None:
    text = "👋 Привет, я твой универсальный помощник по заполнению заявок " \
           "на выполнение обслуживающих работ.\n\n" \
           "Теперь когда в твоем помещении перегорит" \
           " лампочка или заскрипит дверь, " \
           "смело обращайся ко мне 🚀.\n\n Я сделаю так, " \
           "чтобы твоя заявка:\n" \
           "🔹Сохранилась в моей системе\n" \
           "🔹Правильно обработалась и направилась на специалиста\n" \
           "🔹И выполнилась в рамках требуемого времени\n\n" \
           "Хочешь узнать как это сделать? Нажми на кнопку👇"
    await msg.answer(text=text, reply_markup=builder.as_markup())


@router.callback_query(MainCallback.filter(F.foo == "demo"))
async def my_callback_foo(query: CallbackQuery, callback_data: MainCallback):
    text = "✨ Главное меню\n" \
           "Выбери функцию, которая тебе нужна. Если ты потеряешь " \
           "главное меню, просто введи команду /start"
    await query.message.answer(text=text,
                               reply_markup=builder_commands.as_markup())


@router.callback_query(ComandsCallback.filter(F.foo == "/status"))
async def callback_status(query: CallbackQuery):
    space_number, count = 0, 0

    output_submit_values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Заявки!A:I',
        majorDimension='ROWS'
    ).execute()['values'][2:]
    arendators_values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Арендаторы!A:G',
        majorDimension='ROWS'
    ).execute()['values'][2:]

    for arendator in arendators_values:
        if int(query.from_user.id) == int(arendator[0]):
            space_number = int(arendator[-1])

    for submit in output_submit_values:
        if space_number == int(submit[1]):
            await query.message.answer(f"Статус заявки "
                                       f"№{submit[0]} – {submit[5]}")
        if space_number != int(submit[1]):
            count += 1
        if count == len(output_submit_values):
            await query.message.answer(
                f"Актуальных заявок нет")


@router.callback_query(ComandsCallback.filter(F.foo == "/submit"))
async def callback_submit(query: CallbackQuery):
    text = "Чтобы оставить заявку, введи команду /submit"
    await query.message.answer(text=text)


@router.callback_query(ComandsCallback.filter(F.foo == "/contacts"))
async def callback_submit(query: CallbackQuery):
    contact = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Контакты!A2:B2',
        majorDimension='ROWS'
    ).execute()['values']
    print(contact)
    await query.message.answer(f"Вы можете связаться с нами "
                     f"по номеру телефона: {contact[0][0]}")


@router.message(F.text == '/status')
async def cmd_status(msg: types.Message):
    space_number, count = 0, 0

    output_submit_values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Заявки!A:I',
        majorDimension='ROWS'
    ).execute()['values'][2:]
    arendators_values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Арендаторы!A:G',
        majorDimension='ROWS'
    ).execute()['values'][2:]

    for arendator in arendators_values:
        if int(msg.from_user.id) == int(arendator[0]):
            space_number = int(arendator[-1])

    for submit in output_submit_values:
        if space_number == int(submit[1]):
            await msg.answer(f"Статус заявки "
                                       f"№{submit[0]} – {submit[5]}")
        if space_number != int(submit[1]):
            count += 1
        if count == len(output_submit_values):
            await msg.answer(
                f"Актуальных заявок нет")


@router.message(F.text == '/contacts')
async def cmd_contacts(msg: types.Message):
    contact = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Контакты!A2:B2',
        majorDimension='ROWS'
    ).execute()['values']
    print(contact)
    await msg.answer(f"Вы можете связаться с нами "
                     f"по номеру телефона: {contact[0][0]}")
