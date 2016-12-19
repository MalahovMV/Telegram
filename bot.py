import config
import  telebot
import ptwee_db_orm
import Find_and_Parse
import logging
import sys
import time

# Обусловлено особенностями поиска на сайте, который был распаршен
def del_dash(string):
    for j in range(len(string)):
        if string[j] == '-':
            string = string[:j] + ' ' + string[j + 1:]

    return string

#В случае пустого или некорректного запроса сайт создает именно такой ответ
empty_req = [{'Иван Царевич и Серый Волк 2, 2013,':
'http://megogo.net/ru/view/1148471-ivan-carevich-i-seryy-volk-2.html'},
{'Малавита, 2013,': 'http://megogo.net/ru/view/1321981-malavita.html'},
{'Superнянь (Супернянь), 2014,': 'http://megogo.net/ru/view/1373621-supernyan-supernyan.html'},
{'Паркер, 2012,': 'http://megogo.net/ru/view/1197381-parker.html'},
{'Судья Дредд, 2012,': 'http://megogo.net/ru/view/94941-sudya-dredd.html'},
{'Проповедник с пулеметом, 2011,': 'http://megogo.net/ru/view/1604261-propovednik-s-pulemetom.html'}]
logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]#%(levelname)-8s [%(asctime)s] %(message)s'
                    ,level=logging.WARNING, filename='mylog.log')

bot =telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def welcome(message):
    text ='''Привет.
Я с удовольствием помогу тебе получить информацию по интересующему тебя фильму.
Расскажу о его жанре, актерах и годе выпуска.
Также ты можешь создать список фильмов, которые ты бы хотел посмотреть в ближайшее время.
Добавляй, удаляй, меняй местами любые фильмы!
Если возникнут вопросы, используй команду /help
С любовью твой Kinobot
'''
    ptwee_db_orm.add_user(message.chat.id)
    bot.send_message(message.chat.id,text)

@bot.message_handler(commands=['help'])
def help_bot(message):
    ptwee_db_orm.add_user(message.chat.id)
    text = '''Можешь со мной общаться посредством команд, обязательно обрати внимание на нижнее подчеркивание после каждой команды.
Обязательно обрати внимание на команды, в которых обязательно указание года выхода фильма,
без этого поиск будет работать не всегда верно, так как существуют фильмы с одинаковым названием, но разного года выхода.
/find_film_ <NAME> - я буду искать фильм по названию, написанному после команды
/about_film_ <NAME> <AGE> - я постараюсь предоставить тебе больше информации о данном фильме, пожалуйста не забывай вбивать год
/add_film_ <NAME>  <AGE> - добавлю этот фильм в конец твоей очереди фильмов, пожалуйста не забывай вбивать год
/print_queue_ - выведу на экран все фильмы, которые ты выбрал, в порядке очереди
/print_first_ - выведу первый фильм из твоей очереди на экран
/pop_film_ - удалю первый фильм в очереди
/del_film_ <NAME>  <AGE> - удалю фильм из очереди по его названию, пожалуйста не забывай вбивать год
/change_position_ <NAME>  <AGE>  <POSITION> - переставлю указанный тобою фильм в указанную тобой позицию, пожалуйста не забывай вбивать год
/print_up_age_ <YEAR> - выведу фильмы из твоей очереди, которые вышли после указанного тобою года
/print_up_reit_ <REIT> - выведу фильмы из твоей очереди, рейтинг которых выше указанного тобою
/add_rand_ - предложу тебе выбрать жанр, а потом добавлю тебе в очередь случайный фильм этого жанра
    '''
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['find_film_'])
def find_film(message):
    try:
        ptwee_db_orm.add_user(message.chat.id)
        film = message.text.split('_')[2]
        film = del_dash(film)
        html = Find_and_Parse.get_html(film)
        film_lis = Find_and_Parse.parse_film(html)
        if film_lis == empty_req:
            bot.send_message(message.chat.id, 'Извини, не смог найти такой фильм')

        else:
            for film in film_lis:
                bot.send_message(message.chat.id, str(film.keys())[12:-4])

            bot.send_message(message.chat.id, '''Хочешь увидеть более подробную информацию о каком-либо фильме или добавить его себе в очередь для просмотра?
Тогда введи одну из комманд  about_film_ или add_film_ а после них название фильма и год его выхода
Можешь просто скопировать в команду один из тех фильмов, которые предложил тебе я''')

    except:
        bot.send_message(message.chat.id, 'Извини, не могу обработать такой запрос, посмотри /help')
        logging.warning('Возникла проблема с добавлением фильма у юзера - ' + str(message.chat.id) + ' При запросе' +  message.text)

@bot.message_handler(commands='about_film_')
def about_film(message):
    try:
        ptwee_db_orm.add_user(message.chat.id)
        film = message.text.split('_')[2]
        i = len(film) - 1
        while True:
            if (film[i] >= '0') and (film[i] <= '9'):
                break

            else:
                i -= 1

        film = del_dash(film)
        name = film[:i - 4]
        age = film[i - 3:]
        text = ptwee_db_orm.return_film(name,age)

        if text:
            bot.send_message(message.chat.id, text)

        else:
            html = Find_and_Parse.get_html(film)
            film = Find_and_Parse.parse_film(html)
            dict_film = Find_and_Parse.parse_find(str(film[0].values())[14:-3])
            text = 'Название: ' + dict_film['name'] + "\nГод выхода: " + dict_film['age']
            text +="\nРежзисер и актеры: " + dict_film['actors'] + "\nЖанр: " + dict_film['genre']
            text +="\nРейтинг: " + dict_film['reit']
            bot.send_message(message.chat.id, text)

    except:
        bot.send_message(message.chat.id, 'Извини, не могу обработать такой запрос, посмотри /help')
        logging.warning('Возникла проблема с поиском информации о фильме у юзера - ' + str(message.chat.id) + ' При запросе' +  message.text)

@bot.message_handler(commands=['add_film_'])
def add_film(message):
    try:
        ptwee_db_orm.add_user(message.chat.id)
        film = message.text.split('_')[2]
        film = del_dash(film)
        html = Find_and_Parse.get_html(film)
        film = Find_and_Parse.parse_film(html)
        dict_film = Find_and_Parse.parse_find(str(film[0].values())[14:-3])
        bool = ptwee_db_orm.return_film(dict_film['name'], dict_film['age'])
        if not bool:
            ptwee_db_orm.add_film(str(dict_film['name']), ptwee_db_orm.return_id_film(), str(dict_film['age']), str(dict_film['actors']),
                     str(dict_film['reit']), str(dict_film['genre']))

        ptwee_db_orm.add_film_user(dict_film['name'], dict_film['age'], message.chat.id)
        bot.send_message(message.chat.id, 'Добавил тебе новый фильм - ' + dict_film['name'])

    except:
        bot.send_message(message.chat.id, 'Извини, не могу обработать такой запрос, посмотри /help')
        logging.warning('Возникла проблема с добавлением фильма у юзера - ' + str(message.chat.id) + ' При запросе' +  message.text)


@bot.message_handler(commands=['print_queue_'])
def print_queue(message):
    try:
        ptwee_db_orm.add_user(message.chat.id)
        film_lis = ptwee_db_orm.print_films(message.chat.id)
        for film in film_lis:
            bot.send_message(message.chat.id, str(film))

    except:
        bot.send_message(message.chat.id, 'Нет фильмов в очереди')

@bot.message_handler(commands=['print_first_'])
def print_first(message):
    try:
        ptwee_db_orm.add_user(message.chat.id)
        film_lis = ptwee_db_orm.print_films(message.chat.id)
        bot.send_message(message.chat.id, str(film_lis[0]))

    except:
        bot.send_message(message.chat.id, 'Нет фильмов в очереди')

@bot.message_handler(commands=['pop_film_'])
def pop_film(message):
    try:
        ptwee_db_orm.add_user(message.chat.id)
        name = ptwee_db_orm.pop(message.chat.id)
        bot.send_message(message.chat.id, 'Удалил фильм - ' + name)

    except:
        bot.send_message(message.chat.id, 'Очередь уже пуста, нечего удалять')

@bot.message_handler(commands=['del_film_'])
def del_film(message):
    try:
        ptwee_db_orm.add_user(message.chat.id)
        film = message.text.split('_ ')[1]
        film = del_dash(film)
        i = len(film) - 1
        while True:
            if (film[i] >= '0') and (film[i] <= '9'):
                break

            else:
                i -= 1

        name = film[:i - 4]
        age = film[i - 3:]
        name = ptwee_db_orm.del_film(message.chat.id, name, age)
        bot.send_message(message.chat.id, "Удалил фильм - " + name)

    except:
        bot.send_message(message.chat.id, 'Такого фильма нет в очереди, нечего удалять')

@bot.message_handler(commands=['change_position_'])
def change_position(message):
    try:
        ptwee_db_orm.add_user(message.chat.id)
        text = message.text.split('_ ')[1]
        i = len(text) - 1
        while True:
            if (text[i] >= '0') and (text[i] <= '9'):
                break

            else:
                i -= 1

        j = i
        while True:
            if not ((text[j] >= '0') and (text[j] <= '9')):
                break

            else:
                j -= 1

        pos = text[j + 1:i + 1]
        text = text[:j + 1]
        i = len(text) - 1
        while True:
            if (text[i] >= '0') and (text[i] <= '9'):
                break

            else:
                i -= 1

        age = text[i - 3: i + 1]
        name = text[1:i - 4]
        ptwee_db_orm.change_position(message.chat.id, name, age, pos)
        bot.send_message(message.chat.id, "Поставил фильм на нужную позицию, можешь просмотреть очередь с помощью /print_queue_")

    except:
        bot.send_message(message.chat.id, 'Не могу выполнить данную операцию, позиция/фильм недоступны')

@bot.message_handler(commands=['print_up_age_'])
def print_up_age(message):
    try:
        ptwee_db_orm.add_user(message.chat.id)
        film_lis = ptwee_db_orm.return_up_age(message.chat.id, message.text.split('_ ')[1])
        if not film_lis:
            bot.send_message(message.chat.id, "Нет фильмов, удовлетворяющих критерию")

        for film in film_lis:
            bot.send_message(message.chat.id, film)

    except:
        bot.send_message(message.chat.id, 'Упс, что-то пошло не так')
        logging.error("Непредвиденная ошибка при выводе фильмов вышедших после года у пользователя - " + str(message.chat.id) + ' При запросе' +  message.text)


@bot.message_handler(commands=['print_up_reit_'])
def print_up_reit(message):
    try:
        ptwee_db_orm.add_user(message.chat.id)
        film_lis = ptwee_db_orm.return_up_reit(message.chat.id, message.text.split('_ ')[1])
        if not film_lis:
            bot.send_message(message.chat.id, "Нет фильмов, удовлетворяющих критерию")

        for film in film_lis:
            bot.send_message(message.chat.id, film)

    except:
        bot.send_message(message.chat.id, 'Упс, что-то пошло не так')
        logging.error("Непредвиденная ошибка при выводе фильмов с рейтингом у пользователя - " + str(message.chat.id) + ' При запросе' +  message.text)

@bot.message_handler(commands=['add_rand_'])
def choose_ganre(message):
    ptwee_db_orm.add_user(message.chat.id)
    bot.send_message(message.chat.id, 'Нажми на одну из команд')
    bot.send_message(message.chat.id, '/any')
    bot.send_message(message.chat.id, '/arthouse')
    bot.send_message(message.chat.id, '/action')
    bot.send_message(message.chat.id, '/military')
    bot.send_message(message.chat.id, '/detective')
    bot.send_message(message.chat.id, '/adult')
    bot.send_message(message.chat.id, '/comedy')
    bot.send_message(message.chat.id, '/melodrama')
    bot.send_message(message.chat.id, '/adventures')
    bot.send_message(message.chat.id, '/horror')
    bot.send_message(message.chat.id, '/thriller')
    bot.send_message(message.chat.id, '/fiction')

command = ['any', 'arthouse', 'action', 'military', 'detective', 'adult', 'comedy', 'melodrama', 'adventures', 'horror', 'thriller', 'fiction']
@bot.message_handler(commands=command)
def add_rand(message):
    try:
        ptwee_db_orm.add_user(message.chat.id)
        html = Find_and_Parse.catching_rand_film(message.text[1:])
        dict_film = Find_and_Parse.parse_find(html)
        bool = ptwee_db_orm.return_film(dict_film['name'], dict_film['age'])
        if not bool:
            ptwee_db_orm.add_film(str(dict_film['name']), ptwee_db_orm.return_id_film(), str(dict_film['age']),
                                  str(dict_film['actors']),
                                  str(dict_film['reit']), str(dict_film['genre']))

        ptwee_db_orm.add_film_user(dict_film['name'], dict_film['age'], message.chat.id)
        bot.send_message(message.chat.id, 'Добавил тебе новый фильм - ' + dict_film['name'])

    except:
        bot.send_message(message.chat.id, 'Извини, не могу обработать такой запрос, посмотри /help')
        logging.warning('Возникла проблема с добавлением фильма у юзера - ' + str(message.chat.id) + ' При запросе' +  message.text)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
            bot.set_update_listener(listener)
	
        except:
            logging.error('error: {}'.format(sys.exc_info()[0]))
            time.sleep(5)


    
