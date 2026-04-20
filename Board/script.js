// Türkçe karakterleri İngilizceye dönüştür (Scout'un yaptığı gibi)
function turkishToEnglish(text) {
    const chars = {
        'ç': 'c', 'ş': 's', 'ğ': 'g', 'ü': 'u', 'ö': 'o', 'ı': 'i', 'İ': 'I',
        'Ç': 'C', 'Ş': 'S', 'Ğ': 'G', 'Ü': 'U', 'Ö': 'O'
    };
    let result = text;
    for (const [tr, en] of Object.entries(chars)) {
        result = result.replace(new RegExp(tr, 'g'), en);
    }
    return result.replace(/\s+/g, '_').toLowerCase().trim();
}

// Panoyu yükle
function loadBoard() {
    // Server'den yükle (dosya yerine API)
    const serverUrl = 'http://127.0.0.1:5000';
    
    fetch(`${serverUrl}/get-board`)
        .then(res => {
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.json();
        })
        .then(data => {
            const board = document.getElementById('main-board');
            board.innerHTML = ""; // Temizle
            
            if (!data.tasks || data.tasks.length === 0) {
                board.innerHTML = '<div style="color:#999">Henüz görev yok. Yeni bir emir giriniz.</div>';
                return;
            }
            
            data.tasks.forEach((task, index) => {
                // Klasör ismini Scout'un mantığına göre oluştur
                const folderName = turkishToEnglish(task.title);
                const timestamp = task.created_at ? new Date(task.created_at).toLocaleString('tr-TR') : 'Bilinmiyor';
                
                board.innerHTML += `
                    <div class="card">
                        <span class="tag">[${task.language || 'N/A'}]</span>
                        <h4>${task.title}</h4>
                        <p>${task.description || 'Açıklama yok'}</p>
                        <small style="color:#888">ID: ${task.id || index + 1} | ${timestamp}</small>
                        <div class="ref-box">
                            <strong>👁️ Scout Referansları:</strong><br>
                            <a href="../Archive/References/${folderName}/" style="color:#d4af37" target="_blank">📁 Dosyaları Görüntüle</a>
                        </div>
                    </div>`;
            });
        })
        .catch(err => {
            console.error("❌ Board yükleme hatası:", err);
            document.getElementById('main-board').innerHTML = 
                '<div style="color:red">⚠️ Board yüklenemedi. Server çalışıyor mu?</div>';
        });
}

// Yeni görev gönder
function sendOrder() {
    const title = document.getElementById('taskTitle').value.trim();
    const language = document.getElementById('taskLang').value;
    const description = document.getElementById('taskDesc').value.trim();
    
    // Validasyon
    if (!title) {
        alert("❌ Görev başlığı boş olamaz!");
        return;
    }
    if (!description) {
        alert("❌ Görev açıklaması boş olamaz!");
        return;
    }
    
    const task = {
        title: title,
        language: language,
        description: description,
        status: "todo"
    };
    
    const serverUrl = 'http://127.0.0.1:5000';
    
    fetch(`${serverUrl}/send-order`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(task)
    })
    .then(res => {
        if (!res.ok) return res.json().then(err => Promise.reject(err));
        return res.json();
    })
    .then(data => {
        alert("✅ 🐉 Dragon Brain emri aldı!");
        document.getElementById('taskTitle').value = '';
        document.getElementById('taskDesc').value = '';
        loadBoard();
    })
    .catch(err => {
        console.error("❌ Gönderme hatası:", err);
        alert(`❌ Hata: ${err.message || 'Server çalışmıyor'}`);
    });
}

// Sayfa yüklendiğinde board'u yükle
document.addEventListener('DOMContentLoaded', loadBoard);