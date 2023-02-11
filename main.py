import telebot
import os
from Gsheet import spreadsheet

API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)

event = spreadsheet.worksheets()[-1]


def auth(id):
  if id == int(event.cell(1, 3).value):
    return True


@bot.message_handler(commands=['friends'])
def names(message):
  names = message.text.split('\n')[1:]
  template_id = spreadsheet.worksheet("Template").id
  new_sheet_i = len(spreadsheet.worksheets())
  global event
  event = spreadsheet.duplicate_sheet(template_id,
                                      insert_sheet_index=new_sheet_i,
                                      new_sheet_name=names[0])
  i = 2
  for name in names[1:]:
    event.update_cell(i, 1, name.strip())
    event.update_cell(i, 2, 0)
    i += 1
  event.update_cell(1, 3, message.chat.id)
  bot.reply_to(message, f'دورهمي ({names[0]}) و اسامي دوستان ثبت شد')


@bot.message_handler(commands=['addfriends'])
def add_names(message):
  names = message.text.split('\n')[1:]
  event = spreadsheet.worksheet(names[0].strip())
  old_names = event.col_values(1)
  i = len(old_names) + 1
  for name in names[1:]:
    name = name.strip()
    if name not in old_names:
      event.update_cell(i, 1, name)
      event.update_cell(i, 2, 0)
      i += 1
  bot.reply_to(message, f'در دورهمي ({names[0]}) اسامي جديد ثبت شد')


@bot.message_handler(commands=['pay'])
def payment(message):
  event_name = message.text.split('\n')[1].strip()
  user = message.text.split('\n')[2].strip()
  pay = message.text.split('\n')[3].strip()
  i = 2
  while event.cell(i, 1).value != None:
    if event.cell(i, 1).value == user:
      event.update_cell(i, 2, pay)
      bot.send_message(
        message.chat.id,
        f' مبلغ {pay} تومان توسط {user} بابت {event_name} پرداخت شد')
        # f'{user} paid {pay}$ for {event}')
      break
    i += 1
  else:
    bot.send_message(message.chat.id,
                     f'اين نام ({user}) در اين دورهمي ثبت نشده است')


@bot.message_handler(commands=['report'])
def get_report(message):
  if auth(message.chat.id):
    names = event.col_values(1)
    payments = event.col_values(2)
    title = f"{event.title}\n\n"
    title2 = f"\n[مبالغ واريز شده]"
    title3 = f"\n\n\n[مانده واريزي ها]"
    footer = f"\n\n مانده واريز نشده: {event.cell(2, 6).value}"
    card = f"{event.cell(4, 6).value}\n{event.cell(5, 6).value}"
    bill = f"{event.cell(4, 5).value}\n{event.cell(5, 5).value}"
    seperator = "\n"+"-\t"*33+"\n"
    response = f"{names[0] : <20}{payments[0] : >30}\n"
    response += f"{'-----------': <20}{'----------------' : >42}"
    response0 = ''
    for i in range(1, len(names)):
      if payments[i] == '0':
        name = names[i]
        d = 35 - len(name)
        response0 += f"{name : <20}{payments[i] : >{d}}\n"
      else:
        name = '_'+names[i]
        d = 35 - len(name)
        response += f"\n{name : <20}{payments[i] : >{d}}"
    data = title + title2 + seperator + response + seperator + title3 + \
          seperator + response0 + footer + seperator + card + seperator + \
          bill
    bot.send_message(message.chat.id, data)
  else:
    bot.send_message(message.chat.id, "X اين گزارش براي اين گروه نميباشد X")


def recieve_payment(message):
  payment = message.text.split('/')
  if len(payment) < 3:
    return False
  else:
    return True


@bot.message_handler(func=recieve_payment)
def record_payment(message):
  event_name = message.text.split('/')[0].strip()
  user = message.text.split('/')[1].strip()
  pay = message.text.split('/')[2].strip()
  i = 2
  while event.cell(i, 1).value != None:
    if event.cell(i, 1).value == user:
      event.update_cell(i, 2, pay)
      bot.send_message(
        message.chat.id,
        f' مبلغ {pay} تومان توسط {user} بابت دورهمی {event_name} پرداخت شد')
        # f'{user} paid {pay}$ for {event_name}')
      break
    i += 1
  else:
    bot.send_message(message.chat.id,
                     f'اين نام ({user}) در اين دورهمي ثبت نشده است')


@bot.message_handler(commands=['bill'])
def bill_total_amount(message):
  event_name = message.text.split('\n')[1].strip()
  total_amount = message.text.split('\n')[2]
  event = spreadsheet.worksheet(event_name)
  event.update_cell(2, 4, total_amount)
  bot.reply_to(message, f'مبلغ فاکتور ({event_name}) ثبت شد')


bot.polling()
