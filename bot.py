import config
import telebot
import Find_and_Pars

flag = 0
bot =telebot.TeleBot(config.token)
@bot.message_handler(commands=['start'])
def welcome(message):
    text ='''Привет.
Я с удовльствием помогу тебе получить информацию по интересующему тебя фильму.
Расскажу о его жанре, актерах и годе выпуска.
Также ты можешь создать список фильмов, которые ты бы хотел посмотреть в ближайшее время.
Добавляй, удаляй, меняй местами любые фильмы!
Если возникнут вопросы, используй команду /help
С любовью твой Kinobot
    '''
    bot.send_message(message.chat.id,text )

@bot.message_handler(commands=['help'])
def help(message):
    text ='''This is place for my command
    '''
    bot.send_message(message.chat.id,text )

@bot.message_handler(content_types = ['text'])
def message_film(message):
    film_lis = Find_and_Pars.main_pars(message.text)
    #for film in film_lis:
        #bot.send_message(message.chat.id, str(film[0]) + '. '+str(film[1:]))
    markup = generate_markup(film_lis)
    bot.send_message(message.chat.id, film_lis, reply_markup=markup )

#@bot.message_handler(commands=['moreabout'])
#def help(message):
    #film_lis = Find_and_Pars.main_pars(message.text)
    #bot.send_message(message.chat.id, Find_and_Pars.info_film(1, film_lis))
def generate_markup(film_lis):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for film in film_lis:
        markup.add(film[1:])

    return markup

if __name__ == '__main__':
    bot.polling(none_stop=True)