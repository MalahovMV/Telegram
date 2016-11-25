import config
import Find_and_Pars
from telegram.ext import Updater, CommandHandler
from telegram import inlinekeyboardmarkup


TOKEN = config.token

def start_bot(bot, update):
    text = '''Привет.
Я с удовльствием помогу тебе получить информацию по интересующему тебя фильму.
Расскажу о его жанре, актерах и годе выпуска.
Также ты можешь создать список фильмов, которые ты бы хотел посмотреть в ближайшее время.
Добавляй, удаляй, меняй местами любые фильмы!
Если возникнут вопросы, используй команду /help
С любовью твой Kinobot
        '''
    update.message.reply_text(text)

def find_film(bot,update):
    film_lis = Find_and_Pars.main_pars(update.message.text)
    for film in film_lis:
        update.message.reply_text(film)

def generate_markup(film_lis):
    markup = []
    for film in film_lis:
        markup.add(film[1:])

    return  inlinekeyboardmarkup(markup)

def main():
    updater = Updater(TOKEN)
# Get the dispatcher to register handlers
    dp = updater.dispatcher

# Add handlers for Telegram messages
    dp.add_handler(CommandHandler('start', start_bot))
    dp.add_handler(CommandHandler('find_film', find_film))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

