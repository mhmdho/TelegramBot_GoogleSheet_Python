import telebot
import os
from Gsheet import spreadsheet


API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['friends'])
def names(message):
  names = message.text.split('\n')[1:]
  template_id = spreadsheet.worksheet("Template").id
  new_sheet_i = len(spreadsheet._spreadsheets_get()['sheets'])
  event = spreadsheet.duplicate_sheet(template_id, insert_sheet_index=new_sheet_i, new_sheet_name=names[0])
  i = 2
  for name in names[1:]:
    event.update_cell(i, 1, name)
    i += 1
  bot.reply_to(message, 'دورهمي جديد و اسامي دوستان ثبت شد')


@bot.message_handler(commands=['pay'])
def payment(message):
  event = message.text.split('\n')[1]
  user = message.text.split('\n')[2]
  payment = message.text.split('\n')[3]
  bot.send_message(message.chat.id, f'{user} paid {payment}$ for {event}')


@bot.message_handler(commands=['report'])
def get_report(message):
  response = ""
  title = 'Hangout'
  title = f"{title}\n\n"
  col = f"{'name' : <15}{'price' : ^11}{'paid' : >11}\n"
  name = 'Sara'
  price = '140'
  paid = True
  response = f"{name : <20}{price : ^12}{paid : >14}\n"
  data = title+col+response
  bot.send_message(message.chat.id, data)


def recieve_payment(message):
  payment = message.text.split('/')
  if len(payment) < 3:
    return False
  else:
    return True

@bot.message_handler(func=recieve_payment)
def record_payment(message):
  event = message.text.split('/')[0]
  user = message.text.split('/')[1]
  payment = message.text.split('/')[2]
  bot.send_message(message.chat.id, f'{user} paid {payment}$ for {event}')
  # bot.send_message(message.chat.id, f' مبلغ {payment} تومان توسط {user} بابت دورهمی {event} پرداخت شد')


bot.polling()
