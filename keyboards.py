from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

engine_size_keyboard = InlineKeyboardMarkup(row_width=3)
es1 = InlineKeyboardButton('1000 см3', callback_data='es1000')
es2 = InlineKeyboardButton('1200 см3', callback_data='es1200')
es3 = InlineKeyboardButton('1500 см3', callback_data='es1500')
es4 = InlineKeyboardButton('1600 см3', callback_data='es1600')
es5 = InlineKeyboardButton('2000 см3', callback_data='es2000')
es6 = InlineKeyboardButton('2200 см3', callback_data='es2200')
es7 = InlineKeyboardButton('2500 см3', callback_data='es2500')
es8 = InlineKeyboardButton('3000 см3', callback_data='es3000')
es9 = InlineKeyboardButton('3300 см3', callback_data='es3300')
es10 = InlineKeyboardButton('3500 см3', callback_data='es3500')
es11 = InlineKeyboardButton('3800 см3', callback_data='se3800')
es12 = InlineKeyboardButton('Электро', callback_data='es1')
engine_size_keyboard.add(es1, es2, es3, es4, es5, es6, es7, es8, es9, es10, es11, es12)


machine_age_keyboard = InlineKeyboardMarkup(row_width=3)
ma1 = InlineKeyboardButton('Младше 3 лет', callback_data='ma1')
ma2 = InlineKeyboardButton('От 3 до 5 лет', callback_data='ma2')
ma3 = InlineKeyboardButton('старше 5 лет', callback_data='ma3')
machine_age_keyboard.add(ma1, ma2, ma3)


delivery_method_keyboard = InlineKeyboardMarkup(row_width=2)
dm1 = InlineKeyboardButton('Автовоз', callback_data='dm1')
dm2 = InlineKeyboardButton('Контейнер (РЖД)', callback_data='dm2')
delivery_method_keyboard.add(dm1, dm2)


payment_bank_keyboard = InlineKeyboardMarkup(row_width=2)
pb1 = InlineKeyboardButton('Банк приморье', callback_data='pb1')
pb2 = InlineKeyboardButton('Райфайзен банк', callback_data='pb2')
payment_bank_keyboard.add(pb1, pb2)
