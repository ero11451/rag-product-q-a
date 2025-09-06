const form = document.getElementById('qa-form');
const askBtn = document.getElementById('ask-btn');
const clearBtn = document.getElementById('clear-btn');
const questionEl = document.getElementById('question');
const answerEl = document.getElementById('answer');
const errorEl = document.getElementById('error');
const statusEl = document.getElementById('status');

function setLoading(isLoading) {
  askBtn.disabled = isLoading;
  questionEl.disabled = isLoading;
  statusEl.style.display = isLoading ? 'block' : 'none';
  statusEl.textContent = isLoading ? 'Thinking…' : '';
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  errorEl.textContent = '';
  answerEl.textContent = '';
  const question = questionEl.value.trim();
  if (!question) {
    errorEl.textContent = "Please enter a question.";
    return;
  }

  setLoading(true);
  try {
    const res = await fetch('/agent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || 'Request failed');
    }
    console.log(data)
    answerEl.textContent = data.answer.output ?? '';
  } catch (err) {
    errorEl.textContent = err.message || String(err);
  } finally {
    setLoading(false);
  }
});

clearBtn.addEventListener('click', () => {
  questionEl.value = '';
  answerEl.textContent = '';
  errorEl.textContent = '';
  questionEl.focus();
});
