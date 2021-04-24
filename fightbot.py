# bot.py
import os
import random
from dotenv import load_dotenv
from fighter import Fighter

# 1
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 2
bot = commands.Bot(command_prefix='!')

enemy_dict = {'mook1' : Fighter('mook1', 2, 0, 0, 0, 10, 10, 0), 'mook2' : Fighter('mook2', 2, 3, 0, 0, 10, 5, 0), 'boss' : Fighter('boss', 4, 3, 4, 5, 12, 15, 4)}
protag = Fighter('protag', 5, 3, 3, 5, 11, 20, 3)

turnCounter = 0

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name = 'fight', help = 'input your fighter name to start fighting')
async def startFight(ctx, name: str):
    banned_names = ['boss', 'mook1', 'mook2']
    if name in banned_names:
        await ctx.send('name forbidden; please try another')
        return

    protag.setName(name)
    protag.setCombat(1)
    enemy_dict['mook1'].setCombat(1)
    enemy_dict['mook2'].setCombat(1)
    enemy_dict['boss'].setCombat(0)
    await ctx.send('Combat has started. Your enemies are mook1 and mook2. To attack, input command punch or magic')

@bot.command(name = 'punch', help = 'deals fair amount of damage')
async def punch_enemy(ctx, enemy: str):
    await ctx.invoke(bot.get_command('fightEnemyGeneralized'), en=enemy, type = 'attack')

@bot.command(name = 'magic', help = 'deals less damage but charges mana blast')
async def magic_enemy(ctx, enemy: str):
    await ctx.invoke(bot.get_command('fightEnemyGeneralized'), en=enemy, type = 'magic')

@bot.command(name = 'mana-blast', help = 'deals large amount of damage once fully charged')
async def mana_blast_enemy(ctx, enemy: str):
    await ctx.invoke(bot.get_command('fightEnemyGeneralized'), en=enemy, type = 'mana blast')

@bot.command(name = 'fightEnemyGeneralized')
async def fight_enemy_generalized(ctx, en: str, type = str):
    global turnCounter

    if protag.getAlive() == 0:
        await ctx.send('you are dead. use command restart to try again')
        return

    if not enemy_dict['boss'].getCombat():
        if en != 'mook1' and en != 'mook2':
            if en == protag.getName():
                await ctx.send('you cannot attack yourself')
            await ctx.send('please attack mook1 and mook2')
            return


    if enemy_dict['boss'].getCombat():
        if en != 'boss':
            await ctx.send('please attack the boss')
            return
        await ctx.send('bossfight')

    await ctx.send('turn ' + str(turnCounter))

    #protag attacks
    if type == 'attack':
        await ctx.send(protag.attack(enemy_dict[en], 0))
    elif type == 'magic':
        await ctx.send(protag.magic(enemy_dict[en], 2))
    elif type == 'mana blast':
        if protag.getCharged() == 0:
            await ctx.send(protag.manaBlast(enemy_dict[en]))
            #await ctx.send('boss setcombat = ' + str(enemy_dict['boss'].getCombat()))
        else:
            await ctx.send('mana blast not fully charged. choose another command')
            return
    await ctx.send(protag.getName() + ': ' + str(protag.getCharged()) + ' turns until mana blast fully charged')

    #if mook1 and mook2 have not been killed yet
    if enemy_dict['boss'].getCombat()==0:
        #mook1 attacks
        await ctx.send(enemy_dict['mook1'].attack(protag, 0))
        #mook2 attacks
        await ctx.send(enemy_dict['mook2'].attack(protag, 0))
    
        if not enemy_dict['mook1'].getAlive() and not enemy_dict['mook2'].getAlive():
            enemy_dict['boss'].setCombat(1)
            #await ctx.send('boss setcombat = ' + str(enemy_dict['boss'].getCombat()))
            await ctx.send('mook1 and mook2 have been defeated. starting from now, attack the boss')
            return
        await ctx.send('To attack, input command punch, magic, or mana-blast')

    #if mook1 and mook2 are dead, fight boss
    else:
        if not enemy_dict['boss'].getAlive():
            enemy_dict['boss'].setCombat(0)
            await ctx.send('you have won. use restart command to play again')
            return 

        if enemy_dict['boss'].getCharged==0:
            await ctx.send(enemy_dict['boss'].manaBlast(protag))
        else:
            await ctx.send(enemy_dict['boss'].magic(protag, 0))

        await ctx.send('boss: ' + str(enemy_dict['boss'].getCharged()) + ' turns until mana blast fully charged')
        await ctx.send('To attack, input command punch, magic, or mana-blast')
    turnCounter+=1







@bot.command(name = 'restart', help = 'input new fighter name to restart game')
async def restart_fight(ctx, name: str):
    global turnCounter
    turnCounter = 0
    enemy_dict['mook1'].setStats('mook1', 2, 0, 0, 0, 10, 10, 0)
    enemy_dict['mook2'].setStats('mook2', 2, 3, 0, 0, 10, 5, 0)
    enemy_dict['boss'] = Fighter('boss', 4, 3, 4, 5, 12, 15, 3)
    protag.setStats(name, 5, 3, 3, 5, 11, 20, 3)

    enemy_dict['mook1'].setCombat(1)
    enemy_dict['mook2'].setCombat(1)
    enemy_dict['boss'].setCombat(0)
    await ctx.send('Combat has restarted. Your enemies are mook1 and mook2. To attack, input command punch, magic, or mana blast (has chargetime)')

@bot.command(name = 'getStats', help = 'get stats of any character')
async def get_stats(ctx, name: str):
    if name == protag.getName():
        await ctx.send(protag.getStats())
    elif name not in enemy_dict.keys():
        await ctx.send('check name; must be your name, mook1, mook2, or boss')
    else:
        await ctx.send(enemy_dict[name].getStats())


bot.run(TOKEN)
