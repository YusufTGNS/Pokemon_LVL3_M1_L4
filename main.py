import discord
from discord.ext import commands
from config import token
from logic import Pokemon
import logging

# Loglama ayarları
logging.basicConfig(level=logging.INFO, filename="bot.log", filemode="a", format="%(asctime)s - %(message)s")
logger = logging.getLogger()

# Bot için niyetleri (intents) ayarlama
intents = discord.Intents.default()  # Varsayılan ayarların alınması
intents.messages = True              # Botun mesajları işlemesine izin verme
intents.message_content = True       # Botun mesaj içeriğini okumasına izin verme
intents.guilds = True                # Botun sunucularla (loncalar) çalışmasına izin verme

# Tanımlanmış bir komut önekine ve etkinleştirilmiş amaçlara sahip bir bot oluşturma
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot çalışmaya hazır olduğunda tetiklenen bir olay
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
    else:
        await ctx.send("Bir hata oluştu.")

# '!go' komutu
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Mesaj yazarının adını alma
    # Kullanıcının zaten bir Pokémon'u olup olmadığını kontrol edin. Eğer yoksa, o zaman...
    if author not in Pokemon.pokemons.keys():
        pokemon = Pokemon(author)  # Yeni bir Pokémon oluşturma
        await ctx.send(await pokemon.info())  # Pokémon hakkında bilgi gönderilmesi
        image_url = await pokemon.show_img()  # Pokémon resminin URL'sini alma
        if image_url:
            embed = discord.Embed(
                title="Yeni Pokémon!",
                description="Pokémon'unuz başarıyla oluşturuldu!",
                color=discord.Color.blue()
            )
            embed.set_image(url=image_url)  # Pokémon'un görüntüsünün ayarlanması
            embed.set_footer(text="Pokémon Maceranız Başladı!")
            await ctx.send(embed=embed)  # Görüntü içeren gömülü bir mesaj gönderme
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!")  # Bir Pokémon'un daha önce yaratılıp yaratılmadığını gösteren bir mesaj

# '!level_up' komutu
@bot.command()
async def level_up(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[author]
        pokemon.level_up()
        await ctx.send(f"{pokemon.name} artık {pokemon.level} seviyesinde!")
    else:
        await ctx.send("Önce bir Pokémon oluşturmalısınız.")

# '!help' komutu
@bot.command()
async def help(ctx):
    help_message = """
    **Komutlar:**
    - `!go`: Yeni bir Pokémon oluşturur.
    - `!level_up`: Pokémon'un seviyesini artırır.
    - `!help`: Bu mesajı gösterir.
    """
    await ctx.send(help_message)

# Yöneticilere özel bir komut örneği
@bot.command()
@commands.has_permissions(administrator=True)
async def admin_command(ctx):
    await ctx.send("Bu komutu sadece yöneticiler kullanabilir.")

# Botun çalıştırılması
bot.run(token)
