from dotenv import load_dotenv
import discord
from enum import Enum
import os
from app.chatgpt_ai.openai import chatgpt_response, chatgpt_image
import asyncio

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')

# This will load the permissions the bot has been granted in the previous configuration
intents = discord.Intents.default()
intents.message_content = True

class aclient(discord.Client):
  def __init__(self):
    super().__init__(intents = intents)
    self.synced = False # added to make sure that the command tree will be synced only once
    self.added = False

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced: #check if slash commands have been synced 
      await tree.sync() #guild specific: you can leave sync() blank to make it global. But it can take up to 24 hours, so test it in a specific guild.
      self.synced = True
    if not self.added:
      self.added = True
    print(f"Say hi to {self.user}!")
    channel = self.get_channel('Channel ID for bot status.')
    await channel.send("🟢 Bot is now Online!")

client = aclient()
tree = discord.app_commands.CommandTree(client)

@tree.command(description='Ask a question to the bot and get a response.')
async def chat(interaction: discord.Interaction, prompt: str):
    user = interaction.user.id
    await interaction.response.defer()
    bot_response = chatgpt_response(prompt=prompt)
    await interaction.followup.send(f'<@{user}>! {bot_response}')

@tree.command(description='Generates an image based on your prompt')
async def generate(interaction: discord.Interaction, prompt: str):
    user = interaction.user.id
    await interaction.response.defer()
    bot_response = chatgpt_image(prompt=prompt)
    await interaction.followup.send(f'<@{user}>!: {prompt}\n{bot_response}')
    


@client.event
async def on_message(message):
  # This checks if the message is not from the bot itself. If it is, it'll ignore the message.
  if message.author == client.user:
    return

  # From here, you can add all the rules and the behaviour of the bot.
  # In this case, the bot checks if the content of the message is "Hello!" and send a message if it's true.
  if message.content == 'Hello!':
    await message.channel.send("Hello! I'm happy to see you around here.")
    return

  if message.content == 'Good bye!':
    await message.channel.send("Hope to see you soon!")
    return