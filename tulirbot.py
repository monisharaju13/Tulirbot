import telepot
from telepot.loop import MessageLoop


# Replace this with your actual bot token
TOKEN = '7195574526:AAFXgLWPLkxGFE6ZlIeUI3sR8egG7TZMCBM'
# Replace this with the chat ID of the admin who should receive notifications
ADMIN_CHAT_ID = '984811254'

# Sample data for doctors and services
doctors = {
    'dr_karthick': 'Dr. Dr.Karthick Shanmugam - Podiatrist',
    'dr_elakkia': 'DR.R.Elakkiarani Karthick - Physician and Diabetologist',
    'dr_Prabhu': 'Dr.U.Prabhakaran - Surgical Oncology'
}

services = [
   'General Checkup',
    'Cardiology',
    'Podiatrist',
    'Surgical Oncology',
    'Radiology',
    'Emergency Services'
]

appointments = {}

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        command = msg['text'].lower()

        if command == '/start':
            bot.sendMessage(chat_id, 'Hello! Welcome to the Tulir Multispeciality Health Care Bot. Type /help to see available commands.')
        elif command == '/help':
            bot.sendMessage(chat_id, """
Available Commands:
/start - Start the bot
/help - Get help on using the bot
/info - Get information about the bot
/status - Get the current status of the bot
/time - Get the current time
/date - Get the current date
/appointment - Book an appointment
/doctors - Get information about doctors
/services - List available hospital services
/contact - Get hospital contact information
""")
        elif command == '/info':
            bot.sendMessage(chat_id, 'This bot is created to assist with our hospital-related inquiries and services.\n\nWe are dedicated to providing the highest quality healthcare services to our community. \n\n Our team of experienced doctors and healthcare professionals are here to ensure you receive the best care possible. \n\n Available in Salem and Erode districts.')
        elif command == '/status':
            bot.sendMessage(chat_id, 'The bot is currently running and operational. 24 hours servicess are available including weekends.')
        elif command == '/time':
            now = datetime.now().strftime('%H:%M:%S')
            bot.sendMessage(chat_id, f'The current time is: {now}')
        elif command == '/date':
            today = datetime.now().strftime('%Y-%m-%d')
            bot.sendMessage(chat_id, f'Today\'s date is: {today}')
        elif command == '/appointment':
            bot.sendMessage(chat_id, 'Please enter your name to book an appointment.')
            appointments[chat_id] = {}
            appointments[chat_id]['step'] = 'name'
        elif command == '/doctors':
            doc_info = "\n".join([f"{key}: {value}" for key, value in doctors.items()])
            bot.sendMessage(chat_id, f"Available Doctors:\n{doc_info}")
        elif command == '/services':
            services_info = "\n".join(services)
            bot.sendMessage(chat_id, f"Available Services:\n{services_info}")
        elif command == '/contact':
            bot.sendMessage(chat_id, 'Hospital Contact Information:\nPhone: +91 9789333979\nEmail: tulirfootcare@gmail.com\nAddress: Tulir Multispeciality Health Care, Pallipalayam-Kumarapalayam Rd, Vijaya Thottam, komarapalayam, Tamil Nadu-638183.')
        else:
            if chat_id in appointments:
                step = appointments[chat_id].get('step')
                if step == 'name':
                    appointments[chat_id]['name'] = msg['text']
                    bot.sendMessage(chat_id, 'Please enter the doctor you would like to book an appointment with (e.g., dr_karthick, dr_elakkia, dr_Prabhu).')
                    appointments[chat_id]['step'] = 'doctor'
                elif step == 'doctor':
                    doctor_key = msg['text']
                    if doctor_key in doctors:
                        appointments[chat_id]['doctor'] = doctors[doctor_key]
                        bot.sendMessage(chat_id, 'Please enter the desired appointment date (YYYY-MM-DD).')
                        appointments[chat_id]['step'] = 'date'
                    else:
                        bot.sendMessage(chat_id, 'Invalid doctor. Please enter a valid doctor key.')
                elif step == 'date':
                    appointments[chat_id]['date'] = msg['text']
                    name = appointments[chat_id]['name']
                    doctor = appointments[chat_id]['doctor']
                    date = appointments[chat_id]['date']
                    bot.sendMessage(chat_id, f'Appointment booked successfully!\n\nName: {name}\nDoctor: {doctor}\nDate: {date}')
                    
                    # Send notification to admin
                    bot.sendMessage(ADMIN_CHAT_ID, f'New appointment booked!\n\nName: {name}\nDoctor: {doctor}\nDate: {date}')
                    
                    # Clear the appointment data for the user
                    appointments.pop(chat_id)
            else:
                bot.sendMessage(chat_id, 'Sorry, I did not understand that command. Type /help to see available commands.')

bot = telepot.Bot(TOKEN)

MessageLoop(bot, handle).run_as_thread()

print('Bot is listening...')

# Keep the program running
import time
while 1:
    time.sleep(10)
