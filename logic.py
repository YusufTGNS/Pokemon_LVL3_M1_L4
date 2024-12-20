import aiohttp
import random

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer, level=1):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
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
        return f"Pokémonunuzun ismi: {self.name} - Seviye: {self.level}"

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
