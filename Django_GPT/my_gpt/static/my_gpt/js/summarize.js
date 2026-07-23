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
    const response = await fetch("/summarize/run/", {
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
      <p>원문 길이: ${data.original_length}자</p>
      <p>요약문 길이: ${data.summary_length}자</p>
      <p>요약 비율: ${data.summary_ratio}%</p>
      <p>요약 결과: ${data.summary}</p>
    `;
  } catch (err) {
    errorBox.textContent = "네트워크 오류가 발생했습니다.";
  } finally {
    runBtn.disabled = false;
    textInput.disabled = false;
    processing.style.display = "none";
  }
});