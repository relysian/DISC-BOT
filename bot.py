# bot.py
#################################################################
import os
import discord
from PIL import Image
import io
from icalparse import parse_ical
import sched, time
from datetime import datetime
from discord.ext.commands import cooldown
from discord.ext import tasks, commands
import random as random
from emojilist import elist
from wakari import urlshort
from mcstats import mcstat
import asyncio
#################################################################
global lecturetime, ls
GUILD = '760098399869206529'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='|',intents=intents)
ls=elist()
c=False
#################################################################
urlfile=open("urlkey.csv", mode="r").read().split("\n")
urlkey=[]
for x in urlfile:
    urlkey.append(x.split(","))
del urlkey[-1]
#################################################################

future =[]
tmpvar=""
lecturetime=False

global future6
#################################################################

print(time.time())
scheduler = sched.scheduler(time.time, time.sleep)
##################################################################
def richifier(future6):  ## future 5 is [unix,online delivery,course desc, course code]
    global lecturetime
    for count,each in enumerate(future6):        #adding +[course info url] at [4]
        for x in urlkey:
            if x[0]==each[3]:
                future6[count].append(x[1])
        if each[3]=="COMP1202" and datetime.fromtimestamp(each[0]).strftime("%A")=="Friday":    ##adds context to each lecture
            future6[count][1]="Space Cadets"
            future6[count].append("https://teams.microsoft.com/l/channel/19%3aa96eb5721aef41099e19690b93c27ab7%40thread.tacv2/Space%2520Cadets%2520(Fri%252016-18)?groupId=143e2cc4-76a6-42e4-95d9-a25c1afd59f6&tenantId=4a5378f9-29f4-4d3e-be89-669d03ada9d8")                                                    ##ALSO adds the link to slot [5]
        elif each[3]=="COMP1202" and datetime.fromtimestamp(each[0]).strftime("%A")=="Monday":
            future6[count][1]="FAQ Session"
            future6[count].append("https://waa.ai/u6DT")
        elif each[3]=="COMP1202" and datetime.fromtimestamp(each[0]).strftime("%A")=="Thursday":
            future6[count][1]="Labs"
            future6[count].append("https://waa.ai/u6D3")
        elif each[3]=="COMP1215" and (datetime.fromtimestamp(each[0]).strftime("%A")=="Friday" or datetime.fromtimestamp(each[0]).strftime("%A")=="Monday"):
            future6[count][1]="Excerise sheet help/Discussion"
            future6[count].append("https://blackboard.soton.ac.uk/webapps/collab-ultra/tool/collabultra?course_id=_190675_1&mode=view")
        elif each[3]=="COMP1205"and datetime.fromtimestamp(each[0]).strftime("%A")=="Monday":
            future6[count][1]="Group Project with Sarah (meeting now on BB)"
            future6[count].append("https://waa.ai/uNPW")
        elif each[3]=="COMP1205":
            future6[count][1]="see homepage for info (NO LINK TO MEETING (SHOULD BE ON TEAMS))"
            future6[count].append("https://waa.ai/udrj")
        elif each[3]=="COMP1203" and datetime.fromtimestamp(each[0]).strftime("%A")=="Friday":
            future6[count][1]="Q&A session/summarise the week's lectures"
            future6[count].append("https://blackboard.soton.ac.uk/webapps/collab-ultra/tool/collabultra?course_id=_191256_1&mode=cpview")
        elif each[3]=="COMP1203" and datetime.fromtimestamp(each[0]).strftime("%A")=="Monday":
            future6[count][1]="To help with our RasPi coursework (doesn't exist yet so no URL)"
            future6[count].append("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        else:
            continue
    return future6
###################################################################






###################################################################
class DiscordBot():
    @bot.event
    async def on_ready():
        bot.add_cog(MyCog())
        print(bot.user)
#####################################################
    @bot.command(name='emlist')
    async def emlist(ctx, *args):
        global ls
        ls=elist()
        print("emojilist reloaded")
######################################################
    @bot.command(name='cumlord',pass_context = True)
    async def cumlord(ctx):
        print("A coomer tried to Coom")
        c=False
        for x in ctx.message.author.roles:
            if x.id == 765936114841288855:
                c=True
                break
            else:
                pass
        if c==False:
            print("They Succeeded")
            await ctx.message.author.add_roles(bot.get_guild(int(GUILD)).get_role(765936114841288855))
            await ctx.message.channel.send(ctx.message.author.name + " has Coomed")
        c=False
#####################################################
    @cooldown(1,600)
    @bot.command(name='next5',pass_context = True)
    async def next5(ctx):
        for x in richifier(parse_ical()):
            await ctx.message.channel.send("Date: "+datetime.utcfromtimestamp(x[0]).strftime('%Y-%m-%d %H:%M:%S')+"\nLecture: "+str(x[2]))
#################################################

    @bot.command(name='flip',pass_context = True)
    async def flip(ctx):
        if random.randint(0,1) == 1:
            await ctx.message.channel.send("Heads")
        else:
            await ctx.message.channel.send("Tails")
########################################################
    @bot.command(name='do',pass_context = True)
    async def do(ctx, *, arg):
            await ctx.message.channel.send("Kettle-BOT did "+ discord.utils.escape_mentions(str(arg)))
#######################################################################

    @bot.command(name='bonk',pass_context = True)
    async def bonk(ctx, *, arg):
            await ctx.message.channel.send(discord.utils.escape_mentions(str(arg))+" was Bonked!!")
#######################################################################

    @bot.command(name='pp')
    async def help(ctx):
            await ctx.message.channel.send("Kettle-BOT Helped!")


#####################################################
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        elif random.randint(0,690) == 42:
            print("Someone got Lucky")
            await message.channel.send("Kettle-BOT is always watching")
        await bot.process_commands(message)
#######################################################
    @bot.event
    async def on_raw_reaction_add(payload):

        for each in ls:
            if str(payload.message_id) == each[1]:  ##idk tbh
                if str(payload.emoji.id) == each[0] or payload.emoji.name == each[0]:
                    await payload.member.add_roles(bot.get_guild(payload.guild_id).get_role(int(each[2])))
                    print(payload.member.name + " " +each[3])
##########################################################
    @bot.event
    async def on_raw_reaction_remove(payload):
        guild=bot.guilds[0]

        for each in ls:
            if str(payload.message_id) == each[1]:
                if str(payload.emoji.id) == each[0] or str(payload.emoji.name)==each[0]:
                    await guild.get_member(payload.user_id).remove_roles(guild.get_role(int(each[2])))
                    print(guild.get_member(payload.user_id).name + " " + each[4])
#####################################################################################

class MyCog(commands.Cog):
    def __init__(self):
        self.index = 0
        self.timecheck.start()
        self.editmcstat.start()
#########################################################################################
    def cog_unload(self):
        self.timecheck.cancel()
##########################################################################################
    @tasks.loop(count=None)
    async def createmsg(self,futurenow):
        global lecturetime
        embedVar = discord.Embed(title=("Lecture: "+ futurenow[2] + "  in "+str(round(((time.time()-futurenow[0])/60)))+ "mins"), description=futurenow[1], color=0x16C500)
        embedVar.add_field(name="Dear, ", value="""<@&764601237986738197>""", inline=False)
        embedVar.add_field(name="Course Homepage", value="[HERE]"+"("+("https://waa.ai/"+urlshort(futurenow[4]))+")", inline=False)
        embedVar.add_field(name="Online Lecture Location", value="[Click here to go to the Lecture (if available)]"+"("+("https://waa.ai/"+urlshort(futurenow[5]))+")", inline=False)
        if futurenow[3]=="COMP1202":
            embedVar.set_thumbnail(url="https://i.imgur.com/eRgMUFx.png")
            embedVar.add_field(name="For more info please go to", value="""<#764590654448861185>""", inline=False)
        elif futurenow[3]=="COMP1203":
            embedVar.set_thumbnail(url="https://i.imgur.com/TR6iwwz.png")
            embedVar.add_field(name="For more info please go to", value="""<#764590676049395723>""", inline=False)
        elif futurenow[3]=="COMP1205":
            embedVar.set_thumbnail(url="https://i.imgur.com/3l2tbv7.gif")
            embedVar.add_field(name="For more info please go to", value="""<#764590696128446484>""", inline=False)
        elif futurenow[3]=="COMP1215":
            embedVar.set_thumbnail(url="https://i.imgur.com/bFvcT3Y.png")
            embedVar.add_field(name="For more info please go to", value="""<#764590723545694248>""", inline=False)
        else:
            embedVar.set_thumbnail(url="https://i.imgur.com/8LQCEa7.png")
            embedVar.add_field(name="For more info please go to", value="""<#762719395763322960>""", inline=False)
        await bot.get_channel(764657412585816084).send(embed=embedVar)
        await asyncio.sleep(600)
        lecturetime=False
        self.createmsg.stop()
#####################################################################################################

    @tasks.loop(seconds=60.0)
    async def timecheck(self):
        global lecturetime
        global future,future5,lecturetime,future6
        future=[]
        future=parse_ical()
        future=richifier(future)
        #print(future)
        if future[0][0]-int(time.time())<=600 and future[0][0]-int(time.time())>0 and lecturetime==False:
            lecturetime=True
            print("lecture")
            self.createmsg.start(future[0])
        else:
            pass
###############################################################################################

    @tasks.loop(seconds=60.0)
    async def editmcstat(self):
        mc=mcstat()
        ebvar = discord.Embed(title=("Minecraft server Stats"), description="Running: "+ mc[3], color=0x16C500)
        mplay =""
        for each in mc[1].get("list"):
            mplay+= str(each) + "\n"
        mplay = mplay[:-1]

        ebvar.add_field(name="Online?", value=mc[0], inline=False)
        ebvar.add_field(name="IP:", value=mc[2], inline=False)
        ebvar.add_field(name="Players:", value=str(mc[1].get("online"))+" out of "+str(mc[1].get("max"))+ " online.", inline=False)
        ebvar.add_field(name="List:", value=mplay, inline=False)
        msg=await bot.get_channel(760099567391342653).fetch_message(767124576542785556)
        await msg.edit(content = None, embed=ebvar)







####################################################################################
bot.run(open("key.txt", "r").read(), reconnect=True)
