import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import openai
import io
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

API_KEY = 'open api key'
openai.api_key = API_KEY


@bot.command()
async def generate(ctx, *, text):
    # Ustawienie czcionki i rozmiaru tekstu
    font = ImageFont.truetype("arial.ttf", 36)

    
    image = Image.new('RGB', (400, 200), color = (73, 109, 137))

    
    draw = ImageDraw.Draw(image)

    
    textwidth, textheight = draw.textsize(text, font)
    x = (image.width - textwidth) / 2
    y = (image.height - textheight) / 2
    draw.text((x, y), text, font=font, fill=(255, 255, 0))

    
    with io.BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(image_binary, filename='image.png'))


@bot.command()
async def ask(ctx, *, question):
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Q: {question}\nA:",
        max_tokens=100,
        temperature=0.5,
        n=1
    )


    answer = response.choices[0].text.strip()
    await ctx.send(answer)


bot.run('your token')
