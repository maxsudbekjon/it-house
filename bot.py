import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters, ConversationHandler
from datetime import datetime
import json
import os

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# States
LANG_SELECT, MAIN_MENU, TRACK_INPUT, COMPLAINT_INPUT, ADMIN_FLIGHT, ADMIN_TRACK, ADMIN_EDIT_ABOUT, ADMIN_EDIT_PRICE, ADMIN_EDIT_ADDRESS = range(9)

# Data files
DATA_FILE = 'bot_data.json'
TRACKS_FILE = 'tracks.json'

# Default texts
DEFAULT_DATA = {
    'about_uz': 'Biz Xitoydan yuklarni O\'zbekistonga yetkazib berish xizmatini ko\'rsatamiz. Tez, ishonchli va xavfsiz.',
    'about_ru': 'Мы доставляем грузы из Китая в Узбекистан. Быстро, надежно и безопасно.',
    'prices_uz': '🚗 Avto: 6$ kg\n✈️ Avia: 9$ kg',
    'prices_ru': '🚗 Авто: 6$ кг\n✈️ Авиа: 9$ кг',
    'address': 'https://maps.google.com/?q=41.2995,69.2401',
    'admin_username': '@admin',
    'admins': [],
    'channel': None
}

# Load/Save data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_DATA.copy()

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_tracks():
    if os.path.exists(TRACKS_FILE):
        with open(TRACKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_tracks(tracks):
    with open(TRACKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tracks, f, ensure_ascii=False, indent=2)

bot_data = load_data()
tracks_data = load_tracks()
user_languages = {}

# Texts
texts = {
    'uz': {
        'welcome': '🇺🇿 Xush kelibsiz!\n\nTilni tanlang:',
        'main_menu': '📋 Asosiy menyu',
        'id_get': '🆔 ID olish',
        'about': 'ℹ️ Biz haqimizda',
        'track': '📦 Trek kod tekshirish',
        'complaint': '📝 Shikoyat yuborish',
        'prices': '💰 Narxlar',
        'address': '📍 Manzil',
        'yuan': '💴 Yuan',
        'id_text': f'Hurmatli foydalanuvchi!\n\nID olish uchun adminimiz bilan bog\'laning:\n{bot_data["admin_username"]}',
        'track_input': 'Trek kodni kiriting:',
        'track_error': '❌ Trek kodda xatolik bor yoki manzilga hali kelmagan.',
        'complaint_input': 'Shikoyatingizni yuboring, men uni adminga yuboraman:',
        'complaint_sent': '✅ Shikoyatingiz adminga yuborildi!',
        'yuan_text': f'💴 Yuan haqida ma\'lumot olish uchun admin bilan bog\'laning:\n{bot_data["admin_username"]}',
        'back': '🔙 Orqaga'
    },
    'ru': {
        'welcome': '🇷🇺 Добро пожаловать!\n\nВыберите язык:',
        'main_menu': '📋 Главное меню',
        'id_get': '🆔 Получить ID',
        'about': 'ℹ️ О нас',
        'track': '📦 Проверить трек-код',
        'complaint': '📝 Отправить жалобу',
        'prices': '💰 Цены',
        'address': '📍 Адрес',
        'yuan': '💴 Юань',
        'id_text': f'Уважаемый пользователь!\n\nДля получения ID свяжитесь с нашим админом:\n{bot_data["admin_username"]}',
        'track_input': 'Введите трек-код:',
        'track_error': '❌ Ошибка в трек-коде или груз еще не прибыл.',
        'complaint_input': 'Отправьте вашу жалобу, я передам ее админу:',
        'complaint_sent': '✅ Ваша жалоба отправлена админу!',
        'yuan_text': f'💴 Для информации о юане свяжитесь с админом:\n{bot_data["admin_username"]}',
        'back': '🔙 Назад'
    }
}

# Keyboards
def get_lang_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇺🇿 O'zbek", callback_data='lang_uz')],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')]
    ])

def get_main_keyboard(lang):
    t = texts[lang]
    keyboard = [
        [t['id_get'], t['about']],
        [t['track'], t['complaint']],
        [t['prices'], t['address']],
        [t['yuan']]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_admin_keyboard():
    keyboard = [
        ['➕ Trek kod qo\'shish', '🗑 Trek kod o\'chirish'],
        ['📊 Statistika', '📢 Kanal ulash'],
        ['👤 Admin qo\'shish', 'ℹ️ Biz haqimizda'],
        ['💰 Narxlar', '📍 Manzil']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Check channel membership if channel is set
    if bot_data.get('channel'):
        try:
            member = await context.bot.get_chat_member(bot_data['channel'], user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                await update.message.reply_text(
                    f"❌ Botdan foydalanish uchun kanalimizga a'zo bo'ling:\n{bot_data['channel']}",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📢 Kanalga o'tish", url=bot_data['channel'])]])
                )
                return ConversationHandler.END
        except:
            pass
    
    if user_id in bot_data['admins']:
        await update.message.reply_text('🔧 Admin Panel', reply_markup=get_admin_keyboard())
        return MAIN_MENU
    
    await update.message.reply_text(texts['uz']['welcome'], reply_markup=get_lang_keyboard())
    return LANG_SELECT

async def lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    lang = query.data.split('_')[1]
    user_languages[query.from_user.id] = lang
    
    t = texts[lang]
    await query.edit_message_text(t['main_menu'])
    await query.message.reply_text(t['main_menu'], reply_markup=get_main_keyboard(lang))
    
    return MAIN_MENU

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    # Admin commands
    if user_id in bot_data['admins']:
        if text == '➕ Trek kod qo\'shish':
            await update.message.reply_text('Reys raqamini kiriting:')
            return ADMIN_FLIGHT
        elif text == '🗑 Trek kod o\'chirish':
            await update.message.reply_text('O\'chirish uchun reys raqamini kiriting:')
            context.user_data['admin_action'] = 'delete'
            return ADMIN_FLIGHT
        elif text == '📊 Statistika':
            total_users = len(user_languages)
            total_tracks = len(tracks_data)
            stats = f"📊 Statistika:\n\n👥 Foydalanuvchilar: {total_users}\n📦 Trek kodlar: {total_tracks}"
            await update.message.reply_text(stats)
            return MAIN_MENU
        elif text == '📢 Kanal ulash':
            await update.message.reply_text('Kanal username yoki ID kiriting (masalan: @channel yoki -100123456):')
            context.user_data['admin_action'] = 'set_channel'
            return ADMIN_FLIGHT
        elif text == '👤 Admin qo\'shish':
            await update.message.reply_text('Admin ID raqamini kiriting:')
            context.user_data['admin_action'] = 'add_admin'
            return ADMIN_FLIGHT
        elif text == 'ℹ️ Biz haqimizda':
            current = f"🇺🇿 Hozirgi matn (UZ):\n{bot_data['about_uz']}\n\n🇷🇺 Текущий текст (RU):\n{bot_data['about_ru']}\n\nYangi matnni kiriting (UZ|RU formatida):"
            await update.message.reply_text(current)
            return ADMIN_EDIT_ABOUT
        elif text == '💰 Narxlar':
            current = f"Hozirgi narxlar:\n\n🇺🇿 {bot_data['prices_uz']}\n\n🇷🇺 {bot_data['prices_ru']}\n\nYangi narxlarni kiriting (UZ|RU formatida):"
            await update.message.reply_text(current)
            return ADMIN_EDIT_PRICE
        elif text == '📍 Manzil':
            current = f"Hozirgi manzil: {bot_data['address']}\n\nYangi Google Maps linkini kiriting:"
            await update.message.reply_text(current)
            return ADMIN_EDIT_ADDRESS
    
    # User commands
    lang = user_languages.get(user_id, 'uz')
    t = texts[lang]
    
    if text == t['id_get']:
        await update.message.reply_text(t['id_text'])
    elif text == t['about']:
        about_text = bot_data[f'about_{lang}']
        await update.message.reply_text(about_text)
    elif text == t['track']:
        await update.message.reply_text(t['track_input'])
        return TRACK_INPUT
    elif text == t['complaint']:
        await update.message.reply_text(t['complaint_input'])
        return COMPLAINT_INPUT
    elif text == t['prices']:
        prices_text = bot_data[f'prices_{lang}']
        await update.message.reply_text(prices_text)
    elif text == t['address']:
        await update.message.reply_text(f"📍 Bizning manzilimiz:", disable_web_page_preview=False)
        await update.message.reply_location(latitude=41.2995, longitude=69.2401)
    elif text == t['yuan']:
        await update.message.reply_text(t['yuan_text'])
    
    return MAIN_MENU

async def admin_flight_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    flight = update.message.text
    action = context.user_data.get('admin_action', 'add')
    
    if action == 'delete':
        if flight in tracks_data:
            del tracks_data[flight]
            save_tracks(tracks_data)
            await update.message.reply_text(f'✅ Reys {flight} o\'chirildi!')
        else:
            await update.message.reply_text('❌ Bunday reys topilmadi!')
        return MAIN_MENU
    elif action == 'set_channel':
        bot_data['channel'] = flight
        save_data(bot_data)
        await update.message.reply_text(f'✅ Kanal ulandi: {flight}')
        return MAIN_MENU
    elif action == 'add_admin':
        try:
            admin_id = int(flight)
            if admin_id not in bot_data['admins']:
                bot_data['admins'].append(admin_id)
                save_data(bot_data)
                await update.message.reply_text(f'✅ Admin qo\'shildi: {admin_id}')
            else:
                await update.message.reply_text('❌ Bu ID allaqachon admin!')
        except:
            await update.message.reply_text('❌ Xato ID format!')
        return MAIN_MENU
    
    context.user_data['flight'] = flight
    await update.message.reply_text(f'Reys: {flight}\n\nEndi trek kodlarni kiriting (har bir trek kod yangi qatorda):')
    return ADMIN_TRACK

async def admin_track_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    flight = context.user_data.get('flight')
    track_codes = update.message.text.strip().split('\n')
    
    added_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    for track in track_codes:
        track = track.strip()
        if track:
            tracks_data[track] = {
                'flight': flight,
                'status': 'Yo\'lda',
                'added': added_time
            }
    
    save_tracks(tracks_data)
    await update.message.reply_text(f'✅ {len(track_codes)} ta trek kod qo\'shildi!', reply_markup=get_admin_keyboard())
    return MAIN_MENU

async def track_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_code = update.message.text.strip()
    user_id = update.effective_user.id
    lang = user_languages.get(user_id, 'uz')
    t = texts[lang]
    
    if track_code in tracks_data:
        info = tracks_data[track_code]
        message = f"📦 Trek kod: {track_code}\n✈️ Reys: {info['flight']}\n📍 Holat: {info['status']}\n🕐 Qo'shilgan: {info['added']}"
        await update.message.reply_text(message)
    else:
        await update.message.reply_text(t['track_error'])
    
    await update.message.reply_text(t['main_menu'], reply_markup=get_main_keyboard(lang))
    return MAIN_MENU

async def complaint_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_languages.get(user_id, 'uz')
    t = texts[lang]
    complaint = update.message.text
    
    # Send to all admins
    for admin_id in bot_data['admins']:
        try:
            await context.bot.send_message(
                admin_id,
                f"📝 Yangi shikoyat:\n\nUser ID: {user_id}\nMatn: {complaint}",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Javob berish", callback_data=f"reply_{user_id}")]])
            )
        except:
            pass
    
    await update.message.reply_text(t['complaint_sent'])
    await update.message.reply_text(t['main_menu'], reply_markup=get_main_keyboard(lang))
    return MAIN_MENU

async def admin_edit_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    parts = text.split('|')
    if len(parts) == 2:
        bot_data['about_uz'] = parts[0].strip()
        bot_data['about_ru'] = parts[1].strip()
        save_data(bot_data)
        await update.message.reply_text('✅ Matn yangilandi!', reply_markup=get_admin_keyboard())
    else:
        await update.message.reply_text('❌ Format xato! UZ|RU formatida kiriting.')
    return MAIN_MENU

async def admin_edit_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    parts = text.split('|')
    if len(parts) == 2:
        bot_data['prices_uz'] = parts[0].strip()
        bot_data['prices_ru'] = parts[1].strip()
        save_data(bot_data)
        await update.message.reply_text('✅ Narxlar yangilandi!', reply_markup=get_admin_keyboard())
    else:
        await update.message.reply_text('❌ Format xato! UZ|RU formatida kiriting.')
    return MAIN_MENU

async def admin_edit_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = update.message.text.strip()
    bot_data['address'] = address
    save_data(bot_data)
    await update.message.reply_text('✅ Manzil yangilandi!', reply_markup=get_admin_keyboard())
    return MAIN_MENU

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in bot_data['admins']:
        await update.message.reply_text('Bekor qilindi', reply_markup=get_admin_keyboard())
    else:
        lang = user_languages.get(user_id, 'uz')
        await update.message.reply_text('Bekor qilindi', reply_markup=get_main_keyboard(lang))
    return MAIN_MENU

def main():
    TOKEN = '8282184612:AAGc0QCUpyD21zGRM9QPmo9F6juzCaSrxi8'
    
    app = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANG_SELECT: [CallbackQueryHandler(lang_callback)],
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler)],
            ADMIN_FLIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_flight_handler)],
            ADMIN_TRACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_track_handler)],
            TRACK_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, track_input_handler)],
            COMPLAINT_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, complaint_handler)],
            ADMIN_EDIT_ABOUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_edit_about)],
            ADMIN_EDIT_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_edit_price)],
            ADMIN_EDIT_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_edit_address)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    app.add_handler(conv_handler)
    
    print('Bot ishga tushdi...')
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    # Set first admin ID here
    bot_data['admins'] = []  # O'zingizning Telegram ID raqamingizni kiriting
    save_data(bot_data)
    main()