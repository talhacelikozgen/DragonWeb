// Panoyu Yükle ve Referansları Göster
function loadBoard() {
    fetch('../Archive/dragon_board.json')
        .then(res => res.json())
        .then(data => {
            const board = document.getElementById('main-board');
            board.innerHTML = ""; // Temizle
            data.tasks.forEach(task => {
                // Klasör ismini başlığa göre tahmin et (Scout'un mantığı)
                const folderName = task.title.replace(/\s+/g, '_');
                
                board.innerHTML += `
                    <div class="card">
                        <span class="tag">[${task.language}]</span>
                        <h4>${task.title}</h4>
                        <p>${task.description}</p>
                        <div class="ref-box">
                            <strong>👁️ Scout Referansları:</strong><br>
                            <a href="../Archive/References/${folderName}/" style="color:#d4af37">Dosyaları Görüntüle</a>
                        </div>
                    </div>`;
            });
        });
}

// Yeni Emir Gönder (Şimdilik sadece konsola yazar, ileride Python yakalar)
function sendOrder() {
    const title = document.getElementById('taskTitle').value;
    const lang = document.getElementById('taskLang').value;
    const desc = document.getElementById('taskDesc').value;

    console.log("🐲 Emir Dragon Brain'e iletildi:", { title, lang, desc });
    alert("Emir verildi! (Python Backend entegrasyonu bir sonraki adımda yapılacak)");
}

loadBoard();