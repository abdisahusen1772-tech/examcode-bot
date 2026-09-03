import os
import telebot
from dotenv import load_dotenv
from telebot import types
import sqlite3
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
ADMIN_CHAT_ID = 196911057  # Replace with actual admin Telegram ID

# Database Setup
def init_db():
    conn = sqlite3.connect('eca_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            reg_id TEXT PRIMARY KEY,
            telegram_id INTEGER,
            username TEXT,
            full_name TEXT,
            phone TEXT,
            email TEXT,
            level TEXT,
            course TEXT,
            reg_date TEXT,
            payment_status TEXT,
            enrollment_status TEXT,
            receipt_file_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Structured Courses Catalogue (Including Free Seminar)
courses = {
    "python": {
        "name": "🐍 Python Programming",
        "title": "🐍 INTRODUCTION TO PROGRAMMING — PYTHON",
        "fee": "500",
        "method": "Commercial Bank of Ethiopia OR Awash Bank",
        "account_name": "Abdisa Husein Fitesa",
        "account_number": "CBE: 1000744948782 | Awash: 014271368412700",
        "group_link": "https://t.me/+svtwNoJyh9RjMzc0",
        "desc": (
            "🚀 Want to learn how to code but don't know where to start?\n\n"
            "Start your programming journey with Python and learn how to think like a programmer, solve problems, and build your own programs.\n\n"
            "💡 WHAT YOU'LL LEARN:\n"
            "• Programming fundamentals\n• Python basics\n• Variables and data types\n• Conditions and loops\n• Functions\n• Problem-solving\n• Practical programming\n\n"
            "🎯 PERFECT FOR:\nBeginners and students with no programming experience.\n\n"
            "🔥 Start from zero. Build your skills. Create your own programs."
        ),
        "type": "paid"
    },
    "english": {
        "name": "🗣️ English Communication",
        "title": "🗣️ ENGLISH COMMUNICATION",
        "fee": "400",
        "method": "Commercial Bank of Ethiopia OR Awash Bank",
        "account_name": "Abdisa Husein Fitesa",
        "account_number": "CBE: 1000744948782 | Awash: 014271368412700",
        "group_link": "https://t.me/+0H2SiUZCikg1NDA0",
        "desc": (
            "🌍 English is more than a subject — it's a skill that opens doors.\n\n"
            "Improve your speaking, listening, vocabulary, grammar, and everyday communication through practical learning.\n\n"
            "💬 Build the confidence to communicate clearly at school, university, work, and in everyday life.\n\n"
            "🎯 PERFECT FOR:\nStudents who want stronger English and better communication skills.\n\n"
            "🔥 Learn English. Speak with confidence. Open more opportunities."
        ),
        "type": "paid"
    },
    "highschool": {
        "name": "📚 High School Study",
        "title": "📚 HIGH SCHOOL STUDY",
        "fee": "300",
        "method": "Commercial Bank of Ethiopia OR Awash Bank",
        "account_name": "Abdisa Husein Fitesa",
        "account_number": "CBE: 1000744948782 | Awash: 014271368412700",
        "group_link": "https://t.me/+jQAZHeavBQoyMjlk",
        "desc": (
            "🎯 Studying harder doesn't always mean studying better.\n\n"
            "Learn effective study strategies, time management, note-taking, exam preparation, and techniques for understanding difficult subjects.\n\n"
            "🧠 Discover how to study smarter, stay focused, and prepare yourself for important exams.\n\n"
            "🎯 PERFECT FOR:\nHigh school students who want to improve their academic performance.\n\n"
            "🔥 Study smarter. Prepare better. Achieve more."
        ),
        "type": "paid"
    },
    "scholarship": {
        "name": "🎓 Scholarship Guides",
        "title": "🎓 SCHOLARSHIP GUIDES",
        "fee": "450",
        "method": "Commercial Bank of Ethiopia OR Awash Bank",
        "account_name": "Abdisa Husein Fitesa",
        "account_number": "CBE: 1000744948782 | Awash: 014271368412700",
        "group_link": "https://t.me/+W03ZTItiC3hkZjg0",
        "desc": (
            "✈️ Dreaming of studying abroad but don't know where to begin?\n\n"
            "Learn how to discover scholarship opportunities, understand requirements, prepare your documents, write strong motivation letters, and avoid common application mistakes.\n\n"
            "🌍 Turn scholarship opportunities into realistic applications with a clear step-by-step approach.\n\n"
            "🎯 PERFECT FOR:\nStudents looking for local or international scholarship opportunities.\n\n"
            "🔥 Find opportunities. Build a stronger application. Move closer to your dream."
        ),
        "type": "paid"
    },
    "seminar": {
        "name": "🎟️ Free Seminar",
        "title": "🎟️ FREE SEMINAR",
        "fee": "0",
        "method": "None",
        "account_name": "None",
        "account_number": "None",
        "group_link": "https://t.me/+b6J28nCe17U3ZWU0",
        "desc": (
            "🎉 Join our exclusive free seminar to jumpstart your academic and professional journey!\n\n"
            "💡 WHAT YOU'LL LEARN:\n"
            "• Overview of tech and language careers\n"
            "• Roadmap for Exam Code Academy courses\n"
            "• Q&A session with instructors\n\n"
            "🎯 PERFECT FOR:\nAll students eager to learn and explore new opportunities.\n\n"
            "🔥 100% Free! Reserve your spot now."
        ),
        "type": "free"
    }
}

temp_reg = {}

def main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📚 Courses", "📝 Register")
    markup.add("📋 My Registration", "📢 Announcements")
    markup.add("ℹ️ About Us", "❓ Help")
    markup.add("📞 Contact")
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🎓 WELCOME TO EXAM CODE ACADEMY! 🚀\n\n"
        "Hello and welcome! 👋\n\n"
        "We're here to help you learn new skills, improve your academic performance, "
        "communicate with confidence, and discover opportunities for your future.\n\n"
        "📚 What can you learn here?\n\n"
        "🐍 Python Programming\n"
        "🗣️ English Communication\n"
        "📚 High School Study\n"
        "🎓 Scholarship Guides\n"
        "🎟️ Free Seminar\n\n"
        "✨ Your future starts with what you learn today.\n\n"
        "👇 Choose an option below to get started!"
    )
    try:
        bot.send_photo(
            message.chat.id,
            "https://images.unsplash.com/photo-1523240795612-9a054b0db644",
            caption=welcome_text,
            reply_markup=main_menu_markup()
        )
    except:
        bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_markup())

@bot.message_handler(func=lambda msg: msg.text in ["📚 Courses", "📝 Register"])
def handle_menu_actions(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, c in courses.items():
        markup.add(types.InlineKeyboardButton(c['name'], callback_data=f"course_menu_{key}"))
    
    if message.text == "📚 Courses":
        bot.send_message(
            message.chat.id,
            "📚 OUR COURSES\n\nChoose a course that interests you and discover what you can learn.\n\n🚀 Your next skill could change your future.",
            reply_markup=markup
        )
    else:
        bot.send_message(
            message.chat.id,
            "📝 COURSE REGISTRATION\n\nWelcome to the registration process! 🎓\nPlease follow the steps carefully and provide accurate information.\n\nFirst, choose the course you want to register for:",
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('course_menu_'))
def course_menu_click(call):
    c_key = call.data.split('_')[2]
    c = courses[c_key]
    
    text = f"{c['title']}\n\n{c['desc']}\n\n💰 Course Fee: {c['fee']} ETB"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📝 Register Now", callback_data=f"reg_start_{c_key}"))
    markup.add(types.InlineKeyboardButton("🔙 Back to Courses", callback_data="back_courses"))
    
    bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'back_courses')
def back_to_courses(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, c in courses.items():
        markup.add(types.InlineKeyboardButton(c['name'], callback_data=f"course_menu_{key}"))
    bot.edit_message_text("📚 OUR COURSES\n\nChoose a course below:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('reg_start_'))
def start_reg_flow(call):
    c_key = call.data.split('_')[2]
    user_id = call.from_user.id
    temp_reg[user_id] = {"course": c_key}
    
    msg = bot.send_message(call.message.chat.id, "👤 Please enter your full name.")
    bot.register_next_step_handler(msg, process_name)

def process_name(message):
    user_id = message.from_user.id
    if user_id not in temp_reg:
        return
    temp_reg[user_id]["full_name"] = message.text
    
    msg = bot.send_message(message.chat.id, "📱 Please enter your phone number or share your Telegram contact.")
    bot.register_next_step_handler(msg, process_phone)

def process_phone(message):
    user_id = message.from_user.id
    if user_id not in temp_reg:
        return
    temp_reg[user_id]["phone"] = message.text
    
    msg = bot.send_message(message.chat.id, "📧 Please enter your email address.")
    bot.register_next_step_handler(msg, process_email)

def process_email(message):
    user_id = message.from_user.id
    if user_id not in temp_reg:
        return
    temp_reg[user_id]["email"] = message.text
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("High School", "University", "Beginner", "Other")
    msg = bot.send_message(message.chat.id, "🎓 Please select your current level:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_level)

def process_level(message):
    user_id = message.from_user.id
    if user_id not in temp_reg:
        return
    temp_reg[user_id]["level"] = message.text
    
    reg = temp_reg[user_id]
    c_name = courses[reg["course"]]["name"]
    
    summary_text = (
        "📋 PLEASE CHECK YOUR INFORMATION\n\n"
        f"👤 Name: {reg['full_name']}\n"
        f"📱 Phone: {reg['phone']}\n"
        f"📧 Email: {reg['email']}\n"
        f"📚 Course: {c_name}\n"
        f"🎓 Level: {reg['level']}\n\n"
        "Is all the information correct?"
    )
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Confirm", callback_data="confirm_reg"),
        types.InlineKeyboardButton("❌ Cancel", callback_data="cancel_reg")
    )
    bot.send_message(message.chat.id, summary_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['confirm_reg', 'cancel_reg'])
def confirm_or_cancel(call):
    user_id = call.from_user.id
    if call.data == 'cancel_reg':
        if user_id in temp_reg:
            del temp_reg[user_id]
        bot.edit_message_text("❌ Registration cancelled.", chat_id=call.message.chat.id, message_id=call.message.message_id)
        return
        
    if user_id not in temp_reg:
        bot.answer_callback_query(call.id, "Session expired. Please start again.")
        return
        
    reg = temp_reg[user_id]
    c = courses[reg["course"]]
    reg_id = f"ECA-{int(datetime.now().timestamp()) % 100000:05d}"
    reg["reg_id"] = reg_id
    reg["reg_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    reg["username"] = call.from_user.username or "None"
    reg["telegram_id"] = user_id
    
    if c["type"] == "free":
        reg["payment_status"] = "Verified (Free)"
        reg["enrollment_status"] = "Enrolled"
        
        conn = sqlite3.connect('eca_bot.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO registrations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            reg_id, user_id, reg["username"], reg["full_name"], reg["phone"], 
            reg["email"], reg["level"], c["name"], reg["reg_date"], 
            reg["payment_status"], reg["enrollment_status"], "NONE"
        ))
        conn.commit()
        conn.close()
        
        success_text = (
            "🎉 REGISTRATION APPROVED!\n\n"
            "Congratulations! 🎉\n"
            "Your free seminar registration is confirmed.\n\n"
            f"📚 Course: {c['name']}\n"
            f"🆔 Registration ID: {reg_id}\n"
            "💰 Payment: ✅ FREE\n"
            "🎓 Enrollment: ✅ CONFIRMED\n\n"
            "You are eligible to join the seminar group:\n"
            f"🔐 [Click Here to Join Group]({c['group_link']})"
        )
        bot.edit_message_text(success_text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown", disable_web_page_preview=True)
        del temp_reg[user_id]
    else:
        reg["payment_status"] = "Pending"
        reg["enrollment_status"] = "Pending"
        
        payment_text = (
            "💳 PAYMENT INSTRUCTIONS\n\n"
            "Your registration information has been received.\n"
            "To complete your registration, please make the required payment.\n\n"
            f"📚 Course:\n{c['name']}\n\n"
            f"💰 Amount:\n{c['fee']} ETB\n\n"
            "💳 PAYMENT METHODS:\n\n"
            "🏦 Commercial Bank of Ethiopia (CBE)\n"
            "Account Name: Abdisa Husein Fitesa\n"
            "Account Number: 1000744948782\n\n"
            "🏦 Awash Bank\n"
            "Account Name: Abdisa Husein Fitesa\n"
            "Account Number: 014271368412700\n\n"
            "After making the payment, take a clear screenshot of your transaction receipt and click below to submit."
        )
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📸 Submit Receipt", callback_data=f"submit_rcpt_{reg_id}"))
        markup.add(types.InlineKeyboardButton("❌ Cancel Registration", callback_data="cancel_reg"))
        
        bot.edit_message_text(payment_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('submit_rcpt_'))
def prompt_receipt_upload(call):
    user_id = call.from_user.id
    if user_id not in temp_reg:
        bot.answer_callback_query(call.id, "Session expired. Please restart registration.")
        return
    
    msg = bot.send_message(
        call.message.chat.id,
        "📸 PAYMENT RECEIPT\n\nPlease send a clear screenshot of your payment transaction showing:\n"
        "✓ Transaction reference\n✓ Amount paid\n✓ Date/time\n\nSend the screenshot now."
    )
    bot.register_next_step_handler(msg, handle_receipt_upload)

def handle_receipt_upload(message):
    user_id = message.from_user.id

    if user_id not in temp_reg:
        bot.send_message(message.chat.id, "Session error. Please use /start to restart.")
        return

    if not message.photo:
        msg = bot.send_message(
            message.chat.id,
            "⚠️ Please send an image screenshot of your receipt."
        )
        bot.register_next_step_handler(msg, handle_receipt_upload)
        return

    file_id = message.photo[-1].file_id
    reg = temp_reg[user_id]
    reg["receipt_file_id"] = file_id

    conn = sqlite3.connect('eca_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO registrations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        reg["reg_id"], user_id, reg["username"], reg["full_name"], reg["phone"],
        reg["email"], reg["level"], courses[reg["course"]]["name"], reg["reg_date"],
        "Under Verification", "Pending", file_id
    ))
    conn.commit()
    conn.close()

    bot.send_message(
        message.chat.id,
        f"📸 RECEIPT RECEIVED!\n\n"
        f"Your payment receipt has been submitted successfully.\n\n"
        f"⏳ STATUS: WAITING FOR VERIFICATION\n"
        f"Our team will review your payment.\n\n"
        f"🆔 Registration ID: {reg['reg_id']}"
    )

    admin_text = (
        "🔔 NEW PAYMENT RECEIPT — ACTION REQUIRED\n\n"
        f"🆔 Registration ID: {reg['reg_id']}\n"
        f"👤 Student: {reg['full_name']}\n"
        f"📱 Phone: {reg['phone']}\n"
        f"📧 Email: {reg['email']}\n"
        f"👤 Telegram: @{reg['username'] if reg['username'] != 'None' else 'No username'}\n"
        f"📚 Course: {courses[reg['course']]['name']}\n"
        f"🎓 Level: {reg['level']}\n"
        f"📅 Date: {reg['reg_date']}\n\n"
        "💳 Payment status: Under Verification\n\n"
        "Please check the attached payment screenshot and choose an action."
    )

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(
            "✅ ACCEPT / APPROVE",
            callback_data=f"adm_approve_{reg['reg_id']}"
        ),
        types.InlineKeyboardButton(
            "❌ REJECT",
            callback_data=f"adm_reject_{reg['reg_id']}"
        )
    )

    try:
        bot.send_photo(
            ADMIN_CHAT_ID,
            file_id,
            caption=admin_text,
            reply_markup=markup
        )
    except Exception as e:
        try:
            bot.send_message(
                ADMIN_CHAT_ID,
                f"⚠️ Receipt image notification failed, but the registration was saved.\n\n"
                f"{admin_text}\n\nTechnical error: {e}"
            )
        except Exception:
            print(f"ADMIN NOTIFICATION ERROR: {e}")

    del temp_reg[user_id]

@bot.callback_query_handler(func=lambda call: call.data.startswith('adm_approve_') or call.data.startswith('adm_reject_'))
def admin_verification_action(call):
    parts = call.data.split('_')
    action, reg_id = parts[1], parts[2]
    
    conn = sqlite3.connect('eca_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT telegram_id, course FROM registrations WHERE reg_id = ?', (reg_id,))
    row = cursor.fetchone()
    
    if not row:
        bot.answer_callback_query(call.id, "Registration record not found.")
        conn.close()
        return
        
    student_telegram_id, course_name = row[0], row[1]
    
    # Find matching course group link
    group_link = "https://t.me/+exam_code_academy_group"
    for k, c in courses.items():
        if c["name"] == course_name:
            group_link = c["group_link"]
            break
            
    if action == 'approve':
        cursor.execute('UPDATE registrations SET payment_status = "Verified", enrollment_status = "Enrolled" WHERE reg_id = ?', (reg_id,))
        conn.commit()
        conn.close()
        
        try:
            bot.edit_message_caption("✅ APPROVED BY ADMIN", chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        
        student_msg = (
            "🎉 REGISTRATION APPROVED!\n\n"
            "Congratulations! 🎉\n"
            "Your payment has been successfully verified.\n\n"
            f"📚 Course:\n{course_name}\n\n"
            f"🆔 Registration ID:\n{reg_id}\n\n"
            "💰 Payment:\n✅ VERIFIED\n\n"
            "🎓 Enrollment:\n✅ CONFIRMED\n\n"
            "You are now eligible to join the premium course group.\n\n"
            f"🔐 [Click Here to Join Private Group]({group_link})"
        )
        bot.send_message(student_telegram_id, student_msg, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        cursor.execute('UPDATE registrations SET payment_status = "Rejected", enrollment_status = "Rejected" WHERE reg_id = ?', (reg_id,))
        conn.commit()
        conn.close()
        
        try:
            bot.edit_message_caption("❌ REJECTED BY ADMIN", chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        
        student_msg = (
            "❌ PAYMENT NOT VERIFIED\n\n"
            "Unfortunately, we could not verify your payment receipt.\n"
            "Possible reasons:\n• Incorrect amount\n• Unclear receipt\n• Invalid transaction\n\n"
            "Please check your payment information and contact support or restart registration."
        )
        bot.send_message(student_telegram_id, student_msg)
    
    decision_text = (
        "📢 REGISTRATION DECISION COMPLETED\n\n"
        f"🆔 Registration ID: {reg_id}\n"
        f"📚 Course: {course_name}\n"
        f"👤 Student Telegram ID: {student_telegram_id}\n"
        f"📌 Decision: {'✅ ACCEPTED / APPROVED' if action == 'approve' else '❌ REJECTED'}"
    )
    try:
        bot.send_message(ADMIN_CHAT_ID, decision_text)
    except Exception as e:
        print(f"OWNER DECISION NOTIFICATION ERROR: {e}")

    bot.answer_callback_query(call.id, f"Action '{action}' processed successfully.")

@bot.message_handler(func=lambda msg: msg.text == "📋 My Registration")
def my_registration(message):
    conn = sqlite3.connect('eca_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT reg_id, full_name, course, payment_status, enrollment_status, reg_date FROM registrations WHERE telegram_id = ?', (message.from_user.id,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        bot.send_message(message.chat.id, "📋 You have no active registrations found. Click '📝 Register' to join a course.")
        return
        
    for r in rows:
        text = (
            "📋 MY REGISTRATION\n\n"
            f"🆔 Registration ID:\n{r[0]}\n\n"
            f"👤 Name:\n{r[1]}\n\n"
            f"📚 Course:\n{r[2]}\n\n"
            f"💰 Payment Status:\n{r[3]}\n\n"
            f"🎓 Enrollment Status:\n{r[4]}\n\n"
            f"📅 Date:\n{r[5]}"
        )
        bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda msg: msg.text == "📢 Announcements")
def announcements(message):
    bot.send_message(
        message.chat.id,
        "📢 ANNOUNCEMENTS\n\nStay updated with:\n• Course updates\n• Class schedules\n• Exam information\n• Scholarship opportunities\n\n"
        "🔔 *Welcome to Exam Code Academy! All upcoming class schedules will be posted here.*",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda msg: msg.text == "ℹ️ About Us")
def about_us(message):
    text = (
        "🎓 ABOUT EXAM CODE ACADEMY\n\n"
        "Welcome to Exam Code Academy! 🚀\n\n"
        "Our goal is to help students develop practical skills, improve academically, communicate confidently, and discover opportunities for their future.\n\n"
        "📚 OUR COURSES:\n"
        "🐍 Programming\n"
        "🗣️ English Communication\n"
        "📚 Academic Success\n"
        "🎓 Scholarship Opportunities\n\n"
        "💡 Learn today.\n🚀 Grow tomorrow.\n🌍 Build your future.\n\n"
        "Thank you for choosing Exam Code Academy! ❤️"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda msg: msg.text == "❓ Help")
def help_menu(message):
    text = (
        "❓ HOW CAN WE HELP?\n\n"
        "📚 Courses: Explore available courses and descriptions.\n"
        "📝 Registration: Choose a course and complete your form.\n"
        "💳 Payment: Follow bank payment instructions.\n"
        "📸 Receipt: Submit your transaction screenshot.\n"
        "⏳ Verification: Wait for manual admin review.\n"
        "🎉 Enrollment: Receive secure private group access."
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda msg: msg.text == "📞 Contact")
def contact_menu(message):
    text = (
        "📞 CONTACT EXAM CODE ACADEMY\n\n"
        "Need help with registration, payment, or your course? We're here to help! 🤝\n\n"
        "📩 Telegram: @Examcodeet\n"
        "📧 Email: support@examcodeacademy.com\n"
        "⏰ Support Hours: Monday – Saturday (2:00 Local Time - 11:00 Local Time)\n\n"
        "Please include your Registration ID when asking about an existing registration."
    )
    bot.send_message(message.chat.id, text)

print("Exam Code Academy Interactive Bot is running...")
bot.infinity_polling()
from flask import Flask
import threading
import os

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

t = threading.Thread(target=run)
t.start()