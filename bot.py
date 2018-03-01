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

amd = json.loads(open('specs.json').read())
intel = json.loads(open('intel.json').read())
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

		matching = []
		cpuList = ""
		count = 0
		for i in range(0, len(intel['d'])) :
			if msg.content.lower() in intel['d'][i]['ProductName'].lower() :
				matching.append(i)
				cpuList += '[%d] %s\n' % (count,intel['d'][i]['ProductName'])
				count += 1

		if len(cpuList) < 1 :
			await client.send_message(message.channel, "No processors found")
			return
		try :
			await client.send_message(message.channel, cpuList)
		except :
			await client.send_message(message.channel, 'Error: List too large. Please refine search.')
			return
		choice = 0
		if count > 1 :
			await client.send_message(message.channel, 'Which CPU do you want?')
			msg = await client.wait_for_message(author=message.author)
			choice = int(msg.content)
		wantedData = {
			'ProductName':'Name',
			'CoreCount':'Cores',
			'ThreadCount':'Threads',
			'ClockSpeed':'Base Clock',
			'ClockSpeedMax':'Boost Clock',
			'Cache':'Cache',
			'MaxTDP':'TDP',
			'BornOnDate':'Release Date',
			'MaxMem':'Max Memory',
			'Lithography':'Lithography',
			'SocketsSupported':'Socket',
			'ScalableSockets':'Multiple CPU'
		}
		userOut = "```"
		for need in wantedData.keys() :
			spaces = " " * (17 - len(wantedData[need]))
			userOut += spaces + ('%s: %s\n' % (wantedData[need],str(intel['d'][matching[choice]][need])))
			
		userOut += '```'

		await client.send_message(message.channel, userOut)

	if message.content.startswith(client.command_prefix + "amd") :
		await client.send_message(message.channel, 'Please enter model you want to search for (i.e. 1500)')

		msg = await client.wait_for_message(author=message.author)

		matching = []
		cpuList = ""
		count = 0
		for cpu in amd :
			if msg.content.lower() in amd[str(cpu)]['humanName'].lower() and amd[str(cpu)]['type'] == 'CPU' and amd[str(cpu)]['isPart']:
				matching.append(str(cpu))
				cpuList += '[%d] %s\n' % (count, amd[str(cpu)]['humanName'])
				count += 1

		if len(cpuList) < 1 :
			await client.send_message(message.channel, "No processors found")
			return
		try :
			await client.send_message(message.channel, cpuList)
		except :
			await client.send_message(message.channel, 'Error: List too large. Please refine search.')
			return
		choice = 0
		if count > 1 :
			await client.send_message(message.channel, 'Which CPU do you want?')
			msg = await client.wait_for_message(author=message.author)
			choice = int(msg.content)
		wantedData = {
			'humanName':'Name',
			'Core Count':'Cores',
			'Thread Count':'Threads',
			'Base Frequency':'Base Clock',
			'Boost Frequency':'Boost Clock',
			'L3 Cache (Total)':'Cache',
			'TDP':'TDP',
			'Release Date':'Release Date',
			'Lithography':'Lithography',
			'Socket':'Socket'
		}
		userOut = "```"
		for data in wantedData.keys() :
			spaces = " " * (17 - len(wantedData[data]))
			try :
				if data == 'humanName' :
					userOut += spaces + ('%s: %s\n' % (wantedData[data],str(amd[matching[choice]][data])))
				else :
					userOut += spaces + '%s: %s\n' % (wantedData[data],str(amd[matching[choice]]['data'][data]))
			except :
				pass
		userOut += '```'

		await client.send_message(message.channel, userOut)


key = open(".bot.key", "r")

client.run(key.read(59))

key.close()