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
       
        if isinstance(enemy, Wizard):
            chance = random.randint(1, 5)
            if chance == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullandı!"     
                
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu şimdi {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ni yendi!"

class Wizard(Pokemon):
    pass

class Fighter(Pokemon):
     async def attack(self, enemy):
        super_power = random.randint(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nDovuscu Pokémon süper saldırı kullandı. Eklenen guc: {super_power}"

import asyncio

async def main():
    wizard = Wizard("username1")
    fighter = Fighter("username2")

    # Pokémon bilgilerini göster
    wizard_info = await wizard.info()
    fighter_info = await fighter.info()
    print(wizard_info)
    print("#" * 10)
    print(fighter_info)
    print("#" * 10)

    # Saldırı senaryosu
    attack_result1 = await wizard.attack(fighter)
    attack_result2 = await fighter.attack(wizard)

    print(attack_result1)
    print(attack_result2)

# asyncio döngüsü ile çalıştır
asyncio.run(main())
  