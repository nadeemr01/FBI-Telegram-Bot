import requests
import json
import numpy as np
import pandas as pd
from telegram import Update, BotCommand ,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from analysis import gender_based , race_based , nationality_based ,Cyber_classification, Murders_classification,Enterprise_classification,Counterintelligence_classification
Token = "7099094385:AAHLplGVoR9h8lKg9cJjiWFxsu1FEnrs6Rw"
Bot_username = "GP26FD_bot"

#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Добрый день!!!!")
#-----------------------------------------------------------------------------------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Справка по боту*\n\n"
        "Этот бот показывает статистику по базе разыскиваемых ФБР.\n\n"
        "📌 *Что я умею:*\n"
        "• Показывать общую статистику разыскиваемых\n"
        "• Анализировать данные по полу, расе и национальности\n"
        "• Показывать топ-5 национальностей по типам преступлений\n\n"
        "📂 *Основные разделы (команда /menu):*\n"
        "🔹 *Общие данные*\n"
        "   – По полу\n"
        "   – По расе\n"
        "   – По национальности\n\n"
        "🔹 *По типу преступления*\n"
        "   – 💻 Киберпреступники\n"
        "   – 🔪 Насильственные преступления (убийства)\n"
        "   – 🏢 Преступные организации\n"
        "   – 🕵️ Контрразведка\n\n"
        "ℹ️ Все данные основаны на открытом API FBI.\n\n"
        "👉 Используй /menu, чтобы начать работу."
    )
#-----------------------------------------------------------------------------------
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📌 Общие данные", callback_data="menu_classification")],
        [InlineKeyboardButton("⚠️ По типу преступления", callback_data="menu_warning")],
        [InlineKeyboardButton("💡Подсказка", callback_data="menu_reward")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Выбери категорию:",
        reply_markup=reply_markup
    )
#-----------------------------------------------------------------------------------
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    choice = query.data

    if choice == "menu_classification":
        await classification_menu(query)
    elif choice == "menu_warning":
        await warning_menu(query)
    elif choice == "menu_reward":
        await query.edit_message_text("Напиши Эрдени")
#-----------------------------------------------------------------------------------
async def classification_menu(query):
    keyboard = [
        [InlineKeyboardButton("По полу", callback_data="class_tmw")],
        [InlineKeyboardButton("По рассы", callback_data="class_vc")],
        [InlineKeyboardButton("По националности", callback_data="class_si")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
    ]

    await query.edit_message_text(
        "Выбери классификацию:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
#-----------------------------------------------------------------------------------
async def classification_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    selection = query.data

    if selection == "class_tmw":
        msg = gender_based()
    elif selection == "class_vc":
        msg = race_based()
    elif selection == "class_si":
        msg = nationality_based()
    else:
        return

    await query.edit_message_text(msg)
#-----------------------------------------------------------------------------------
async def warning_menu(query):
    keyboard = [
        [InlineKeyboardButton("киберпреступники", callback_data="warn_cyb")],
        [InlineKeyboardButton("Насильственные преступления - Убийства", callback_data="warn_murd")],
        [InlineKeyboardButton("Расследования преступных организаций", callback_data="warn_org")],
        [InlineKeyboardButton("Контрразведка", callback_data="warn_cntr")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
    ]

    await query.edit_message_text(
        "Выбери классификацию:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
#-----------------------------------------------------------------------------------
async def warning_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    selection = query.data

    if selection == "warn_cyb":
        msg = Cyber_classification()
    elif selection == "warn_murd":
        msg = Murders_classification()
    elif selection == "warn_org":
        msg = Enterprise_classification()
    elif selection == "warn_cntr":
        msg = Counterintelligence_classification()    
    else:
        return

    await query.edit_message_text(msg)
#-----------------------------------------------------------------------------------
async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("📌 Общие данные", callback_data="menu_classification")],
        [InlineKeyboardButton("⚠️ По типу преступления", callback_data="menu_warning")],
        [InlineKeyboardButton("💡Подсказка", callback_data="menu_reward")]
    ]


    await query.edit_message_text(
        "Выбери категорию:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
#-----------------------------------------------------------------------------------
async def post_init(application):
    commands = [
        BotCommand("start", "Запускай"),
        BotCommand("help", "Я помогу тебе"),
        BotCommand("menu", "Открой тут интересно")
    ]
    await application.bot.set_my_commands(commands)

#-----------------------------------------------------------------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower() 
    
    if "привет" in user_text:
        response = "Ну здарова!"
    elif "что ты умеешь" in user_text:
        response = "а для чего я команды создал?"
    elif "эрдени" in user_text:
        response = "Просто легенда!"    
    else:
        response = f"Ты написал: {update.message.text}. а я тебя не понимаю, я ещё не на столько умен!"
    
    await update.message.reply_text(response)
    
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------


if __name__ == '__main__':
    print("bot is starting.....")
    app = ApplicationBuilder().token(Token).post_init(post_init).build()
    

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", custom_command))

    app.add_handler(CallbackQueryHandler(menu_handler, pattern="^menu_"))
    app.add_handler(CallbackQueryHandler(classification_filter, pattern="^class_"))
    app.add_handler(CallbackQueryHandler(warning_filter, pattern="^warn_"))
    app.add_handler(CallbackQueryHandler(back_handler, pattern="^back_"))

    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    
    print("bot is working and polling")
    app.run_polling(poll_interval=3)
    
#-----------------------------------------------------------------------------------