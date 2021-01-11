import discord
import json
import random
from discord.ext import tasks

client = discord.Client()

with open('items.json') as json_file:
    items = json.load(json_file)

colors = {
    "Common": 0x559e58,
    "Uncommon": 0x626bcc,
    "Rare": 0x784399,
    "Exotic": 0x963535,
    "Legendary": 0xeb8c34,
    "Mythical": 0xfff64d
}

balances = {}

with open('balances.json') as json_file:
    balances = json.load(json_file)


@tasks.loop(seconds=1.0)
async def add_one_dollar_and_save():
    for k in balances.keys():
        balances[k] += 1
    with open('balances.json', 'w') as outfile:
        json.dump(balances, outfile)


add_one_dollar_and_save.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$open'):
        if balances.get(str(message.author.id), 'none') == 'none':
            balances[str(message.author.id)] = 25
            await message.channel.send(
                "Initial 25$ were added to your account. Type $open one more time to use them."
            )
        else:
            if balances[str(message.author.id)] >= 25:
                chosen_item = random.choice(items["i"])

                balances[str(message.author.id)] -= 25
                if chosen_item["rarity"] == "Common":
                    balances[str(message.author.id)] += random.randint(0, 5)
                elif chosen_item["rarity"] == "Uncommon":
                    balances[str(message.author.id)] += random.randint(5, 10)
                elif chosen_item["rarity"] == "Rare":
                    balances[str(message.author.id)] += random.randint(10, 20)
                elif chosen_item["rarity"] == "Exotic":
                    balances[str(message.author.id)] += random.randint(20, 40)
                elif chosen_item["rarity"] == "Legendary":
                    balances[str(message.author.id)] += random.randint(40, 80)
                elif chosen_item["rarity"] == "Mythical":
                    balances[str(message.author.id)] += random.randint(80, 200)

                embed = discord.Embed(
                    title=chosen_item["title"],
                    description=chosen_item["description"],
                    color=colors[chosen_item["rarity"]])
                embed.set_author(name="YOU GOT:")
                embed.set_thumbnail(url=chosen_item["image"])
                embed.set_footer(
                    text="Rarity: " + chosen_item["rarity"] +
                    ", Current Balance: $" + str(balances[str(message.author.id)]))
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(
                    "Sorry, but you don't have enough money. Type *$balance* to check your balance and remember that you get $1 passively every 15 minutes"
                )

    if message.content.startswith('$balance'):
        if balances.get(str(message.author.id), 'none') == 'none':
            balances[str(message.author.id)] = 25
            await message.channel.send(
                "Initial 25$ were added to your account. Type $open to use the money."
            )
        else:
            await message.channel.send(
                "Your balance is: $" + str(balances[str(message.author.id)]) +
                "\n(Remember that you get $1 passively every 15 minutes)")
    if message.content.startswith("$help"):
        await message.channel.send(
            "This bot allows people to open cases with various contents, giving users various perks.\n\n**$open** - open a case\n**$balance** - check the balance\n\nThis bot is made by russiniet"
        )


client.run('Nzk3MTMwODY4OTA0MDM0MzUy.X_h_-Q.yh61bZZ7cMbK9vr9ZGfYMpfmZ9A')
