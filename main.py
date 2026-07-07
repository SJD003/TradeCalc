import json
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# إعدادات النظام
logging.basicConfig(level=logging.INFO)
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

bot = Bot(token=config['bot_token'])
dp = Dispatcher(storage=MemoryStorage())

class CalcState(StatesGroup):
    profession = State()
    collecting_inputs = State()

def compute(formula, inputs):
    try:
        # تحويل المعادلة النصية إلى حسابية
        for key, val in inputs.items():
            formula = formula.replace(key, str(val))
        return eval(formula)
    except: return None

@dp.message(Command("start"))
async def start(msg: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text=p)] for p in config['professions'].keys()], resize_keyboard=True)
    await msg.answer("مرحباً بك في الحاسبة الذكية 🤖\nاختر مهنتك للبدء:", reply_markup=markup)
    await state.set_state(CalcState.profession)

@dp.message(CalcState.profession)
async def pick_prof(msg: types.Message, state: FSMContext):
    if msg.text not in config['professions']: return await msg.answer("يرجى الاختيار من القائمة.")
    await state.update_data(prof=msg.text, inputs={}, step=0)
    await state.set_state(CalcState.collecting_inputs)
    await send_step(msg, state)

async def send_step(msg: types.Message, state: FSMContext):
    data = await state.get_data(); prof = data['prof']; step = data['step']
    markup = types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="⬅️ السابق"), types.KeyboardButton(text="➡️ التالي")],
        [types.KeyboardButton(text="🏠 الرئيسية")]
    ], resize_keyboard=True)
    await msg.answer(f"الخطوة {step+1}: أدخل **{config['professions'][prof]['inputs'][step]}**:", parse_mode="Markdown", reply_markup=markup)

@dp.message(CalcState.collecting_inputs)
async def process(msg: types.Message, state: FSMContext):
    if msg.text == "🏠 الرئيسية": await state.clear(); return await start(msg, state)
    data = await state.get_data(); prof = data['prof']; step = data['step']
    
    if msg.text == "⬅️ السابق":
        if step > 0: await state.update_data(step=step-1); await send_step(msg, state)
        return
    
    try:
        val = float(msg.text)
        data['inputs'][config['professions'][prof]['inputs'][step]] = val
        if step + 1 < len(config['professions'][prof]['inputs']):
            await state.update_data(step=step+1); await send_step(msg, state)
        else:
            res = compute(config['professions'][prof]['formula'], data['inputs'])
            await msg.answer(f"✅ النتيجة النهائية: {res:.2f}", reply_markup=types.ReplyKeyboardRemove())
            await state.clear()
    except: await msg.answer("⚠️ يرجى إدخال رقم صحيح.")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
