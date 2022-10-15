from sre_parse import CATEGORIES
import requests
import json
from telegram.ext import Application, CommandHandler
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Translates input text, returning translated text
def translate(query, language):
    url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "1db58d8f8dmsh7f016d406d9f822p167d98jsnd06e66cca352",
        "X-RapidAPI-Host": "deep-translate1.p.rapidapi.com"
    }
    body = {
        "q": query,
        "source": "en",
        "target": language
    }
    response = requests.post(url, json=body, headers=headers)
    string_response = response.text
    json_response = json.loads(string_response)
    translated_cat_fact = json_response["data"]["translations"]["translatedText"]
    return translated_cat_fact

def random_cat_fact():
    url = "https://catfact.ninja/fact"
    try:
        response = requests.get(url)
        string_response = response.text
        json_response = json.loads(string_response)
        cat_fact = json_response["fact"]
        translated_cat_fact = translate(cat_fact, "es")
        return translated_cat_fact
    except Exception as e:
        print(e)

async def get_cat_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cat_fact = random_cat_fact()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=cat_fact)

def main():
    application = ApplicationBuilder().token('5683250045:AAGhkpEDNHusUZvWQytNblns26DkCwOZJjk').build()
    
    cat_fact_hander = CommandHandler('getcatfact', get_cat_fact)
    application.add_handler(cat_fact_hander)
    
    application.run_polling()

if __name__ == "__main__":
    main()
