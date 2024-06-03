import disnake
from disnake.ext import commands
from image import DiscordMessageImage
import io

intents = disnake.Intents.default()
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.slash_command(description="Generate an image from a user ID and text")
async def generate(interaction: disnake.ApplicationCommandInteraction, userid: str, text: str):
    await interaction.response.defer()
    
    user_id = str(userid)
    message = text
    discord_message_image = DiscordMessageImage(user_id, message)
    image = discord_message_image.create_image()

    with io.BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await interaction.followup.send(content="",file=disnake.File(fp=image_binary, filename='message.png'))

bot.run('')
