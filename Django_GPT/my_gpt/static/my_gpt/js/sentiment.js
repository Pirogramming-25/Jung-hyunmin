const MAX_HISTORY = 5;
const history = [];

const textInput = document.getElementById("input-text");
const runBtn = document.getElementById("run-btn");
const processing = document.getElementById("processing");
const errorBox = document.getElementById("error-box");
const resultBox = document.getElementById("result-box");
const historyList = document.getElementById("history-list");

runBtn.addEventListener("click", async () => {
  errorBox.textContent = "";
  resultBox.textContent = "";

  runBtn.disabled = true;
  textInput.disabled = true;
  processing.style.display = "block";

  try {
    const response = await fetch("/sentiment/run/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": CSRF_TOKEN,
      },
      body: JSON.stringify({ text: textInput.value }),
    });

    const data = await response.json();

    if (!response.ok) {
      errorBox.textContent = data.error || "알 수 없는 오류가 발생했습니다.";
      return;
    }

    resultBox.textContent =
      `감정: ${data.label} (신뢰도: ${(data.score * 100).toFixed(2)}%)`;

    history.unshift({ text: textInput.value, label: data.label, score: data.score });
    if (history.length > MAX_HISTORY) history.pop();
    renderHistory();
  } catch (err) {
    errorBox.textContent = "네트워크 오류가 발생했습니다.";
  } finally {
    runBtn.disabled = false;
    textInput.disabled = false;
    processing.style.display = "none";
  }
});

function renderHistory() {
  historyList.innerHTML = "";
  history.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `${item.text} → ${item.label} (${(item.score * 100).toFixed(1)}%)`;
    historyList.appendChild(li);
  });
}