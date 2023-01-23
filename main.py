import telebot
import os
from Gsheet import spreadsheet


API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)


last_event = spreadsheet.worksheets()[-1].id
print(last_event)
event = spreadsheet.get_worksheet_by_id(last_event)


@bot.message_handler(commands=['friends'])
def names(message):
  names = message.text.split('\n')[1:]
  template_id = spreadsheet.worksheet("Template").id
  new_sheet_i = len(spreadsheet._spreadsheets_get()['sheets'])
  # new_sheet_i = len(spreadsheet.worksheets())
  global event
  event = spreadsheet.duplicate_sheet(template_id, insert_sheet_index=new_sheet_i, new_sheet_name=names[0])
  i = 2
  for name in names[1:]:
    event.update_cell(i, 1, name)
    event.update_cell(i, 2, 0)
    i += 1
  bot.reply_to(message, f'دورهمي ({names[0]}) و اسامي دوستان ثبت شد')


@bot.message_handler(commands=['pay'])
def payment(message):
  event = message.text.split('\n')[1]
  user = message.text.split('\n')[2]
  payment = message.text.split('\n')[3]
  bot.send_message(message.chat.id, f'{user} paid {payment}$ for {event}')
  # bot.send_message(message.chat.id, f' مبلغ {payment} تومان توسط {user} بابت دورهمی {event} پرداخت شد')


@bot.message_handler(commands=['report'])
def get_report(message):
  title = f"{event.title}\n\n"
  col = f"{'name' : <20}{'payment' : ^10}\n"
  response = ""
  i = 2
  while event.cell(i,1).value != None:
    response += f"{event.cell(i,1).value : <20}{event.cell(i,2).value : ^10}\n"
    print(response)
    i += 1
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
