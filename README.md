# Discord Pokemon Bot

Bu proje, Discord'da kullanılmak üzere bir Pokemon botu geliştirmek için hazırlanmıştır. Bot, kullanıcılara kendi Pokemon'larını oluşturma, seviyelerini artırma, besleme ve diğer kullanıcılara saldırma imkanı sunar.

## Özellikler

### Pokemon Mekanikleri
- **Pokemon Sınıfı**: Pokemon'un temel özellikleri (isim, seviye, sağlık, saldırı gücü) ve işlevleri (besleme, saldırı, seviye atlama) tanımlanır.
- **Alt Sınıflar**:
  - **Wizard**: Daha hızlı sağlık artışı sağlar.
  - **Fighter**: Süper saldırı özelliği ile ekstra güç kullanır.

### Discord Bot Özellikleri
- **Komutlar**:
  - `!go`: Yeni bir Pokemon oluşturur.
  - `!level_up`: Pokemon'un seviyesini artırır (120 saniye bekleme süresi bulunur).
  - `!info`: Kullanıcının mevcut Pokemon'unun detaylarını gösterir.
  - `!feed`: Pokemon'u besler ve sağlık puanını artırır.
  - `!attack @kullanıcı`: Belirtilen kullanıcıya saldırır.
  - `!ban @kullanıcı`: Yöneticilere özel, bir kullanıcıyı banlama komutu.
  - `!help`: Komutların listesini ve açıklamalarını gösterir.

## Kullanılan Teknolojiler
- **Python**: Projenin temel programlama dili.
- **discord.py**: Discord botunu oluşturmak için kullanılan kütüphane.
- **aiohttp**: PokeAPI'den veri almak için kullanılan asenkron HTTP istemcisi.

## Kurulum ve Kullanım
1. Gerekli bağımlılıkları yükleyin:
   ```bash
   pip install discord.py aiohttp
   ```
2. `config.py` dosyasına Discord bot token'inizi ekleyin:
   ```python
   token = "YOUR_BOT_TOKEN"
   ```
3. Botu başlatın:
   ```bash
   python main.py
   ```
4. Discord sunucunuzda botu kullanmaya başlayabilirsiniz.

## Notlar
- PokeAPI kullanılarak Pokemon isimleri ve görselleri çekilmektedir. İnternet bağlantısı gereklidir.
- Bazı komutlar (örn. `!level_up`) için süre kısıtlaması bulunmaktadır.
- Yalnızca sunucu yöneticileri `!ban` komutunu kullanabilir.

## Geliştirici Notları
- **logic.py**: Pokemon'ların oyun mekaniklerini tanımlayan sınıflar ve işlevler içerir.
- **main.py**: Discord botunun ana işleyişini tanımlar ve komutları yönetir.

Proje hakkında geri bildirim ve katkılarınızı bekliyoruz! 😊

