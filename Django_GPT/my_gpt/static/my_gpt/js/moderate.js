const textInput = document.getElementById("input-text");
const runBtn = document.getElementById("run-btn");
const processing = document.getElementById("processing");
const errorBox = document.getElementById("error-box");
const resultBox = document.getElementById("result-box");

runBtn.addEventListener("click", async () => {
  errorBox.textContent = "";
  resultBox.textContent = "";

  runBtn.disabled = true;
  textInput.disabled = true;
  processing.style.display = "block";

  try {
    const response = await fetch("/moderate/run/", {
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

    resultBox.innerHTML = `
      <p>최고 위험 레이블: ${data.highest_label}</p>
      <p>위험 점수: ${(data.highest_score * 100).toFixed(2)}%</p>
      <ul>
        ${data.all_scores.map(s => `<li>${s.label}: ${(s.score * 100).toFixed(2)}%</li>`).join("")}
      </ul>
    `;
  } catch (err) {
    errorBox.textContent = "네트워크 오류가 발생했습니다.";
  } finally {
    runBtn.disabled = false;
    textInput.disabled = false;
    processing.style.display = "none";
  }
});