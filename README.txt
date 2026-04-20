DRAGON BRAIN - SİSTEM KULLANIM KILAVUZU

1. KURULUM (İLK SEFER):
Terminali aç ve şu komutu yaz: 
pip install -r Brain/requirements.txt

2. SİSTEMİ ÇALIŞTIRMA (BİLGİSAYARDA HER ZAMAN AÇIK KALACAKLAR):
- Brain/server.py: Siteden (Board) gelen emirleri dinler. Kapatırsan emir veremezsin.
- Brain/scout.py: Emirler geldikten sonra referansları toplar (Bunu ihtiyacın olduğunda manuel çalıştırabilirsin).

3. ÇALIŞMA MANTIĞI:
Site (Board) -> Server.py -> Archive/dragon_board.json -> Scout.py -> Archive/References/