# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import random
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import requests
import urllib3
import arksearch
import json
from terminaltables import AsciiTable

client = Bot(description="TechBot by eragon5779#1448", command_prefix="$", pm_help = False)

@client.event
async def on_ready():
        print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=121920'.format(client.user.id))
        return await client.change_presence(game=discord.Game(name='Providing Tech Help')) #This is buggy, let us know if it doesn't work.


@client.event
async def on_message(message) :
	if message.author == client.user :
		return
    
	if message.content.startswith(client.command_prefix + "intel") :
		await client.send_message(message.channel, 'Please enter model you want to search for (i.e. 6700)')

		msg = await client.wait_for_message(author=message.author)

		ark_json = arksearch.quick_search(msg.content)
		if len(ark_json) < 1:
			await client.send_message(message.channel, 'Could not find any processors')
			return

		await client.send_message(message.channel, u"Processors found: {0}".format(len(ark_json)))

		choice_dict = {}
		counter = 0
		cpuList = ""
		for cpu in ark_json:
			choice_dict[counter] = cpu['id']
			cpuList += (u"[{0}] {1}\n".format(counter, cpu['value']))
			counter += 1
		await client.send_message(message.channel, cpuList)

		if len(ark_json) > 1:
			await client.send_message(message.channel, "Which CPU do you want?")
			msg = await client.wait_for_message(author=message.author)
			choice = int(msg.content)
		else:
			choice = 0
		
		searchTerm = "https://odata.intel.com/API/v1_0/Products/Processors()?&$filter=ProductId eq %s&$format=json" % choice_dict[int(choice)]
		searchTerm.replace(' ',"%20")
		cpu_data = requests.get(searchTerm).text

		# split the data to [48:227]

		def pp_json(json_thing, sort=True, indents=4):
			if type(json_thing) is str:
				return(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
			else:
				return(json.dumps(json_thing, sort_keys=sort, indent=indents))

		cpu_data = pp_json(cpu_data, False)

		cpu_data = cpu_data.split('\n')[48:227]
		cpu_data = '\n'.join(cpu_data)
		cpu_data = '{\n' + cpu_data + '\n}'
		cpu_data = pp_json(cpu_data)
		cpu_data = json.loads(cpu_data)

		wantedData = ['ProductName','CoreCount','ThreadCount',
					  'ClockSpeed','ClockSpeedMax','Cache','MaxTDP',
					  'BornOnDate','MaxMem','Lithography',
					  'SocketsSupported','ScalableSockets']

		userOut = "```"

		for need in wantedData :
			spaces = 16 - len(need)
			userOut += ' ' * spaces
			userOut += need + ': ' + str(cpu_data[need]) + '\n'
		userOut += "```"

		await client.send_message(message.channel, userOut)

key = open(".bot.key", "r")

client.run(key.read(59))

key.close()