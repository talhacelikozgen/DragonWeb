@echo off

echo Dragon AI Baslatiliyor...

rem Sanal ortam klasorunun varligini kontrol et
if not exist ".\venv\" (
    echo Hata: Sanal ortam (venv) bulunamadi. Lutfen kurulum adimlarini takip edin.
    echo Ornek: "python -m venv venv" komutunu calistirin.
    pause
    exit /b 1
)

rem api_server.py dosyasinin varligini kontrol et
if not exist "api_server.py" (
    echo Hata: 'api_server.py' dosyasi bulunamadi. Lutfen dosyanin dogru konumda oldugundan emin olun.
    pause
    exit /b 1
)

echo Sanal ortam etkinlestiriliyor...
call ".\venv\Scripts\activate"
echo api_server.py baslatiliyor...
python "api_server.py"
echo Dragon AI calismayi tamamladi veya durduruldu.
pause
