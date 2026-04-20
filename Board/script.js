fetch('../Archive/dragon_board.json')
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById('task-list');
        data.tasks.forEach(task => {
            list.innerHTML += `
                <div class="card">
                    <div>[${task.status}]</div>
                    <div class="tag">${task.language}</div>
                    <strong>${task.title}</strong>
                    <p>${task.description}</p>
                </div>`;
        });
    });