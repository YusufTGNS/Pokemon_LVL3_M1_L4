import aiohttp
import random

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer, level=1,):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.power = random.randint(30,60)
        self.hp = random.randint(100,200)
        self.level = level
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        # `else` bloğuna gerek yok çünkü nesne zaten kaydedilmiş oluyor

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için eşzamansız bir yöntem
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                else:
                    return "Pikachu"  # Varsayılan ad

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        return f"Pokémonunuzun ismi: {self.name} - Seviye: {self.level} - Sağlık : {self.hp} - Saldırı Gücü: {self.power}"

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    img_url = data['sprites']['front_default']
                    return img_url
                else:
                    return None

    def level_up(self):
        """Pokémon seviyesini artırır."""
        self.level += 1
        return self.level

    def __str__(self):
        """Pokémon hakkında genel bilgi döndürür."""
        return f"{self.name} (Seviye {self.level})"
    
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):  # Enemy'nin bir Wizard veri tipi olduğunu (Büyücü sınıfının bir örneği olduğunu) kontrol etme
            şans = random.randint(1, 5) 
        if şans == 1:
            return "Sihirbaz Pokémon, savaşta bir kalkan kullanıldı!"
        
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu şimdi {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ni yendi!"

class Wizard(Pokemon):
    async def attack(self, enemy):
        return await super().attack(enemy)

class Fighter(Pokemon):
    async def attack(self, enemy):
        süper_güç = random.randint(5, 15) 
        self.güç += süper_güç
        sonuç = await super().attack(enemy)
        self.güç -= süper_güç
        return sonuç + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {süper_güç}"

    