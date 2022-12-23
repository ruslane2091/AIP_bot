import os
import discord
from discord import utils, guild
from discord.ext import commands
import redis
import json

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

redis_url = os.environ.get('REDIS_URL')
Token = 'ID' 

#  Создаём базу данных или загружаем готовую
if redis_url is None:

    try:
        data = json.load(open('Database.json', 'r', encoding='utf-8'))  # Вывод базы данных

    except:

        data = {
            "post_id": 1054381354411896872,
            "roles": {
            },
            "administrators": {
                "admins": [
                    "ruslane2091#6184"
                ],
                "editors": [
                    "ruslane2091#6184"
                ]
            },
            "excroles": {},
            "Max_roles_per_user": 10,
            "prefix": "!",
            "twitchlist": [
                "плохое слово",
                "nigga",
                "naga",
                "ниггер",
                "нига",
                "нага",
                "faggot",
                "пидор",
                "пидорас",
                "педик",
                "гомик",
                "петух",
                "хач",
                "жид",
                "хиджаб",
                "даун",
                "аутист",
                "дебил",
                "retard",
                "негр",
                "негры",
                "нигер",
                "пидорас",
                "негр",
                "virgin",
                "simp",
                "incel",
                "девственник",
                "cимп",
                "инцел",
                "cunt",
                "пизда",
                "куколд",
                "nigger"
            ]
        }


else:

    redis_db = redis.from_url(redis_url)
    raw_data = redis_db.get('data')
    print(raw_data)
    print('Вывод базы данных')

    if raw_data is None:
        print('None')
        data = {
            "post_id": 111222333,

            "roles": {

            },
            "administrators": {
                "admins": [
                    "ruslane2091#6184"
                ],
                "editors": [
                    "ruslane2091#6184"
                ]
            },
            "excroles": {},
            "Max_roles_per_user": 10,
            "prefix": "!",
            "twitchlist": [
                "плохое слово",
                "nigga",
                "naga",
                "ниггер",
                "нига",
                "нага",
                "faggot",
                "пидор",
                "пидорас",
                "педик",
                "гомик",
                "петух",
                "хач",
                "жид",
                "хиджаб",
                "даун",
                "аутист",
                "дебил",
                "retard",
                "негр",
                "негры",
                "нигер",
                "пидорас",
                "негр",
                "virgin",
                "simp",
                "incel",
                "девственник",
                "cимп",
                "инцел",
                "cunt",
                "пизда",
                "куколд",
                "nigger"
            ]
        }

    else:
        data = json.loads(raw_data)
        print(data)  # Вывод нашей базы данных
        print('Вывели')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    '''
        on ready
        Данная функция отвечает за проверку работоспособности бота
        :return: ничего
        '''
    print('bot connected')


async def number(emoji): #при проверке
    '''
        number
        Определяет индекс нужного эмоди
        :param emoji: получает эмоджи, чтобы искать его в бд
        :return: номер эмодзи
        '''
    for i in range(len(data['roles'])):

        if emoji in data['roles'][i]:
            return i
     #при проверке return 0


async def check(text): #при проверке
    '''
       check
       Проверяет нахождение слова в словаре запрещённых слов
       :param text: получает сообщение
       :return: 1 или 0. Т.е. найдено или нет
       '''
    for i in range(len(data['twitchlist'])):
        if data['twitchlist'][i] in text.lower().replace(' ', ''):
            return 1
    return 0


def check_adm(mes):
    '''
    check_adm
    Проверка на то, является ли человек админом
    :param mes: ник пользователя
    :return: либо 0 если не админ, либо номер в админке
    '''
    for i in range(len(data['administrators']['admins'])):
        if str(data['administrators']['admins'][i] in str(mes)):
            return i

    for i in range(len(data['administrators']['editors'])):
        if str(data['administrators']['editors'][i] in str(mes)):
            return i

    return 0


@bot.event
async def on_raw_reaction_add(payload):
    '''
        on_raw_reaction_add
        Слушатель событий, проверяет поставлена ли реакция на сообщение
        :param payload:
        :return: лишь вызывает какие-то функции
        '''
    if payload.message_id == data['post_id']:

        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        emoji = payload.emoji.name
        member = payload.member

        if emoji in data['roles']:

            role = utils.get(message.guild.roles, id=data['roles'][emoji])

            print(f'{member} Получил роль {role}')
            await member.add_roles(role)

        else:
            print(f'Я не вижу данного эмоджи в базе. {emoji}')


@bot.event
async def on_raw_reaction_remove(payload):
    '''
    on_raw_reaction_remove
    Слушатель событий, определяет убрали ли реакцию
    :param payload:
    :return: убирает роль
    '''
    if data['post_id'] == payload.message_id:

        emoji = payload.emoji.name  # эмоджи при нажатии на которое выдается роль

        if emoji in data['roles']:  # само эмоджи

            guild = await(bot.fetch_guild(payload.guild_id))
            role = discord.utils.get(guild.roles, id=data['roles'][emoji])  # определяем роль которую будем выдавать

            member = await(guild.fetch_member(payload.user_id))

            if member is not None:  # проверяем есть ли он на сервере

                await member.remove_roles(role)  # забираем рольку
                print(f'{member} лишился роли {role}')

            else:
                print(f'{member} Не найден на сервере')

        else:
            print(f'{emoji} not found')


@bot.command()
async def change_post(ctx, text):
    '''
        change_post
        Меняет id поста на нужное
        :param ctx: внутренняя команда
        :param text: текст с idшником
        :return: меняет бд и отправляет новый пост ид
        '''
    author = ctx.message.author


    if (str(author) in data['administrators']['admins']) or (str(author) in data['administrators']['editors']):
        data['post_id'] = int(text)

        await change_data()
        await author.send(data['post_id'])


@bot.command()
async def base_info(ctx):
    '''
        base_info
        Отправляет сообщение с базовой информацией по боту
        :param ctx: внутренняя команда
        :return:
        '''
    author = ctx.message.author

    await author.send('''Добро пожаловать в discord-канал! 
Обязательно ознакомься с правилами.
Приятного времяпровождения на сервере, а для получения полной информации о функционале бота, напишите !tech_info 
С уважением, администратор канала "Проект по АиПу"!''')

    print(f'Пользователь {author} получил базовую информацию о сервере')


@bot.command()
async def tech_info(ctx):
    '''
        tech_info
        Отправляет техническую информацию о боте. То есть о его функционале и организацонные моменты
        :param ctx:
        :return: отправляет сообщение
        '''
    author = ctx.message.author

    serv_name = ctx.message.guild.name
    print(serv_name)
    
    await author.send('''В перечень функционала бота входит:
1.Добавление/удаление роли у пользователя по реакции.
2.Привествие пользователя при присоединении к discord-каналу.
3.Фильтация запрещенных слов на площадке Twitch.

Полный список доступных Вам команд:
!base_info – базовая информация
!tech_info – техническая информация
''')

    if (str(author) in data['administrators']['admins']) or (str(author) in data['administrators']['editors']):
        await author.send('''Также специально для администраторов и редакторов канала: 
!add_emoji - Добавляет эмодзи и номер роли в базу данных 
Пример работы: !add_emoji 😋 11112222 (ВАЖНО: необходимы,как минимум, права редактора) 

!add_banworld - Добавляет запретные слова
Пример: !add_banworld дом (ВАЖНО: необходимо вводить слово с маленкой буквы)
''')

    print(f'Пользователь {author} получил техническую информацию о сервере')


@bot.event
async def on_member_join(member):
    """
       on_member_join
       Отправляет сообщение при присоединеннии пользователя на сервер
       :param member: ник пользователя
       :return: отправляет сообщение
       """
    print(f'{member} присоединился к серверу')

    await member.send(f'''Приветствуем {member}, на сервере. Написав команду !base_info 
ты узнаешь всю необходимую информацию по серверу. ''')


async def change_data():
    '''
    change_data
    Функция изменения бд
    :return: обновляет бд
    '''
    if redis_url is None:  # Обработка базы данных
        print('redis_url is None')
        json.dump(data,
                  open('Database.json', 'w', encoding='utf-8'),
                  indent=2,
                  ensure_ascii=False,
                  )

        # Загружаем базу данных из редис

    else:

        redis_db = redis.from_url(redis_url)
        redis_db.set('data', json.dumps(data))
        print('Готово!')


@bot.command()
async def add_emoji(ctx, emoji, text):
    """
        add_emoji
        Добавляет эмоцию в базу данных
        :param ctx:
        :param emoji: эмодзи
        :param text: текст сообщения
        :return: обновляет бд, вызывает для этого функцию
        """
    author = ctx.message.author

    if (str(author) in data['administrators']['admins']) or (str(author) in data['administrators']['editors']):

        print(f'{author} Отправил {emoji} и роль {text}')

        data['roles'][emoji] = int(text)

        await change_data()
        await author.send('Эмодзи получен')

    else:

        await author.send('''Вы не являетесь администратором. 
Обратитесь за доступом''')


@bot.command()
async def add_banworld(ctx, *, text):
    """
    add_banworld
    Функция добавление запрещённого слова в базу данных
    :param ctx:
    :param text: слово
    :return: обновляет бд
    """
    author = ctx.message.author

    if (str(author) in data['administrators']['admins']) or (str(author) in data['administrators']['editors']):
        if text not in data['twitchlist']:
            data['twitchlist'] += [str(text)]

            await change_data()

            print(f'слово {text} добавлено')

    else:
        await author.send('''Вы не являетесь администратором. 
    Обратитесь за доступом''')


@bot.command()
async def delit_banworld(ctx, *, text):
    '''
    delit_banworld
    Удаление бан слова из бд
    :param ctx:
    :param text: слово
    :return: обновляет бд
    '''
    author = ctx.message.author

    if (str(author) in data['administrators']['admins']) or (str(author) in data['administrators']['editors']):
        if text in data['twitchlist']:

            data['twitchlist'].remove(str(text))

            await change_data()

            print(f'слово {text} удалено')
        else:
            author.send(f'Я не вижу данного слова {text} в базе')

    else:
        await author.send('''Вы не являетесь администратором. 
    Обратитесь за доступом''')


@bot.command()
async def delit_emoji(ctx, emoji):
    '''
    delit_emoji
    Удаление эмоции из бд
    :param ctx:
    :param emoji: эмодзи
    :return: обновляет бд, удаляет оттуда
    '''
    author = ctx.message.author

    if (str(author) in data['administrators']['admins']) or (str(author) in data['administrators']['editors']):
        del data['roles'][emoji]

        await change_data()

        print(f'{emoji} удалён из базы данных')

@bot.command()
async def vivod_bd(ctx):
    """
    vivod_bd
    Выводит всю базу данных
    :param ctx:
    :return: отправляет базу данных админу
    """
    author = ctx.message.author
    mes = ctx.message.content
    mes = str(mes).replace('!vivod_bd ', '', 1)

    if str(author) in (data['administrators']['admins'] or data['administrators']['editors']):
        await author.send(data[mes])


@bot.command()
async def add_admin(ctx):
    """
    add_admin
    добавление пользователя в администраторы бота
    :param ctx:
    :return: добавляет админа
    """
    author = ctx.message.author
    mes = ctx.message.content
    mes = str(mes).replace('!add_admin ', '', 1)

    h = -1

    if 'editor'.lower() in mes:
        mes = mes.replace('editor ', '', 1)
        h = 0

    if 'admin'.lower() in mes:
        mes = mes.replace('admin ', '', 1)
        h = 1

    if str(author) in (data['administrators']['admins']):

        if h == 0:
            data['administrators']['editors'] += [str(mes)]
            await author.send(f'{mes} добавлен в список редакторов')
            await change_data()

        if h == 1:
            data['administrators']['admins'] += str(mes)
            await author.send(f'{mes} добавлен в список администраторов')
            await change_data()

        if h == -1:
            await author.send(f'Мне не понятно ваше сообщение, попробуйте снова: {mes}')


@bot.command()
async def delit_admin(ctx):
    """
    delit_admin
    Удаляяет пользователя из админки бота
    :param ctx:
    :return: удаляет админа из бд
    """
    author = ctx.message.author
    mes = ctx.message.content
    mes = str(mes).replace('!delit_admin ', '', 1)

    h = -1

    if 'editor'.lower() in mes:
        mes = mes.replace('editor ', '', 1)
        h = 0

    if 'admin'.lower() in mes:
        mes = mes.replace('admin ', '', 1)
        h = 1

    await author.send(f'{mes} - ваш запрос')
    if str(author) in (data['administrators']['admins']):

        if (mes in data['administrators']['admins']) or (mes in data['administrators']['editors']):

            if str(author) not in str(mes):
                if h == 1:
                    for i in range(len(data['administrators']['admins'])):

                        if data['administrators']['admins'][i] == mes:
                            del data['administrators']['admins'][i]

                            await change_data()

                            print(f'{mes} удалён из списка администраторов')
                            break

                if h == 0:

                    for i in range(len(data['administrators']['editors'])):

                        if data['administrators']['editors'][i] == mes:
                            del data['administrators']['editors'][i]

                            await change_data()

                            print(f'{mes} удалён из списка редакторов')
                            break



            else:
                await author.send('вы не можете удалить самого себя')

        else:
            await author.send(f'{mes} Я не вижу данного администратора/редактора')


@bot.event
async def on_message(message):
    """
    on_message
    Обработчик всех отправленных сообщений
    :param message: сообщение
    :return:
    """
    mes = message.content
    author = message.author

    if '!' in mes:
        await bot.process_commands(message)

    if (str(author) not in data['administrators']['admins']) and (str(author) not in data['administrators']['editors']):

        if await check(mes):
            await message.delete()

            print(f'Сообщение удалено {message.content}')

        else:
            print('Банвордов не замечено')

    else:
        print(f'{author} адмнистратор, поэтому пишет, что захочет')

bot.run(Token)  #при проверке
