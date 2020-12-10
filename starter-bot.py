import os

from discord.ext import commands
import psutil

from dotenv import load_dotenv
from asyncio import sleep

load_dotenv()
token = os.getenv("TOKEN")
execution_command = os.getenv("EXEC-COMMAND")
pre_stop_command = os.getenv("PRE-STOP")
stop_command = os.getenv("STOP-COMMAND")

def exec():
    if not process_name in (p.name() for p in psutil.process_iter()):
        return os.system("\"{}\"".format(execution_command))
    else:
        return 100

def stop():
    return_code = os.system("\"{}\"".format(pre_stop_command))
    if not return_code:
        return os.system("\"{}\"".format(stop_command))
    else:
        return return_code

def add_op(discriminator):
    file = open("ops", "a")
    file.write("{}\n".format(discriminator))
    file.close()

def ops():
    file = open("ops", "r")
    ops = file.read()
    file.close()
    return ops.split("\n")

def remove_op(discriminator):
    op_list = ops()
    op_list.remove(discriminator)
    file = open("ops", "w")
    for op in op_list:
        file.write(op + "\n")
    file.close()

async def check_op(ctx):
    if ctx.author.discriminator in ops():
        return True
    else:
        await ctx.send("You are not authorized!")
        return False

bot = commands.Bot(command_prefix='!')

@bot.command()
async def start(ctx):
    await ctx.send("Starting...")
    result = exec()
    if not result :
        await ctx.send("Started!")
    elif result == 100 :
        await ctx.send("Already running!")
    else:
        await ctx.send("Start was not successfull!")

@bot.command()
async def op(ctx, discriminator):
    if await check_op(ctx):
        add_op(discriminator)
        await ctx.send("Added {} to operator list!".format(discriminator))

@bot.command()
async def deop(ctx, discriminator):
    if await check_op(ctx):
        remove_op(discriminator)
        await ctx.send("Removed {} from operator list!".format(discriminator))

@bot.command()
async def restart(ctx):
    if await check_op(ctx):
        if not stop():
            await ctx.send("Stopped server!")
            await start(ctx)
        else:
            await ctx.send("Could not stop server!")

bot.run(token)
