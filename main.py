from time import perf_counter
from typing import Any
import discord
import os
import asyncio
import aiohttp
import youtube_dl
import wavelink
import DiscordUtils
import random
import datetime

from discord import client
from discord import webhook
from discord import permissions
from discord.enums import ChannelType
from discord.ext import commands, tasks
from discord.ext.commands.core import bot_has_permissions, bot_has_role, has_permissions
from discord.ext.commands.errors import MissingPermissions
from discord import Webhook
from dotenv import load_dotenv
from googletrans import Translator
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
from wavelink.ext import spotify

intents = discord.Intents.all()

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following guild:')

    for x in bot.guilds:
        print(f'{x.name}: {x.member_count}')
        
    bot.loop.create_task(node_connect())

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == 337528450409562132
    return commands.check(predicate)

@bot.command(name='sil', pass_context=True)
@has_permissions(manage_messages=True)
@bot_has_role('Winston')
async def delete_messages_24(ctx, amount=6):
    await ctx.channel.purge(limit=amount + 1)

@delete_messages_24.error
async def delete_messages_24_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('Mesaj silme yetkisine sahip değilsin!')

@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.guild.kick(member)
    await ctx.send(f'User {member} has been kick')

@bot.command(name='bilgi')
async def info(ctx, *, member: discord.Member):
    await ctx.send('{0} joined on {0.joined_at} and has {1} roles'.format(member, len(member.roles)))

@info.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Böyle birisini bulamıyorum...')

#mute command 
@bot.command(name='sustur', help='!sustur {\isim} {saniye}')
@bot_has_role('Winston')
async def mute(ctx, member: discord.Member=None, mute_time : int=None):
    if not member:
        await ctx.send("Kimi susturmak istiyorsun?")
        return
    if not mute_time:
        await ctx.send(f"Ne kadar süreliğine susturulsun {ctx.author.name} bey?")
        return
    await member.edit(mute=True)
    await ctx.send(f"{member.display_name} susturuldu.")

    await asyncio.sleep(mute_time)
    await member.edit(mute=False)
    await ctx.send(f"{member.display_name}\'ın susturulma süresi bitti.")

#mute command 
@bot.command(name='sağır')
@bot_has_role('Winston')
async def mute(ctx, member: discord.Member=None, mute_time : int=None):
    if not member:
        await ctx.send("Kimi sağır etmek istiyorsun?")
        return
    if not mute_time:
        await ctx.send(f"Ne kadar süreliğine sağır edilsin {ctx.author.name} bey?")
        return
    await member.edit(deafen=True)
    await ctx.send(f"{member.display_name} sağır edildi.")

    await asyncio.sleep(mute_time)
    await member.edit(deafen=False)
    await ctx.send(f"{member.display_name}\'ın sağır edilme süresi bitti.")

#titret command
@bot.command(name='titret')
async def moveplayer(ctx, member: discord.Member):
    channel1 = ctx.author.voice.channel
    channels = (c for c in ctx.guild.channels if c.type==ChannelType.voice and c!= channel1)
    for x in channels:
        await member.move_to(x)
    await member.move_to(channel1)

#unmute command
@bot.command(name='konuş')
async def  unmute(ctx, member: discord.Member=None):
    await member.edit(mute=False)
    await ctx.send(f"{member.display_name} susturulması sonlandırıldı.")


@bot.command()
@commands.is_owner()
async def leave_guild(ctx, *, guild_name):
    guild = discord.utils.get(bot.guilds, name=guild_name)
    await guild.leave()

#translator
@bot.command()
async def translate(ctx, lang, *, thing):
    translator = Translator()
    translation = translator.translate(thing, dest=lang)
    await ctx.send(translation.text)

@translate.error
async def translate_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send('Lütfen geçerli bir dil kullan.')

#Webhook
@bot.command()
async def foo(ctx, *, message: str):
    async with aiohttp.ClientSession() as session:
        #webhook = Webhook.partial(885459986489172019, '2uFEbz7Iu0WOr63GmtfDRuUPVjqQdSZyfZO2OdnYEBbvvQo4CVNwxsi80BdCX8-rPFOs', adapter=AsyncWebhookAdapter(session))
        #webhook = Webhook.partial(885460993063391263, 'CZ79W-YoWYJAjaPf7vapfo86AXzMLDvlZTv5sKkdskDdZYDO-xClK9Z0zKF6wurZP4ei', adapter=AsyncWebhookAdapter(session))
        #webhook = Webhook.partial(968602772951949402, 'TaM0K3Lnl2t6NYPNuJ9xWoRjCedEKnqtsz8rjzuzoZiy5F6dYb_iZRTk6dBoBIsOPQ_K', adapter=AsyncWebhookAdapter(session))
        #Kigel
        webhook = Webhook.partial(1054816357243441164, 'GPO685SwAn3ZgxFOTK7I9SnYfmKPRM6GMET-zN_7Cp50g2Vo3BZ6HAOVp_SnmY315HlY', session = session)
        #webhook = Webhook.partial(1054822523176484975, 'CIgwwkif3b6mKfkjQtD_1tiq-tZ8ZA2yy5wM1jqLyGoLARzMu1y8m_XI-QjjD-sqVccr', session = session)
        await webhook.send(content=message, username='Eren', avatar_url= "https://i.imgur.com/JHJ3SMJ.png")

@bot.command()
@is_owner()
async def m(ctx):
    webhook1 = await ctx.channel.create_webhook(name='deneme2')
    print(
        f'{webhook1.id} is id '
        f'{webhook1.token} is token'
    )

@bot.command()
@is_owner()
async def remrole(ctx, member: discord.Member):
    for role in ctx.guild.roles:
        if role.name == 'muted':
            await member.remove_roles(role)
            print('done')

@bot.command()
@has_permissions(manage_roles = True)
async def kayit(ctx, member: discord.Member, nick: str, age: str):
    role = discord.utils.find(lambda r: r.name == 'Kigelliler', ctx.message.guild.roles)
    
    if role in member.roles:
        await ctx.send("Üye zaten kayıtlı.")
        return

    for role in ctx.guild.roles:
        if role.name == 'Kigelliler':
            await member.add_roles(role)

    for role in ctx.guild.roles:
        if role.name == 'misafir':
            await member.remove_roles(role)

    await member.edit(nick= f"{nick} {age}")
    await ctx.send(f"{member.name} kaydı tamamlandı.")

@kayit.error
async def kayit_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("\{!kayit @etiket /isim /yaş\} şeklinde girmelisin.")

@bot.command()
async def kura(ctx, *,members):
    list1 = members.split()

    await ctx.send(random.choice(list1))

#@bot.command()
#@is_owner()
#async def chn(ctx):
#    while True:
#        if ctx.guild.get_member(859181482161078314).nick != 'sabri sikici':
#            await ctx.guild.get_member(859181482161078314).edit(nick='sabri sikici')
#            print('done.')
    
#@bot.event
#async def on_member_update(before, after):
#    guild = bot.get_guild(372049876520796180)
#    await guild.get_member(859181482161078314).edit(nick='özyurt sikici')

#@bot.event
#async def on_user_update(before, after):
#    guild = bot.get_guild(372049876520796180)
#    await guild.get_member(859181482161078314).edit(nick='özyurt sikici')

# Youtube
"""
@bot.command(pass_context=True, brief="Makes the bot join your channel", aliases=['j', 'jo'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await voice.disconnect()
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Joined {channel}")

@bot.command(pass_context=True, brief="Makes the bot leave your channel", aliases=['l', 'le', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send("Don't think I am in a voice channel")

@bot.command()
async def play(ctx, *, url):
    player = music.get_player(guild_id = ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix = True)

    if not ctx.voice_client.is_playing():
        await player.queue(url, search = True)
        song = await player.play()
        await ctx.send(f"{song.name} oynatılmaya başladı.")
    else:
        song = await player.queue(url, search = True)
        await ctx.send(f"{song.name} sıraya eklendi.")


@bot.command()
async def queue(ctx):
    player = music.get_player(guild_id = ctx.guild.id)
    await ctx.send(f"{','.join([song.name for song in player.current_queue()])}")

@bot.command
async def pause(ctx):
    player = music.get_player(guild_id = ctx.guild.id)
    song = await player.pause()
    await ctx.send(f"Paused {song.name}")

@bot.command
async def resume(ctx):
    player = music.get_player(guild_id = ctx.guild.id)
    song = await player.resume()
    await ctx.send(f"Resumed {song.name}")

@bot.command()
async def loop(ctx):
    player = music.get_player(guild_id = ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        return await ctx.send(f"{song.name} is looping!")
    else:
        return await ctx.send(f"{song.name} is not looping!")

@bot.command()
async def nowplaying(ctx):
    player = music.get_player(guild_id = ctx.guild.id)
    song = player.now_playing()
    await ctx.send(song.name)

@bot.command()
async def remove(ctx, index):
    player = music.get_player(guild_id = ctx.guild.id)
    song = await player.remove_from_queue(int(index))
    await ctx.send(f"Removed {song.name} from queue!")
"""

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} is ready!")

async def node_connect():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot, host='ssl.freelavalink.ga', port=443, password='www.freelavalink.ga', https= True, spotify_client=spotify.SpotifyClient(client_id="dfd63517d84e4fb58d25f4fd9638a091", client_secret="c76059d814f344b992c4b29136541701"))

@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.YouTubeTrack, reason):
    ctx = player.ctx
    vc: player = ctx.voice_client

    if vc.loop:
        return await vc.play(track)

    if vc.queue.is_empty:
        return

    next_song = vc.queue.get()
    await vc.play(next_song)
    await ctx.send(f"Now playing: {next_song.title}")

@bot.command()
async def play(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls = wavelink.Player)
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("İlk önce bir ses kanalına katıl.")
    elif not ctx.author.voice.channel == ctx.me.voice.channel:
        return await ctx.send("Aynı ses kanalında olmalıyız")
    else:
        vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty and not vc.is_playing():
        await vc.play(search)
        await ctx.send(f"{search.title} şu anda oynatılıyor.")
    else:
        await vc.queue.put_wait(search)
        await ctx.send(f"{search.title} sıraya eklendi.")
    
    vc.ctx = ctx
    setattr(vc, "loop", False)

@bot.command()
async def pause(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Herhangi bir ses kanalında değilim.")
    elif not ctx.author.voice:
        return await ctx.send("İlk önce bir ses kanalına katıl.")
    elif not ctx.author.voice.channel == ctx.me.voice.channel:
        return await ctx.send("Aynı ses kanalında olmalıyız")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.pause()
    await ctx.send("Şarkı duraklatıldı..")

@bot.command()
async def resume(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Herhangi bir ses kanalında değilim.")
    elif not ctx.author.voice:
        return await ctx.send("İlk önce bir ses kanalına katıl.")
    elif not ctx.author.voice == ctx.me.voice:
        return await ctx.send("Aynı ses kanalında olmalıyız")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.resume()
    await ctx.send("Şarkı devam ettiriliyor.")

@bot.command()
async def skip(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Herhangi bir ses kanalında değilim.")
    elif not ctx.author.voice:
        return await ctx.send("İlk önce bir ses kanalına katıl.")
    elif not ctx.author.voice.channel == ctx.me.voice.channel:
        return await ctx.send("Aynı ses kanalında olmalıyız")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.stop()
    await ctx.send("Sonraki şarkıya geçildi.")

@bot.command()
async def disconnect(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Herhangi bir ses kanalında değilim.")
    elif not ctx.author.voice:
        return await ctx.send("İlk önce bir ses kanalına katıl.")
    elif not ctx.author.voice.channel == ctx.me.voice.channel:
        return await ctx.send("Aynı ses kanalında olmalıyız")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.disconnect()

@bot.command()
async def loop(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Herhangi bir ses kanalında değilim.")
    elif not ctx.author.voice:
        return await ctx.send("İlk önce bir ses kanalına katıl.")
    elif not ctx.author.voice.channel == ctx.me.voice.channel:
        return await ctx.send("Aynı ses kanalında olmalıyız")
    else:
        vc: wavelink.Player = ctx.voice_client

    try:
        vc.loop ^= True
    except Exception:
        setattr(vc, "loop", False)

    if vc.loop:
        return await ctx.send("Loop aktive edildi.")
    else:
        return await ctx.send("Loop kapatıldı.")

@bot.command()
async def queue(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Herhangi bir ses kanalında değilim.")
    elif not ctx.author.voice:
        return await ctx.send("İlk önce bir ses kanalına katıl.")
    elif not ctx.author.voice.channel == ctx.me.voice.channel:
        return await ctx.send("Aynı ses kanalında olmalıyız")
    else:
        vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty:
        return await ctx.send("Müzik sırası boş.")

    em = discord.Embed(title = "Queue")
    queue = vc.queue.copy()
    song_count = 0
    for song in queue:
        song_count += 1
        em.add_field(name = f"Song Num {song_count}", value = f"'{song.title}'")

    return await ctx.send(embed = em)

@bot.command()
async def volume(ctx: commands.context, volume: int):
    if not ctx.voice_client:
        return await ctx.send("Herhangi bir ses kanalında değilim.")
    elif not ctx.author.voice:
        return await ctx.send("İlk önce bir ses kanalına katıl.")
    elif not ctx.author.voice.channel == ctx.me.voice.channel:
        return await ctx.send("Aynı ses kanalında olmalıyız")
    else:
        vc: wavelink.Player = ctx.voice_client

    if volume > 100:
        return await ctx.send("ses seviyesi 100'den fazla olamaz.")
    if volume < 0:
        return await ctx.send("ses seviyesi 0'dan küçük olamaz.")
        
    await ctx.send(f"Ses seviyesi ayarlandı: {volume}")
    return await vc.set_volume(volume)

@bot.command()
async def nowplaying(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Herhangi bir ses kanalında değilim.")
    elif not ctx.author.voice:
        return await ctx.send("İlk önce bir ses kanalına katıl.")
    elif not ctx.author.voice.channel == ctx.me.voice.channel:
        return await ctx.send("Aynı ses kanalında olmalıyız")
    else:
        vc: wavelink.Player = ctx.voice_client

    if not vc.is_playing():
        return await ctx.send("Hiçbir şey oynatılmıyor.")

    em = discord.Embed(title=f"Şu an oynatılıyor {vc.track.title}", description=f"Şarkıcı: {vc.track.author}")
    em.add_field(name="Duration", value=f"{str(datetime.timedelta(seconds=vc.track.length))}")
    em.add_field(name="Extra Info", value=f"Song URL: {str(vc.track.uri)}")
    return await ctx.send(embed=em)

@bot.command()
async def splay(ctx: commands.Context, *, search: str):
    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls = wavelink.Player)
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("İlk önce bir ses kanalına katıl.")
    elif not ctx.author.voice.channel == ctx.me.voice.channel:
        return await ctx.send("Aynı ses kanalında olmalıyız")
    else:
        vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty and not vc.is_playing():
        try:
            track = await spotify.SpotifyTrack.search(query=search, return_first=True)
            await vc.play(track)
            await ctx.send(f"{track.title} şu anda oynatılıyor.")
        except Exception as e:
            await ctx.send("Lütfen bir spotify url'si gir.")
            return print(e)
    else:
        track = await spotify.SpotifyTrack.search(query=search, return_first=True)
        await vc.queue.put_wait(track)
        await ctx.send(f"{track.title} sıraya eklendi.")
    
    vc.ctx = ctx
    """   
    if vc.loop:
        return
    """
    setattr(vc, "loop", False)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    #elif message.author.name == 'Tavşanlarhoca' or message.author.id == 313225607582318602:
        #await message.delete()
        #await message.channel.send(f'Sus amk evladı {message.author.name}!!')
    elif message.author.name == 'Yarking' or message.author.name == 'Secorpion':
        if message.content.lower() == 'jarvis':
            await message.channel.send(f'Buyrun {message.author.name} Bey')
        if message.content.lower() == 'halettin mi canım?':
            await message.channel.send(f'Halettim {message.author.name} Bey')
        if message.content == 'sustur':
            await message.ctx.invoke(message.bot.get_command('kick'))
#    else:
#        guild = bot.get_guild(372049876520796180)
#        await guild.get_member(859181482161078314).edit(nick='sabri sikici')
    
    await bot.process_commands(message)

bot.run(TOKEN)