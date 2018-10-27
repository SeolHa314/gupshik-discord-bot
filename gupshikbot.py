import discord
import asyncio
import datetime

import getgupshik

gupshikbot = discord.Client()
token = ""

schoolcode = ""
try:
	credentialfile = open("./credential.txt")
	token = credentialfile.read()[:-1]
except FileNotFoundError:
	print("you should make credential.txt file on root folder containing only token")
else:
	pass


@gupshikbot.event
async def on_ready():
	print("logged in as")
	print(gupshikbot.user.name)
	print(gupshikbot.user.id)
	print("-" * 20)

@gupshikbot.event
async def on_message(message):
	global schoolcode
	if message.content.startswith("!test"):
		await gupshikbot.send_message(message.channel, "this is working!!")

	elif message.content.startswith('!set'):
		await gupshikbot.send_message(message.channel, "please input school code")
		code = await gupshikbot.wait_for_message(timeout = 15.0, author = message.author)

		if code is None:
			await gupshikbot.send_message(message.channel, 'pls enter in 15 sec')
			return
		else:
			schoolcode = code.content
			await gupshikbot.send_message(message.channel, "your school code is {}".format(schoolcode))

	elif message.content.startswith('!todaygupshik'):
		text = getgupshik.loadgupshikdata(schoolcode, datetime.date.today().day)
		if len(text) < 2:
			await gupshikbot.send_message(message.channel, "you cannot eat gupshik today")
		else:
		    await gupshikbot.send_message(message.channel, text)

	elif message.content.startswith("!gupshik"):
		await gupshikbot.send_message(message.channel, "input day you want to see")
		selectedDay = await gupshikbot.wait_for_message(timeout = 15.0, author = message.author)

		if selectedDay is None:
			await gupshikbot.send_message(message.channel, "input in 15 sec")
			return
		else:
			text = getgupshik.loadgupshikdata(schoolcode, int(selectedDay.content))
			if len(text) < 2:
				await gupshikbot.send_message(message.channel, "you cannot eat gupshik that day")
			else:
				await gupshikbot.send_message(message.channel, text)


gupshikbot.run(token)
