const form = document.getElementById('calculator-form');
const resultText = document.getElementById('result-text');

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const payload = {
    input1: Number(formData.get('input1')),
    input2: Number(formData.get('input2')),
    operator: formData.get('operator'),
  };

  resultText.textContent = 'Calculating...';

  try {
    const response = await fetch('/calculate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      resultText.textContent = data.error || 'Something went wrong.';
      return;
    }

    resultText.textContent = `Result: ${data.result}`;
  } catch (error) {
    resultText.textContent = 'Unable to connect to backend.';
  }
});
