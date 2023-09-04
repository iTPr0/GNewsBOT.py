import discord
from discord.ext import commands, tasks
import os
import requests
from decouple import config
from discord import Embed

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

PREFIX = '!'
BOT_TOKEN = config('BOT_TOKEN')
GNEWS_API_KEY = config('GNEWS_API_KEY')

GNEWS_API_URL = 'https://gnews.io/api/v4/search'

target_channel_id = #id_do_canal_alvo

@bot.event
async def on_ready():
    print(f'Logado como {bot.user}!')

async def fetch_and_send_technology_news(target_channel, author):
    try:
        print('Buscando e enviando notícias de tecnologia...')

        response = requests.get(GNEWS_API_URL, params={
            'q': 'informática OR TI OR tecnologia da informação OR desenvolvimento de software OR cibersegurança OR hackers OR computação',
            'lang': 'pt',
            'country': 'BR',
            'token': GNEWS_API_KEY
        })

        articles = response.json()['articles']
        if articles:
            chunk_size = 3

            for i in range(0, len(articles), chunk_size):
                chunk = articles[i:i + chunk_size]

                for article in chunk:
                    embed = Embed(
                        title=article['title'],
                        description=article['description'],
                        color=0x0099ff
                    )
                    embed.set_footer(
                        text=f'Admin por {author.name} • Copyright © 2023',
                        icon_url=author.avatar.url if author.avatar else discord.Embed.Empty
                    )
                    embed.add_field(
                        name='Link:',
                        value=f'[Clique aqui]({article["url"]})'
                    )
                    embed.set_image(url=article['image'])

                    await target_channel.send(embed=embed)
        else:
            await target_channel.send('Nenhuma notícia de tecnologia encontrada.')
    except Exception as error:
        print('Erro ao buscar notícias de tecnologia:', error)
        await target_channel.send('Ocorreu um erro ao buscar notícias de tecnologia.')

@bot.command()
async def nf(ctx):
    print('Comando !nf recebido.')

    target_channel = discord.utils.get(ctx.guild.text_channels, id=target_channel_id)

    if target_channel:
        await fetch_and_send_technology_news(target_channel, ctx.author)
        await ctx.message.delete()
    else:
        print('Canal alvo não encontrado.')

@tasks.loop(seconds=30)
async def update_technology_news():
    target_channel = bot.get_channel(target_channel_id)

    if target_channel:
        await fetch_and_send_technology_news(target_channel, bot.user)

@update_technology_news.before_loop
async def before_update_technology_news():
    await bot.wait_until_ready()

bot.run(BOT_TOKEN)