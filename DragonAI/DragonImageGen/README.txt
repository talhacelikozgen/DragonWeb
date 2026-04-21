DRAGON AI KURULUM VE KULLANIM REHBERİ

​Dragon AI projesini Intel Arc B580 ekran kartınızda sıfırdan çalıştırmak için aşağıdaki adımları sırasıyla 
takip edin. Bu rehber, sistemde hiçbir hazırlık olmadığını varsayarak hazırlanmıştır.

​Temel Yazılım Gereksinimleri:
Bilgisayarınızda Python 3.10 sürümünün kurulu olduğundan emin olun. Ayrıca Intel ekran kartının performansını 
tam kullanabilmek için internetten Intel oneAPI Base Toolkit paketini indirip kurmuş olmanız gerekmektedir. Bu 
paket, kartın içindeki yapay zeka çekirdeklerini (XMX) aktif eder.

​Sanal Ortam Kurulumu:
VS Code terminalini açın ve projenin ana klasörü olan DragonImageGen dizinine gidin. Önce "python -m venv venv" 
komutuyla bir sanal ortam oluşturun. Ardından ".\venv\Scripts\activate" komutuyla bu ortamı aktif hale getirin. 
Bu sayede kuracağımız kütüphaneler bilgisayarın genelini etkilemez, sadece bu projeye özel kalır.

​Kütüphanelerin Yüklenmesi:
Sanal ortam aktifken "pip install -r requirements.txt" komutunu çalıştırarak gerekli olan PyTorch, Intel Extension 
for PyTorch (IPEX) ve diğer yapay zeka kütüphanelerini otomatik olarak yükleyin.

​Model Dosyalarının Hazırlanması:
Dragon AI çevrimdışı (offline) çalışma mantığına sahiptir. İnternetten indirdiğiniz Stable Diffusion modellerini 
(özellikle .safetensors uzantılı olanları) DragonWeb/DragonAI/DragonImageGen/models/ klasörü içerisine yerleştirin. 
Model dosyaları olmazsa üretim yapılamaz.

​Sistemin Çalıştırılması:
Görsel üretmek veya dış dünyayla bağlantı kurmak için "python api_server.py" komutunu kullanın. Eğer modele yeni bir 
şeyler öğretmek istiyorsanız "python training/trainer.py" komutuyla öğrenme modülünü başlatın.

​Veri Gizliliği ve Kayıt:
Ürettiğiniz tüm görseller "outputs" klasörüne, modelin öğrendiği yeni bilgiler ise "training/lora_weights" klasörüne 
kaydedilir. Hiçbir veri dış sunuculara gönderilmez, her şey sizin yerel depolamanızda kalır.

​Önemli Not: Eğer ekran kartı tanınmazsa Intel Arc Control üzerinden grafik sürücülerinizin güncel olup olmadığını kontrol edin.
