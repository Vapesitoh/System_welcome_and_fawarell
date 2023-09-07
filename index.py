import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from web_server import run_web_server  # Importa la función desde web_server.py
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import requests
import random

# Token de tu bot
TOKEN = 'MTE0ODcyMTM3ODg2MjgzMzg0Ng.GskP-Q.yWJVUlUkuFUFWdUthToia3WGiJW-3WEJYyYzAY'

# Tu código del bot de Discord

# URL de la imagen de fondo
background_url_bienvenida = 'https://e1.pxfuel.com/desktop-wallpaper/90/671/desktop-wallpaper-anime-city-anime-backgrounds-city-anime.jpg'
background_url_despedida = 'https://s1.zerochan.net/Theresa.Apocalypse.600.3490572.jpg'

# ID del canal de bienvenida
welcome_channel_id = 1067122455753269359  # Reemplaza con el ID de tu canal de bienvenida

# ID del canal de despedida
farewell_channel_id = 1067122455753269359  # Reemplaza con el ID de tu canal de despedida

# Colores aleatorios para el círculo alrededor del avatar
circle_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Definir intents
intents = discord.Intents.default()
intents.members = True
intents.typing = False
intents.presences = True

# Crear una instancia del bot con los intents
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_member_join(member):
    welcome_channel = member.guild.get_channel(welcome_channel_id)
    
    if welcome_channel is None:
        return
    
    welcome_message = f'Bienvenido/a a Neptune, {member.mention}!'
    
    response = requests.get(background_url_bienvenida)
    background_image = Image.open(io.BytesIO(response.content))
    
    user_avatar_url = member.avatar.url
    response_avatar = requests.get(user_avatar_url)
    user_avatar = Image.open(io.BytesIO(response_avatar.content))
    
    mask = Image.new("L", user_avatar.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, user_avatar.width, user_avatar.height), fill=255)
    user_avatar.putalpha(mask)
    
    # Crear una copia de la imagen de fondo para aplicar el efecto de desenfoque
    blurred_background = background_image.copy()
    
    # Aplicar el efecto de desenfoque solo al contorno del fondo (4 píxeles)
    blurred_background = blurred_background.filter(ImageFilter.GaussianBlur(radius=4))
    
    # Agregar un círculo de color aleatorio alrededor del avatar
    draw = ImageDraw.Draw(blurred_background)
    circle_color = random.choice(circle_colors)
    circle_radius = 90  # Ajusta el radio del círculo según tus necesidades
    position = (350, 100)  # Posición en la imagen de fondo
    circle_center = (position[0] + user_avatar.width // 2, position[1] + user_avatar.height // 2)
    draw.ellipse((circle_center[0] - circle_radius, circle_center[1] - circle_radius,
                  circle_center[0] + circle_radius, circle_center[1] + circle_radius),
                 fill=circle_color, outline=circle_color)
    
    # Pegar la imagen del usuario (en círculo) en la imagen de fondo con desenfoque
    blurred_background.paste(user_avatar, position, user_avatar)
    
    font_path = "Daydream.ttf"
    font_size = 24
    font = ImageFont.truetype(font_path, font_size)
    
    text1 = f'Bienvenid@ A Neptune, {member.display_name}!'
    text2 = 'Recuerda leer las reglas.'
    draw.multiline_text((155, 400), text2, fill="black", font=font)
    draw.multiline_text((110, 300), text1, fill="black", font=font)

    image_buffer = io.BytesIO()
    blurred_background.save(image_buffer, format="JPEG")
    image_buffer.seek(0)
    
    await welcome_channel.send(welcome_message, file=discord.File(image_buffer, filename="welcome.jpg"))

@bot.event
async def on_member_remove(member):
    farewell_channel = member.guild.get_channel(farewell_channel_id)
    
    if farewell_channel is None:
        return
    
    welcome_message = f'Adios, {member.mention}!'
    
    response = requests.get(background_url_despedida)
    background_image = Image.open(io.BytesIO(response.content))
    
    user_avatar_url = member.avatar.url
    response_avatar = requests.get(user_avatar_url)
    user_avatar = Image.open(io.BytesIO(response_avatar.content))
    
    mask = Image.new("L", user_avatar.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, user_avatar.width, user_avatar.height), fill=255)
    user_avatar.putalpha(mask)
    
    blurred_background = background_image.copy()
    blurred_background = blurred_background.filter(ImageFilter.GaussianBlur(radius=4))
    
    draw = ImageDraw.Draw(blurred_background)
    circle_color = random.choice(circle_colors)
    circle_radius = 90
    position = (350, 100)
    circle_center = (position[0] + user_avatar.width // 2, position[1] + user_avatar.height // 2)
    draw.ellipse((circle_center[0] - circle_radius, circle_center[1] - circle_radius,
                  circle_center[0] + circle_radius, circle_center[1] + circle_radius),
                 fill=circle_color, outline=circle_color)
    
    blurred_background.paste(user_avatar, position, user_avatar)
    
    font_path = "Daydream.ttf"
    font_size = 26
    font = ImageFont.truetype(font_path, font_size)
    
    text1 = f'Adios de Neptune, {member.display_name}!'
    text2 = 'Esperamos volver a verte pronto'
    draw.multiline_text((55, 400), text2, fill="black", font=font)
    draw.multiline_text((100, 300), text1, fill="black", font=font)

    image_buffer = io.BytesIO()
    blurred_background.save(image_buffer, format="JPEG")
    image_buffer.seek(0)
    await farewell_channel.send(file=discord.File(image_buffer, filename="farewell.jpg"))

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')


bot.run(TOKEN)
