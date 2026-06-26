/**
 * 게임 관리 객체
 */
const game={
    tryCount : 9,
    answer: []
}
/**
 * DOM객체 등록
 */
const input1 = document.getElementById("number1");
const input2 = document.getElementById("number2");
const input3 = document.getElementById("number3");
const attemptsSpan = document.getElementById("attempts");
const results = document.getElementById("results");
const resultImg = document.getElementById("game-result-img");
const submitButton = document.querySelector(".submit-button");
/**
 * 정답 생성 함수
 * @returns 중복되지 않는 0~9사이 숫자 list
 */
function generateAnswer(){
    let a, b, c;
    a = Math.floor(Math.random()*10);
    do {
        b = Math.floor(Math.random()*10);
    } while (b==a);
    do {
        c = Math.floor(Math.random()*10);
    }while(c==b || c==a);
    return [a,b,c];
}
/**
 * 입력칸 초기화 함수
 */
function clearInput(){
    input1.value="";
    input2.value="";
    input3.value="";
}
/**
 * 남은횟수 업데이트 함수
 */
function updateUI(){
    attemptsSpan.textContent = game.tryCount;
}
/**
 * 게임 시작 함수
 */
function init_UI(){
    clearInput();
    updateUI();
    game.answer = generateAnswer();
}
function check_numbers(){
    const n1 = parseInt(input1.value);
    const n2 = parseInt(input2.value);
    const n3 = parseInt(input3.value);
    const guess = [n1, n2, n3];
    let strikes=0, balls=0;

    //입력되지 않은 입력값 확인
    if(isNaN(n1) || isNaN(n2) || isNaN(n3)){
        clearInput();
        return;
    }
    //중복 입력값 확인
    if(new Set(guess).size!=3){
        clearInput();
        return;
    }
    for(let i=0; i<3; i++){
        if(guess[i] == game.answer[i]) strikes++;
        else if(game.answer.includes(guess[i])) balls++;
    }

    game.tryCount--;
    updateUI();
    showResult(guess, strikes, balls);
    if(strikes==3){
        resultImg.src = "success.png";
        submitButton.disabled = true;
        clearInput();
        return;
    }
    if(game.tryCount==0){
        resultImg.src = "fail.png";
        submitButton.disabled = true;
        clearInput();
        return;
    }
}
function showResult(guess, strikes, balls){
    let resultHTML;
    const resultDiv = document.createElement("div");

    //결과메시지 생성
    if(!strikes && !balls){
        resultHTML = '<span class="num-reulst out">O</span>';
    } else{
        resultHTML = `<p>${strikes}<span class="strike">S</span>${balls}<span class="ball">B</span></p>`;
    }

    resultDiv.className = "check-result";
    //입력값 : 결과메시지로 최종 메시지 생성
    resultDiv.innerHTML = `
        <div class="left">${guess.join(" ")}</div>
        <div>:</div>
        <div class="right">${resultHTML}</div>
    `;
    document.getElementById("results").appendChild(resultDiv);
}

//게임 시작
init_UI();