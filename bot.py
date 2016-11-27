import config
import telebot
import ptwee_db_orm
import Find_and_Parse

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
def help_bot(message):
    text = '''Можешь со мной общаться посредством команд, обязательно обрати внимание на точку после каждой команды:
/find_film_ <NAME> - я буду искать фильм по названию, написанному после команды
/about_film_ <NAME>. <AGE> - я постараюсь предоставить тебе больше информации о данном фильме
/add_film_ <NAME>. <AGE> - добавлю этот фильм в конец твоей очереди фильмов
/print_queue_ - выведу на экран все фильмы, которые ты выбрал, в порядке очереди
/print_first_ - выведу первый фильм из твоей очереди на экран
/pop_film_ - удалю первый фильм в очереди
/del_film_ <NAME>. <AGE> - удалю фильм из очереди по его названию
/change_position_ <NAME>. <AGE>. <POSITION> - переставлю указанный тобою фильм в указанную тобой позицию
/print_up_age_ <YEAR> - выведу фильмы из твоей очереди, которые вышли после указанного тобою года
/print_up_reit_ <REIT> - выведу фильмы из твоей очереди, рейтинг которых выше указанного тобою
    '''
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['find_film_'])
def find_film(message):
    try:
        #bot.send_message(message.chat.id, message.text.split('_')[2])
        html = Find_and_Parse.get_html(message.text.split('_')[2])
        film_lis = Find_and_Parse.parse_film(html)
        for fil in film_lis:
            bot.send_message(message.chat.id, str(fil.keys())[12:-3])

    except:
        bot.send_message(message.chat.id, 'Извини, не могу обработать такой запрос, посмотри /help')

@bot.message_handler(commands=['about_film_'])
def about_film(message):
    try:
        #film_lis = ptwee_db_orm.print_films()
        flag = True
        #text = str(message.text.split('_ ')[-1]).split('. ')
        #for film in film_lis:
         #   movie = film.split('.')
          #  if (text[0] in movie[0]) and (text[1] in movie[2]):
           #     bot.send_message(message.chat.id, film)
            #    flag = False

        if flag:
            #bot.send_message(message.chat.id, message.text.split('_')[2])
            html = Find_and_Parse.get_html(message.text.split('_')[2])
            film = Find_and_Parse.parse_film(html)
            dict_film = Find_and_Parse.parse_find(str(film[0].values())[14:-3])
            text = 'Название: ' + dict_film['name'] + "\nГод выхода: " + dict_film['age']
            text +="\nРежзисер и актеры: " + dict_film['actors'] + "\nЖанр: " + dict_film['genre']
            text +="\nРейтинг: " + dict_film['reit']
            bot.send_message(message.chat.id, text)

    except:
        bot.send_message(message.chat.id, 'Извини, не могу обработать такой запрос, посмотри /help')

@bot.message_handler(commands=['add_film_'])
def add_film(message):
    try:
        html = Find_and_Parse.get_html(message.text.split('_')[2])
        film = Find_and_Parse.parse_film(html)
        dict_film = Find_and_Parse.parse_find(str(film[0].values())[14:-3])
        bool = ptwee_db_orm.film_in(dict_film['name'], dict_film['age'], str(message.chat.id))
        if not bool:
            ptwee_db_orm.add_film(str(dict_film['name']), ptwee_db_orm.len_db(), str(dict_film['age']), str(dict_film['actors']),
                     str(dict_film['reit']), str(dict_film['genre']), str(message.chat.id))

        bot.send_message(message.chat.id, 'Добавил тебе новый фильм ' + dict_film['name'])

    except:
        bot.send_message(message.chat.id, 'Извини, не могу обработать такой запрос, посмотри /help')

@bot.message_handler(commands=['print_queue_'])
def print_queue(message):
    try:
        film_lis = ptwee_db_orm.print_films()
        for film in film_lis:
            bot.send_message(message.chat.id, str(film))

    except:
        bot.send_message(message.chat.id, 'Упс, что-то пошло не так')

@bot.message_handler(commands=['print_first.'])
def print_first(message):
    try:
        bot.send_message(message.chat.id, 'print')

    except:
        bot.send_message(message.chat.id, 'Упс, что-то пошло не так')

@bot.message_handler(commands=['pop_film.'])
def pop_film(message):
    try:
        bot.send_message(message.chat.id, 'pop')

    except:
        bot.send_message(message.chat.id, 'Очередь уже пуста, нечего удалять')

@bot.message_handler(commands=['del_film.'])
def del_film(message):
    try:
        bot.send_message(message.chat.id, message.text.split('.')[1])

    except:
        bot.send_message(message.chat.id, 'Такого фильма нет в очереди, нечего удалять')

@bot.message_handler(commands=['change_position.'])
def change_position(message):
    try:
        bot.send_message(message.chat.id, message.text.split('.')[1])

    except:
        bot.send_message(message.chat.id, 'Не могу выполнить данную операцию, позиция/фильм недоступны')

@bot.message_handler(commands=['print_up_age.'])
def print_up_age(message):
    try:
        bot.send_message(message.chat.id, 'age')

    except:
        bot.send_message(message.chat.id, 'Упс, что-то пошло не так')

@bot.message_handler(commands=['print_up_reit.'])
def print_up_reit(message):
    try:
        bot.send_message(message.chat.id, 'reit')

    except:
        bot.send_message(message.chat.id, 'Упс, что-то пошло не так')

if __name__ == '__main__':
    bot.polling(none_stop=True)