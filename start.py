import telebot
from telebot import types

# ТОКЕН
API_TOKEN = '8550938957:AAEI8uSkNGckcvLFO-U1CRRXROXXHX8bgEI'
bot = telebot.TeleBot(API_TOKEN)

# ССЫЛКА НА KWORK
KWORK_LINK = 'https://kwork.com/user/todosanatolie990'

# Словарь с текстами (Оптимизация удалена)
strings = {
    'ru': {
        'welcome': "Выберите язык / Choose a language:",
        'main_text': "👋 Привет! Я бот-визитка v3x нолика.\nЧем могу помочь?",
        'btn_services': "🛠 IT Услуги (Python)",
        'btn_games': "🎮 Игры & Боты",
        'btn_price': "💰 Цены",
        'btn_order': "🚀 Заказать проект",
        'btn_back': "⬅️ Назад",
        'info_services': "Я создаю на Python:\n✅ Telegram ботов\n📊 Парсеры данных\n⚡ Скрипты автоматизации",
        'info_games': "Игры и спец. софт:\n🕹 Мини-игры на Pygame\n🤖 Боты для Discord\n⚙️ Игровые макросы",
        'info_price': "Цены начинаются от 500 руб ($5). Пишите — договоримся! 🤝"
    },
    'en': {
        'welcome': "Choose a language / Выберите язык:",
        'main_text': "👋 Hi! I'm v3x nolik's business card bot.\nHow can I help you?",
        'btn_services': "🛠 IT Services (Python)",
        'btn_games': "🎮 Games & Bots",
        'btn_price': "💰 Pricing",
        'btn_order': "🚀 Order a Project",
        'btn_back': "⬅️ Back",
        'info_services': "I develop using Python:\n✅ Telegram bots\n📊 Web scrapers\n⚡ Automation scripts",
        'info_games': "Games & Special Soft:\n🕹 Python games (Pygame)\n🤖 Discord bots\n⚙️ In-game scripts",
        'info_price': "Prices start from $5. Let's chat! 🤝"
    }
}

user_lang = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_ru = types.InlineKeyboardButton("Русский 🇷🇺", callback_data='set_ru')
    btn_en = types.InlineKeyboardButton("English 🇺🇸", callback_data='set_en')
    markup.add(btn_ru, btn_en)
    bot.send_message(message.chat.id, strings['ru']['welcome'], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    cid = call.message.chat.id
    mid = call.message.message_id

    if call.data.startswith('set_'):
        lang = call.data.split('_')[1]
        user_lang[cid] = lang
        show_main_menu(cid, mid, lang)

    elif call.data == 'main_menu':
        lang = user_lang.get(cid, 'ru')
        show_main_menu(cid, mid, lang)

    elif call.data in ['services', 'games', 'price']:
        lang = user_lang.get(cid, 'ru')
        if call.data == 'services': text = strings[lang]['info_services']
        elif call.data == 'games': text = strings[lang]['info_games']
        elif call.data == 'price': text = strings[lang]['info_price']
        show_submenu(cid, mid, text, lang)

def show_main_menu(cid, mid, lang):
    markup = types.InlineKeyboardMarkup(row_width=1) # Сделал кнопки в один столбец для красоты
    b1 = types.InlineKeyboardButton(strings[lang]['btn_services'], callback_data='services')
    b2 = types.InlineKeyboardButton(strings[lang]['btn_games'], callback_data='games')
    b3 = types.InlineKeyboardButton(strings[lang]['btn_price'], callback_data='price')
    b4 = types.InlineKeyboardButton(strings[lang]['btn_order'], url=KWORK_LINK)
    markup.add(b1, b2, b3, b4)
    bot.edit_message_text(chat_id=cid, message_id=mid, text=strings[lang]['main_text'], reply_markup=markup)

def show_submenu(cid, mid, text, lang):
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton(strings[lang]['btn_back'], callback_data='main_menu')
    markup.add(back)
    bot.edit_message_text(chat_id=cid, message_id=mid, text=text, reply_markup=markup)

print("Бот запущен! Оптимизация удалена, остались только Игры и Python.")
bot.infinity_polling()