import json

import discord

bot = discord.Bot()

if __name__ == "__main__":
    config = json.load(open("config.json"))
    bot.load_extension("cogs.RandomAdvancement")
    bot.load_extension("cogs.AdvancementInfo")
    bot.run(config["token"])
