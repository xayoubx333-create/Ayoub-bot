import telebot
from telebot import types
import time

# إعدادات أيوب النهائية
TOKEN = '8546862642:AAGdmdEkD3_hL-G8DUPGHviH49S3VFx8ORA'
ADMIN_ID = 7096534637 
bot = telebot.TeleBot(TOKEN)

# نصوص محمية باليونيكود لضمان عمل البوت 24 ساعة ومنع الخطأ في السطر 30
START_MSG = "Welcome to AyouBot!\n\u0645\u0631\u062d\u0628\u0627 \u0628\u0643 \u0641\u064a \u0639\u0627\u0626\u0644\u0629 ayoubot"

db = {} 
publics = []

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.chat.id
    if uid not in db:
        db[uid] = {'pts':0, 'user':'None', 't':0}
    bot.send_message(uid, START_MSG)

@bot.message_handler(func=lambda m: "tiktok.com" in m.text.lower())
def register(m):
    uid = m.chat.id
    user = m.text.split('@')[-1].split('?')[0] if '@' in m.text else "User"
    db[uid].update({'user': user})
    if (m.text, user) not in publics: publics.append((m.text, user))
    
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("\u062c\u0645\u0631 \u0646\u0642\u0627\u0637", "\u062d\u0633\u0627\u0628\u064a")
    bot.send_message(uid, f"Registered: @{user}", reply_markup=kb)

@bot.message_handler(func=lambda m: True)
def logic(m):
    uid = m.chat.id
    if m.text == "\u062c\u0645\u0631 \u0646\u0642\u0627\u0637":
        if not publics: return bot.send_message(uid, "Empty!")
        for l, u in publics[:3]:
            btn = types.InlineKeyboardMarkup()
            btn.add(types.InlineKeyboardButton(f"Follow @{u}", url=l))
            btn.add(types.InlineKeyboardButton("Verify (+5)", callback_data="chk"))
            bot.send_message(uid, f"Target: @{u}", reply_markup=btn)
        db[uid]['t'] = time.time()

@bot.callback_query_handler(func=lambda c: True)
def calls(c):
    uid = c.message.chat.id
    if c.data == "chk":
        if time.time() - db[uid].get('t', 0) < 12:
            bot.answer_callback_query(c.id, "Wait 12s!", show_alert=True)
        else:
            db[uid]['pts'] += 5
            bot.answer_callback_query(c.id, "Success +5")

bot.polling(none_stop=True)
  
