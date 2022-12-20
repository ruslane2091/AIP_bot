import os
import discord
from discord import utils, guild
from discord.ext import commands
# from discord.ui import Bu
import redis
import json

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

redis_url = os.environ.get('REDIS_URL')
Token = 'MTA1NDMwMTU1MTU1ODE0NDA3MA.Gynj4I.jk3a_bD9BueLKYMC69jqTRpntBfSkBpxNDwOZo'

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
        data = json.loads(raw_data)
        print(data)  # Вывод нашей базы данных
        print('Вывели')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():

    print('bot connected')


async def number(emoji):
    for i in range(len(data['roles'])):

        if emoji in data['roles'][i]:
            return i


async def check(text):
    for i in range(len(data['twitchlist'])):
        if data['twitchlist'][i] in text.lower().replace(' ', ''):
            return 1
    return 0


def check_adm(mes):
    for i in range(len(data['administrators']['admins'])):
        if str(data['administrators']['admins'][i] in str(mes)):
            return i

    for i in range(len(data['administrators']['editors'])):
        if str(data['administrators']['editors'][i] in str(mes)):
            return i

    return 0


@bot.event
async def on_raw_reaction_add(payload):
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
    author = ctx.message.author

    if (str(author) in data['administrators']['admins']) or (str(author) in data['administrators']['editors']):
        data['post_id'] = int(text)

        await change_data()
        await author.send(data['post_id'])


@bot.command()
async def base_info(ctx):
    author = ctx.message.author

    await author.send('''Добро пожаловать в discord-канал! 
Обязательно ознакомься с правилами.
Приятного времяпровождения на сервере, а для получения полной информации о функционале бота, напишите !tech_info 
С уважением, администратор канала "Проект по АиПу"!''')

    print(f'Пользователь {author} получил базовую информацию о сервере')


@bot.command()
async def tech_info(ctx):
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
Пример: !add_banworld шлюпка. Слова Вводить с МАЛОЙ буквы!!!!!!!!
''')

    print(f'Пользователь {author} получил техническую информацию о сервере')


@bot.event
async def on_member_join(member):
    print(f'{member} присоединился к серверу')

    await member.send(f'''Приветствуем {member}, на сервере. Написав команду !base_info 
ты узнаешь всю необходимую информацию по серверу. ''')


async def change_data():
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
    author = ctx.message.author

    if (str(author) in data['administrators']['admins']) or (str(author) in data['administrators']['editors']):
        del data['roles'][emoji]

        await change_data()

        print(f'{emoji} удалён из базы данных')

@bot.command()
async def vivod_bd(ctx):
    author = ctx.message.author
    mes = ctx.message.content
    mes = str(mes).replace('!vivod_bd ', '', 1)

    if str(author) in (data['administrators']['admins'] or data['administrators']['editors']):
        await author.send(data[mes])


@bot.command()
async def add_admin(ctx):
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
bot.run(Token)
