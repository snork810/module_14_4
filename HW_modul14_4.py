from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio 
from crud_functions import *


API = ""
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())




class UserState(StatesGroup): 
    age = State()
    growth = State()
    weight = State()

start_menu = ReplyKeyboardMarkup(
      keyboard = [
      [KeyboardButton(text='Информация'), 
      KeyboardButton(text='Рассчитать')],
      [KeyboardButton(text='Купить')]
      ], resize_keyboard=True)
buy_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product2', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product3', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product4', callback_data='product_buying')],
    ]
)
calclulate_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
        InlineKeyboardButton(text='Формула расчёта', callback_data='formula' )]
    ]
)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    images = [
        'F:\PYTHON\pyton_progects\socs.jpg',
        'F:\PYTHON\pyton_progects\T_short.jpg',
        'F:\PYTHON\pyton_progects\dzhins.jpg',
        'F:\PYTHON\pyton_progects\jacket.jpg',
    ]
    items = get_all_product()
    for i,v in enumerate(images):
        with open (v, 'rb') as img:
            await message.answer_photo(img)
            await message.answer(f'''Название {items[0][i][-1]} | 
            Описание {items[1][i][-1]} | Цена: {items[2][i][-1]}$
            ''')
    await message.answer("Выберите продукт для покупки:", reply_markup=buy_menu)

@dp.callback_query_handler(text="product_buying") 
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт')
    await call.answer()     


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=calclulate_menu)
@dp.callback_query_handler(text='formula')
async def set_formul(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()
@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст:" )
    await UserState.age.set()
    await call.answer() 

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age= message.text)
    data = await state.get_data()
    await message.answer("Введите свой рост в сантиметрах:" )
    await UserState.growth.set()
    

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth= message.text)
    data = await state.get_data()
    await message.answer("Введите свой вес в килограммах:" )
    await UserState.weight.set()
    

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight= message.text)
    data = await state.get_data()
    calories = int(data['weight'])*10 + int(data['growth'])*6.25 - int(data['age'])*5 + 5
    await message.answer(f"Ваша норма калорий: {calories}")
    await state.finish()





@dp.message_handler(commands=['start']) #Хэндлер для реагирования на команды
async def start_message(message):
    print("Бот запущен")  
    await message.answer(f"Привет!, {message.from_user.username}.  Я бот помогающий твоему здоровью.", reply_markup=start_menu )

@dp.message_handler()
async def all_message(message):
    print('Мы получили новое сообщение')
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
