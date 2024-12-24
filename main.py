import discord
from discord.ext import commands
from config import token
from logic import Pokemon
import logging


logging.basicConfig(level=logging.INFO, filename="bot.log", filemode="a", format="%(asctime)s - %(message)s")
logger = logging.getLogger()


intents = discord.Intents.default()  
intents.messages = True              
intents.message_content = True       
intents.guilds = True                


bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


@bot.event
async def on_ready():
    logger.info(f'Giriş yapıldı: {bot.user.name}')
    print(f'Giriş yapıldı: {bot.user.name}')

# Hata yönetimi
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Bu komut mevcut değil. Lütfen geçerli bir komut kullanın.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Eksik bir argüman var. Komut kullanımını kontrol edin.")
    elif isinstance(error, commands.CommandOnCooldown):  
        await ctx.send(f"Bu komutu tekrar kullanabilmek için {error.retry_after:.1f} saniye beklemelisiniz.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu kullanmak için gerekli yetkiye sahip değilsiniz.")
    else:
        await ctx.send(f"Bir hata oluştu: {str(error)}")

# '!go' komutu
@bot.command()
async def go(ctx):
    author = ctx.author.name  
    if author not in Pokemon.pokemons:
        pokemon = Pokemon(author)  
        await ctx.send(await pokemon.info())  
        image_url = await pokemon.show_img()  
        if image_url:
            embed = discord.Embed(
                title="Yeni Pokémon!",
                description="Pokémon'unuz başarıyla oluşturuldu!",
                color=discord.Color.blue()
            )
            embed.set_image(url=image_url)  
            embed.set_footer(text="Pokémon Maceranız Başladı!")
            await ctx.send(embed=embed)  
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!")  

# '!level_up' komutu
@bot.command()
@commands.cooldown(1, 120, commands.BucketType.user)  
async def level_up(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        pokemon.level_up()  
        await ctx.send(f"{pokemon.name} artık {pokemon.level} seviyesinde!")
    else:
        await ctx.send("Önce bir Pokémon oluşturmalısınız.")

# '!info'
@bot.command()
async def info(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        image_url = await pokemon.show_img()
        embed = discord.Embed(
            title=f"{pokemon.name} - Bilgiler",
            description="Pokémon'unuzun detayları aşağıda:",
            color=discord.Color.green()
        )
        embed.add_field(name="Adı", value=pokemon.name, inline=False)
        embed.add_field(name="Seviye", value=str(pokemon.level), inline=False)
        embed.add_field(name="Sağlık", value=str(pokemon.hp), inline=False)
        embed.add_field(name="Güç", value=str(pokemon.power), inline=False)
        if image_url:
            embed.set_image(url=image_url)  
        embed.set_footer(text="Pokémon Bilgisi")
        await ctx.send(embed=embed)
    else:
        await ctx.send("Henüz bir Pokémon oluşturmadınız. `!go` komutunu kullanarak bir Pokémon oluşturabilirsiniz.")

# '!ban' komutu - Yöneticilere özel
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason=None):
    if not member:
        await ctx.send(
            "**Komut Kullanımı:**\n"
            "`!ban <@kullanıcı> [sebep]`\n"
            "Bu komut bir kullanıcıyı banlamak için kullanılır. Sadece ban yetkisine sahip kullanıcılar bu komutu kullanabilir."
        )
        return
    
    if member == ctx.author:
        await ctx.send("Kendinizi banlayamazsınız!")
        return
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} kullanıcısı banlandı. Sebep: {reason or 'Belirtilmedi.'}")
        logger.info(f"{member} kullanıcı {ctx.author} tarafından banlandı. Sebep: {reason}")
    except discord.Forbidden:
        await ctx.send("Bu kullanıcıyı banlamak için yeterli yetkim yok.")
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {str(e)}")


# '!help' komutu
@bot.command()
async def help(ctx):
    help_message = """
    **Komutlar:**
    - `!go`: Yeni bir Pokémon oluşturur.
    - `!level_up`: Pokémon'un seviyesini artırır (120 saniye bekleme süresi bulunur).
    - `!info`: Pokémon bilgilerinizi gösterir.
    - `!ban`: Bir kullanıcıyı banlar (Sadece yetkili kullanıcılar için).
    - `!help`: Bu mesajı gösterir.
    """
    await ctx.send(help_message)


bot.run(token)
