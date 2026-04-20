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

function sendOrder() {
    const task = {
        title: document.getElementById('taskTitle').value,
        language: document.getElementById('taskLang').value,
        description: document.getElementById('taskDesc').value,
        status: "todo"
    };

    // Bilgisayarındaki Python beynine (server.py) veriyi gönder
    fetch('http://127.0.0.1:5000/send-order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(task)
    })
    .then(res => res.json())
    .then(data => {
        alert("🐉 Dragon Brain Emri Aldı!");
        loadBoard(); // Panoyu yenile
    })
    .catch(err => {
        console.error("Bağlantı Hatası: Python 'server.py' çalışıyor mu?", err);
    });
}

loadBoard();