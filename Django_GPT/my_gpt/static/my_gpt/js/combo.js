const textInput = document.getElementById("input-text");
const runBtn = document.getElementById("run-btn");
const regenerateBtn = document.getElementById("regenerate-btn");
const processing = document.getElementById("processing");
const errorBox = document.getElementById("error-box");
const resultBox = document.getElementById("result-box");

let lastText = null;

async function runCombo(text, regenerate) {
  errorBox.textContent = "";

  runBtn.disabled = true;
  regenerateBtn.disabled = true;
  textInput.disabled = true;
  processing.style.display = "block";

  try {
    const response = await fetch("/combo/run/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": CSRF_TOKEN,
      },
      body: JSON.stringify({ text: text, regenerate: regenerate }),
    });

    const data = await response.json();

    if (!response.ok) {
      errorBox.textContent = data.error || "알 수 없는 오류가 발생했습니다.";
      return;
    }

    lastText = text;
    regenerateBtn.style.display = "inline-block";

    resultBox.innerHTML = `
      <h4>[입력 원문]</h4>
      <p>${data.original_text}</p>

      <h4>[요약]</h4>
      <p>${data.summary}</p>

      <h4>[감정 분석]</h4>
      <p>${data.sentiment.label} (${(data.sentiment.score * 100).toFixed(2)}%)</p>

      <h4>[유해 표현 분석]</h4>
      <p>Highest Risk: ${data.toxicity.highest_label} (${(data.toxicity.highest_score * 100).toFixed(2)}%)</p>

      <h4>[종합 판정]</h4>
      <p>${data.verdict}</p>
    `;
  } catch (err) {
    errorBox.textContent = "네트워크 오류가 발생했습니다.";
  } finally {
    runBtn.disabled = false;
    regenerateBtn.disabled = false;
    textInput.disabled = false;
    processing.style.display = "none";
  }
}

runBtn.addEventListener("click", () => {
  runCombo(textInput.value, false);
});

regenerateBtn.addEventListener("click", () => {
  if (lastText === null) return;
  runCombo(lastText, true);
});