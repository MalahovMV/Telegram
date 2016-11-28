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
    text = '''Можешь со мной общаться посредством команд, обязательно обрати внимание на нижнее подчеркивание после каждой команды:
В тех командах, где требуется указать название и год, пожалуйста копируй эти данные из команд /find_film_ ; /print_queue_
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
        for film in film_lis:
            bot.send_message(message.chat.id, str(film.keys())[12:-3])

    except:
        bot.send_message(message.chat.id, 'Извини, не могу обработать такой запрос, посмотри /help')

@bot.message_handler(commands=['about_film_'])
def about_film(message):
    try:
        film = message.text.split('_')[2]
        name = film.split(', ')[0][1:]
        age = film.split(', ')[1][:-1]
        text = ptwee_db_orm.return_film(name,age)

        if text:
            bot.send_message(message.chat.id, text + 'dshsghd')

        else:
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
    #try:
    if True:
        html = Find_and_Parse.get_html(message.text.split('_')[2])
        film = Find_and_Parse.parse_film(html)
        dict_film = Find_and_Parse.parse_find(str(film[0].values())[14:-3])
        bool = ptwee_db_orm.film_in(dict_film['name'], dict_film['age'], str(message.chat.id))
        if not bool:
            ptwee_db_orm.add_film(str(dict_film['name']), ptwee_db_orm.return_id_film(), str(dict_film['age']), str(dict_film['actors']),
                     str(dict_film['reit']), str(dict_film['genre']), str(message.chat.id))
        bot.send_message(message.chat.id, 'Добавил тебе новый фильм ' + dict_film['name'])

    #except:
        #bot.send_message(message.chat.id, 'Извини, не могу обработать такой запрос, посмотри /help')

@bot.message_handler(commands=['print_queue_'])
def print_queue(message):
    try:
        film_lis = ptwee_db_orm.print_films(message.chat.id)
        for film in film_lis:
            bot.send_message(message.chat.id, str(film))

    except:
        bot.send_message(message.chat.id, 'Упс, что-то пошло не так')

@bot.message_handler(commands=['print_first_'])
def print_first(message):
    try:
        film_lis = ptwee_db_orm.print_films(message.chat.id)
        bot.send_message(message.chat.id, str(film_lis[0]))

    except:
        bot.send_message(message.chat.id, 'Упс, что-то пошло не так')

@bot.message_handler(commands=['pop_film_'])
def pop_film(message):
    try:
        name = ptwee_db_orm.pop(message.chat.id)
        bot.send_message(message.chat.id, 'Удалил фильм - ' + name)

    except:
        bot.send_message(message.chat.id, 'Очередь уже пуста, нечего удалять')

@bot.message_handler(commands=['del_film_'])
def del_film(message):
    try:
        film = message.text.split('_')[2]
        name = film.split('. ')[0][1:]
        age = film.split('. ')[1]
        name = ptwee_db_orm.del_film(message.chat.id, name, age)
        bot.send_message(message.chat.id, "Удалил фильм - " + name)

    except:
        bot.send_message(message.chat.id, 'Такого фильма нет в очереди, нечего удалять')

@bot.message_handler(commands=['change_position_'])
def change_position(message):
    try:
        bot.send_message(message.chat.id, message.text.split('.')[1])

    except:
        bot.send_message(message.chat.id, 'Не могу выполнить данную операцию, позиция/фильм недоступны')

@bot.message_handler(commands=['print_up_age_'])
def print_up_age(message):
    try:
        film_lis = ptwee_db_orm.return_up_age(message.chat.id, message.text.split('_ ')[1])
        if not film_lis:
            bot.send_message(message.chat.id, "Нет фильмов, удовлетворяющих критерию")

        for film in film_lis:
            bot.send_message(message.chat.id, film)

    except:
        bot.send_message(message.chat.id, 'Упс, что-то пошло не так')

@bot.message_handler(commands=['print_up_reit_'])
def print_up_reit(message):
    try:
        film_lis = ptwee_db_orm.return_up_reit(message.chat.id, message.text.split('_ ')[1])
        if not film_lis:
            bot.send_message(message.chat.id, "Нет фильмов, удовлетворяющих критерию")

        for film in film_lis:
            bot.send_message(message.chat.id, film)

    except:
        bot.send_message(message.chat.id, 'Упс, что-то пошло не так')

if __name__ == '__main__':
    bot.polling(none_stop=True)