async function loadDashboard() {
    const response = await fetch('/entries');
    const entries = await response.json();

    if (entries.length === 0) {
        document.getElementById('noData').classList.remove('hidden');
        return;
    }

    // --- Count emotion frequency ---
    const emotionCounts = {};
    entries.forEach(entry => {
        emotionCounts[entry.emotion] = (emotionCounts[entry.emotion] || 0) + 1;
    });

    new Chart(document.getElementById('emotionChart'), {
        type: 'bar',
        data: {
            labels: Object.keys(emotionCounts),
            datasets: [{
                label: 'Number of entries',
                data: Object.values(emotionCounts),
                backgroundColor: '#6c4fa1'
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } }
        }
    });

    // --- Count symbol frequency ---
    const symbolCounts = {};
    entries.forEach(entry => {
        entry.symbols.forEach(symbol => {
            if (symbol) {
                symbolCounts[symbol] = (symbolCounts[symbol] || 0) + 1;
            }
        });
    });

    new Chart(document.getElementById('symbolChart'), {
        type: 'bar',
        data: {
            labels: Object.keys(symbolCounts),
            datasets: [{
                label: 'Times mentioned',
                data: Object.values(symbolCounts),
                backgroundColor: '#9b7fc7'
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } }
        }
    });

    // --- List past entries ---
    const listDiv = document.getElementById('entryList');
    entries.slice().reverse().forEach(entry => {
        const div = document.createElement('div');
        div.className = 'entry-item';
        const date = new Date(entry.timestamp).toLocaleString();
        div.innerHTML = `
            <p class="entry-date">${date}</p>
            <p>${entry.text}</p>
            <p><strong>${entry.emotion}</strong> (confidence: ${entry.confidence}) — 
               symbols: ${entry.symbols.length ? entry.symbols.join(', ') : 'none'}</p>
        `;
        listDiv.appendChild(div);
    });
}

loadDashboard();