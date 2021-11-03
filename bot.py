import random; import discord; from discord.ext import commands; import sqlite3; from discord.utils import get

TOKEN = "OTA1MDMyMzYxNTU5ODc5Njgx.YYELEQ.zSJjH_5uT9HO1p-m1veTSe1cn6Q"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or(';'), intents=intents)
bot.remove_command('help')

conn = sqlite3.connect("createam.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Users
              (id INT, nickname TEXT, mention TEXT, buildmoney INT, codemoney INT)''')

joinr = ["{member} пришёл на запах пиццы.", "{member} присоединился к посиделкам у костра.", "{member} присоединился к нам, поприветствуем его!", "{member} спрятался у нас от шторма.", "{member} зашёл к нам. Надеемся, что он не забыл торт!"]
exitr = ["{member} ушёл в другую компанию.", "{member} покинул помещение. Надеемся, что он вернётся!", "{member} унесло ветром.", "{member} стало скучно у нас."]

@bot.event
async def on_ready():
    print("бот начал работу")#сообщение о готовности
    global allchatchannel
    allchatchannel = bot.get_channel(680475001568100425)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"https://discord.gg/Zu2Dg5cR2q"))
    for guild in bot.guilds:#т.к. бот для одного сервера, то и цикл выводит один сервер
        print(guild.id)#вывод id сервера
        serv=guild#без понятия зачем это
        for member in guild.members:#цикл, обрабатывающий список участников
            cursor.execute(f"SELECT id FROM users where id={member.id}")#проверка, существует ли участник в БД
            if cursor.fetchone()==None:#Если не существует
                cursor.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@{member.id}>', 0, 0)")
                print(f'{member.name} успешно записан в базу данных')
            else:#если существует
                print(f'{member.name} уже занесён в базу данных, запрос отклонён')
                pass
            conn.commit()#применение изменений в БД

@bot.event
async def on_member_join(member):
    embed = discord.Embed(
        description = (random.choice(joinr)).replace("{member}", "<@!" + str(member.id) +">"),
        colour = 0x73eff7
    )
    global my_channel
    await my_channel.send(embed=embed)
    guild = member.guild
    startrole = get(guild.roles, id=905034607395766294)
    await member.add_roles(startrole)

@bot.event
async def on_member_remove(member):
    embed = discord.Embed(
        description = (random.choice(exitr)).replace("{member}", "<@!" + str(member.id) +">"),
        colour = 0x257179
    )
    global my_channel
    await my_channel.send(embed=embed)
    await my_channel.send(embed=embed)

@bot.event
async def on_member_join(member):
    cursor.execute(f"SELECT id FROM users WHERE id={member.id}")#все также, существует ли участник в БД
    if cursor.fetchone()==None:#Если не существует
        cursor.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@{member.id}>', 0, 0)")
        print(f'{member.name} успешно записан в базу данных')
    else:#Если существует
        print(f'{member.name} уже занесён в базу данных, запрос отклонён')
        pass
    conn.commit()#применение изменений в БД

@bot.command()
async def profile(ctx): #команда _account (где "_", ваш префикс указаный в начале)
    for row in cursor.execute(f"SELECT mention,codemoney,buildmoney FROM users where id={ctx.author.id}"):
        embed = discord.Embed(
            title='Профиль сотрудника CreaTeam',
            description=f'''Пользователь: {row[0]}
            
Очков строительства: **{row[2]} :bricks:**
Очков кодинга: **{row[1]} :wrench:**

Введите ;level для повышения''',
            colour=0x5d275d
        )
        await ctx.send(embed=embed)

@bot.command()
async def addscore(ctx, arg1, arg2, arg3):
    if ctx.author.guild_permissions.administrator:
        if arg3 == 'dev':
            for row in cursor.execute(f"SELECT codemoney FROM users WHERE id={arg1}"):
                addscores = row[0] + int(arg2)
                cursor.execute(f'UPDATE users SET codemoney={addscores} WHERE id={arg1}')
                await ctx.send(f'Успешно зачислено {arg2} очков кодинга пользователю <@!{arg1}>')
        elif arg3 == 'build':
            for row in cursor.execute(f"SELECT buildmoney FROM users WHERE id={arg1}"):
                addscores = row[0] + int(arg2)
                cursor.execute(f'UPDATE users SET buildmoney={addscores} WHERE id={arg1}')
                await ctx.send(f'Успешно зачислено {arg2} очков строительства пользователю <@!{arg1}>')
        else:
            await ctx.send("Неверный тип очков. Допустимые: **dev**, **build**")
    else:
        await ctx.send("**Отказ:** Нет прав для использования данной команды.")
    conn.commit()

@bot.command()
async def level(ctx):
    member = ctx.author
    guild = ctx.guild

    minorcoder = get(guild.roles, id=693891856454516737)
    juniorcoder = get(guild.roles, id=680486225639243816)
    seniorcoder = get(guild.roles, id=680486591890063433)
    majorcoder = get(guild.roles, id=875365606025723974)

    minorbuilder = get(guild.roles, id=693892009790013502)
    juniorbuilder = get(guild.roles, id=680486557379330057)
    seniorbuilder = get(guild.roles, id=680486731623301171)
    majorbuilder = get(guild.roles, id=875365470470045737)

    if minorcoder in member.roles:
        await ctx.send('''  Должность: **Coder**
Ранг: **Minor** (1/4)
        
Следующий ранг: **Junior**
Цена повышения: **500** :wrench:
        
Для повышения напиши ;upgrade code''')

    if juniorcoder in member.roles:
        await ctx.send('''  Должность: **Coder**
Ранг: **Junior** (2/4)

Следующий ранг: **Senior**
Цена повышения: **1000** :wrench:

Для повышения напиши ;upgrade code''')

    if seniorcoder in member.roles:
        await ctx.send('''  Должность: **Coder**
Ранг: **Senior** (3/4)

Следующий ранг: **Major**
Цена повышения: **2500** :wrench:

Для повышения напиши ;upgrade code''')

    if majorcoder in member.roles:
        await ctx.send('''  Должность: **Coder**
Ранг: **Major** (4/4 - MAX)
Ты достиг наилучшего звания в данной должности, мои поздравления!''')


    if minorbuilder in member.roles:
        await ctx.send('''  Должность: **Builder**
Ранг: **Minor** (1/4)

Следующий ранг: **Junior**
Цена повышения: **500** :bricks:

Для повышения напиши ;upgrade build''')

    if juniorbuilder in member.roles:
        await ctx.send('''  Должность: **Builder**
Ранг: **Junior** (2/4)

Следующий ранг: **Junior**
Цена повышения: **1000** :bricks:

Для повышения напиши ;upgrade build''')

    if seniorbuilder in member.roles:
        await ctx.send('''  Должность: **Builder**
Ранг: **Senior** (3/4)

Следующий ранг: **Major**
Цена повышения: **2500** :bricks:

Для повышения напиши ;upgrade build''')

    if majorbuilder in member.roles:
        await ctx.send('''  Должность: **Builder**
Ранг: **Major** (4/4 - MAX)*
Ты достиг наилучшего звания в данной должности, мои поздравления!''')

@bot.command(name='upgrade', pass_context=True)
async def upgrade(ctx, arg1):

    member = ctx.author.id
    amember = ctx.author
    guild = ctx.guild

    minorcoder = get(guild.roles, id=693891856454516737)
    juniorcoder = get(guild.roles, id=680486225639243816)
    seniorcoder = get(guild.roles, id=680486591890063433)
    majorcoder = get(guild.roles, id=875365606025723974)

    minorbuilder = get(guild.roles, id=693892009790013502)
    juniorbuilder = get(guild.roles, id=680486557379330057)
    seniorbuilder = get(guild.roles, id=680486731623301171)
    majorbuilder = get(guild.roles, id=875365470470045737)

    if arg1 == 'code':
            for row in cursor.execute(f"SELECT codemoney FROM users WHERE id={member}"):
                money = row[0]
                if minorcoder in amember.roles:
                    if money >= 500:
                        money -= 500
                        await amember.add_roles(juniorcoder)
                        await amember.remove_roles(minorcoder)
                        await ctx.send('''Твой ранг успешно улучшен!
Minor Coder ->->-> **Junior Coder**''')
                        cursor.execute('UPDATE users SET codemoney=? WHERE id=?',(money,member))
                    elif money < 500:
                        await ctx.send(f'Не хватает {500 - money} :wrench:')
                elif juniorcoder in amember.roles:
                    if money >= 1000:
                        money -= 1000
                        await amember.add_roles(seniorcoder)
                        await amember.remove_roles(juniorcoder)
                        await ctx.send('''Твой ранг успешно улучшен!
Junior Coder ->->-> **Senior Coder**''')
                        cursor.execute('UPDATE users SET codemoney=? WHERE id=?',(money,member))
                    elif money < 1000:
                        await ctx.send(f'Не хватает {1000 - money} :wrench:')
                elif seniorcoder in amember.roles:
                    if money >= 2500:
                        money -= 2500
                        await amember.add_roles(majorcoder)
                        await amember.remove_roles(seniorcoder)
                        await ctx.send('''Твой ранг успешно улучшен!
Senior Coder ->->-> **MAJOR CODER**
Ты достиг наилучшего ранга в данной должности, поздравляю!''')
                        cursor.execute('UPDATE users SET codemoney=? WHERE id=?',(money,member))
                    elif money < 2500:
                        await ctx.send(f'Не хватает {2500 - money} :wrench:')
                elif majorcoder in amember.roles:
                    await ctx.send('Ты достиг наилучшего звания, дальше - некуда. Спасибо за работу в команде CreaTeam, продолжай в том же духе! :star_struck:')
                else:
                    await ctx.send('Ты не являешься кодером команды CreaTeam.')
            conn.commit()

    elif arg1 == 'build':
            for row in cursor.execute(f"SELECT buildmoney FROM users WHERE id={member}"):
                money = row[0]
                if minorbuilder in amember.roles:
                    if money >= 500:
                        money -= 500
                        await amember.add_roles(juniorbuilder)
                        await amember.remove_roles(minorbuilder)
                        await ctx.send('''Твой ранг успешно улучшен!
Minor Builder ->->-> **Junior Builder**''')
                        cursor.execute('UPDATE users SET buildmoney=? WHERE id=?', (money, member))
                    elif money < 500:
                        await ctx.send(f'Не хватает {500 - money} :bricks:')
                elif juniorbuilder in amember.roles:
                    if money >= 1000:
                        money -= 1000
                        await amember.add_roles(seniorbuilder)
                        await amember.remove_roles(juniorbuilder)
                        await ctx.send('''Твой ранг успешно улучшен!
Junior Builder ->->-> **Senior Builder**''')
                        cursor.execute('UPDATE users SET buildmoney=? WHERE id=?', (money, member))
                    elif money < 1000:
                        await ctx.send(f'Не хватает {1000 - money} :bricks:')
                elif seniorbuilder in amember.roles:
                    if money >= 2500:
                        money -= 2500
                        await amember.add_roles(majorbuilder)
                        await amember.remove_roles(seniorbuilder)
                        await ctx.send('''Твой ранг успешно улучшен!
Senior Builder ->->-> **MAJOR BUILDER**
Ты достиг наилучшего ранга в данной должности, поздравляю!''')
                        cursor.execute('UPDATE users SET buildmoney=? WHERE id=?', (money, member))
                    elif money < 2500:
                        await ctx.send(f'Не хватает {2500 - money} :bricks:')
                elif majorbuilder in amember.roles:
                    await ctx.send(
                        'Ты достиг наилучшего звания, дальше - некуда. Спасибо за работу в команде CreaTeam, продолжай в том же духе! :star_struck:')
                else:
                    await ctx.send('Ты не являешься строителем команды CreaTeam.')
            conn.commit()

    else:
        await ctx.send('Неверная должность. Допустимые: **code**, **build**')

@bot.command(name='status')
async def status(ctx):
    embed = discord.Embed(
        title = 'Состояние CreaBot',
        description = f'''**Пинг:** {round(bot.latency * 1000)}ms''',
        colour = 0x173b47
    )
    await ctx.send(embed=embed)

bot.run(TOKEN)
