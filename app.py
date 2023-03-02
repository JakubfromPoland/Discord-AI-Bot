import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import openai
import io
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

API_KEY = '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'
openai.api_key = API_KEY

# Utworzenie komendy, która generuje obraz z tekstu
@bot.command()
async def generate(ctx, *, text):
    # Ustawienie czcionki i rozmiaru tekstu
    font = ImageFont.truetype("arial.ttf", 36)

    # Utworzenie obrazu o wymiarach 400x200 pikseli
    image = Image.new('RGB', (400, 200), color = (73, 109, 137))

    # Utworzenie obiektu ImageDraw, który pozwoli na rysowanie tekstu na obrazie
    draw = ImageDraw.Draw(image)

    # Ustawienie pozycji i koloru tekstu, a następnie narysowanie go na obrazie
    textwidth, textheight = draw.textsize(text, font)
    x = (image.width - textwidth) / 2
    y = (image.height - textheight) / 2
    draw.text((x, y), text, font=font, fill=(255, 255, 0))

    # Zapisanie obrazu w pamięci i przesłanie użytkownikowi jako załącznik wiadomości
    with io.BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(image_binary, filename='image.png'))

# Utworzenie komendy, która generuje odpowiedź z ChatGPT na podstawie podanego pytania
@bot.command()
async def ask(ctx, *, question):
    # Wygenerowanie odpowiedzi z ChatGPT na podstawie pytania
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Q: {question}\nA:",
        max_tokens=100,
        temperature=0.5,
        n=1
    )

    # Pobranie odpowiedzi z odpowiedzi z ChatGPT i wysłanie jej na czacie
    answer = response.choices[0].text.strip()
    await ctx.send(answer)

# Uruchomienie bota
bot.run('MTA4MDU4OTkxNzgwMjk5MTY2Ng.GreN7R.jm6UoN9fcGix3jfVEkzS3BqcrRUdGnMCjwTel4')
