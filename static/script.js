document.getElementById('submitBtn').addEventListener('click', async () => {
    const text = document.getElementById('dreamText').value;

    if (!text.trim()) {
        alert('Please write a dream entry first.');
        return;
    }

    const response = await fetch('/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    });

    const result = await response.json();

    document.getElementById('resultEmotion').textContent = result.emotion;
    document.getElementById('resultConfidence').textContent = result.confidence;
    document.getElementById('resultSymbols').textContent =
        result.symbols.length > 0 ? result.symbols.join(', ') : 'None detected';

    document.getElementById('result').classList.remove('hidden');
});