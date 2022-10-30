from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import engine_size_keyboard, machine_age_keyboard, delivery_method_keyboard, payment_bank_keyboard
import requests

storage = MemoryStorage()

with open('TOKEN.ini', 'r') as token:
    TOKEN = token.read()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


class Details(StatesGroup):
    exchange_rate = State()
    auto_price = State()
    engine_size = State()
    machine_age = State()
    delivery_method = State()
    payment_bank = State()


@dp.message_handler(commands=['start'], state=None)
async def start_handler(message: types.Message):
    await bot.send_message(message.from_user.id, 'Добрый день!\nДавайте посчитаем приблизительную конечную стоимость машины.\n\nДля начала укажите курс воны к рублю.\nЕго вы можете посмотреть по данной ссылке - https://www.primbank.ru/currency\nВыбрав «Курсы для переводов SWIFT».\nНас интересует KWR — продажа.')
    await Details.exchange_rate.set()


@dp.message_handler(state=Details.exchange_rate)
async def set_exchange_rate(message: types.Message, state: FSMContext):
    await state.update_data(exchange_rate=message.text)
    await Details.auto_price.set()
    await message.answer('Укажите стоимость авто в вонах')


@dp.message_handler(state=Details.auto_price)
async def set_auto_price(message: types.Message, state: FSMContext):
    await state.update_data(auto_price=message.text)
    await message.answer('Укажите объем мотора:', reply_markup=engine_size_keyboard)
    await Details.next()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('es'), state=Details.engine_size)
async def set_engine_size(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(engine_size=callback.data)
    await callback.message.answer(f'Выберете категорию возраста машины:', reply_markup=machine_age_keyboard)
    await Details.next()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('ma'), state=Details.machine_age)
async def set_machine_age(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(machine_age=callback.data)
    await callback.message.answer(f'Укажите чем бы Вы хотели доставить до своего города машину:\n- Автовоз\n- Контейнер (РЖД)', reply_markup=delivery_method_keyboard)
    await Details.next()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('dm'), state=Details.delivery_method)
async def set_delivery_method(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(delivery_method=callback.data)
    await callback.message.answer('Укажите через какой банк вы будете оплачивать расходы по Корее:', reply_markup=payment_bank_keyboard)
    await Details.next()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('pb'), state=Details.payment_bank)
async def set_payment_bank(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(payment_bank=callback.data)

    data = await state.get_data()
    exchange_rate = float(data['exchange_rate'])
    CAB = data['auto_price']
    CAP = round(int(CAB)/1000 * exchange_rate)
    engine_size = int(data['engine_size'].replace('es', ''))
    machine_age = data['machine_age']
    euro_exchange = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()['Valute']['EUR']['Value']
    broker_services = 90000
    client_services = 100000
    delivery_method = data['delivery_method']
    payment_bank = data['payment_bank']
    final_price = CAP+round(exchange_rate * 300)+round(1600 * exchange_rate)+round(75 * exchange_rate)+round((engine_size * 3 * euro_exchange if machine_age == 'ma2' else round(CAP*0.5)))+broker_services+(140000 if delivery_method == 'dm1' else 190000)+client_services

    await callback.message.answer(f"Готово!\n\nКурс: {exchange_rate} Р = 1000 W\n\nЦена авто в рублях: {CAP} Р\nКомиссия диллера/аукциона: {round(exchange_rate * 300)}\nЦена судна до Владивостока: {round(1600 * exchange_rate)}\nКомиссия за SWIFT перевод: {round(75 * exchange_rate)}\n\nСтоимость растаможки: {round(engine_size * 3 * euro_exchange if machine_age == 'ma2' else round(CAP*0.5))} Р\nУслуги брокера: {broker_services} Р\n\nСтоимость доставки по России: {140000 if delivery_method == 'dm1' else 190000} Р\nКомиссия за агентские услуги: {client_services} Р\n\nПриблизительная финальная стоимость под ключ: {final_price if payment_bank == 'pb1' else final_price/100*5+final_price} Р\n\n\nВышеуказанный расчет складывается исключительно из реального курса валют на сегодняшний день и не является точной финальной суммой. На разных этапах работы от курса может меняться стоимость тех или иных расходных пунктов. Кроме того, логистические или таможенные цепочки могут ввести повышение стоимости услуг в связи с большим ажиотажем в данной сфере. Чтобы быть на 100% уверенным что вашего бюджета хватит, нужно иметь 100-200 тыс. рублей запаса на случай повышения цен или курса.\n\nЕсли Вас устроил данный расчет, и вы готовы к заказу автомобиля из Южной Кореи, Вы можете оставить заявку на почту AutoKoreaNN@yandex.ru или обратиться к администрации канала в телеграмме t.me/autokoreaNN")
    await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp)
