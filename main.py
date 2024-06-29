import json

import disnake
from disnake.ext import commands

bot = commands.InteractionBot()

if __name__ == "__main__":
    config = json.load(open("config.json"))
    bot.load_extension("cogs.RandomAdvancement")
    bot.load_extension("cogs.AdvancementInfo")# Note: We did not append the .py extension.
    bot.run(config["token"])
