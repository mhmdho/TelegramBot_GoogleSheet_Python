import telebot
import os

API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)
