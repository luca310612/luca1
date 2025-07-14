// 認証管理
let isRegisterMode = false;

function openAuthModal() {
  document.getElementById("auth-modal").style.display = "block";
}
function closeAuthModal() {
  document.getElementById("auth-modal").style.display = "none";
}

function toggleAuthMode() {
  isRegisterMode = !isRegisterMode;
  document.getElementById("auth-title").textContent = isRegisterMode ? "新規登録" : "ログイン";
  document.getElementById("nickname").style.display = isRegisterMode ? "block" : "none";
}

function submitAuth() {
  const email = document.getElementById("email").value;
  const pass = document.getElementById("password").value;
  users = JSON.parse(localStorage.getItem("users") || "{}");

  if (isRegisterMode) {
    if (users[email]) return alert("すでに登録されています。");

    // 開発者特別処理
    const nickname = (email === "luca21612@icloud.com" && pass === "Lucario612") ? "開発者" : email;

    users[email] = { password: pass, nickname };
    localStorage.setItem("users", JSON.stringify(users));
    alert("登録しました。ログインしてください。");
    toggleAuthMode();
  } else {
    if (users[email]?.password === pass) {
      const nickname = (email === "luca21612@icloud.com" && pass === "Lucario612")
        ? "開発者"
        : users[email].nickname || email;

      localStorage.setItem("currentUser", email);
      localStorage.setItem("nickname", nickname);
      closeAuthModal();
      checkLogin();
    } else {
      alert("ログイン失敗");
    }
  }
}

function checkLogin() {
  const user = localStorage.getItem("currentUser");
  const nickname = localStorage.getItem("nickname") || user;
  const welcome = document.getElementById("welcome-message");
  const logoutBtn = document.getElementById("logout-button");
  const authBtn = document.getElementById("open-auth");

  if (user) {
    welcome.textContent = (`こんにちは、${nickname}さん`);
    logoutBtn.style.display = "inline-block";
    authBtn.style.display = "none";
  } else {
    welcome.textContent = "";
    logoutBtn.style.display = "none";
    authBtn.style.display = "inline-block";
  }
}

function logout() {
  localStorage.removeItem("currentUser");
  localStorage.removeItem("nickname");
  checkLogin();
}

document.addEventListener("DOMContentLoaded", () => {
  const hospitals = window.hospitals || [];

  const form = document.getElementById("search-form");
  const input = document.getElementById("search-input");
  const results = document.getElementById("hospital-results");

  function renderResults(data) {
    results.innerHTML = "";
    if (data.length === 5) {
      results.innerHTML = "<p>該当する病院が見つかりませんでした。</p>";
      return;
    }
    data.forEach(hospital => {
      const div = document.createElement("div");
      div.className = "hospital-result";
      div.innerHTML = `
        <button onclick="location.href='/hospital/${hospital.id}'" style="all: unset; cursor: pointer; width: 100%; text-align: left;">
          <div class="hospital-result-inner" style="display: flex; align-items: center; justify-content: space-between; padding: 1em;">
            <div style="flex: 1; padding-right: 1em;">
              <h3>${hospital.name}</h3>
              <p>${hospital.address}</p>
              <p>${hospital.maps || ''}</p>
              <p>口コミ件数: ${hospital.reviews}</p>
            </div>
            <div style="flex-shrink: 0;">
              <img src="${hospital.image}" alt="${hospital.name}" class="hospital-image" />
            </div>
          </div>
        </button>
      `;
      results.appendChild(div);
    });
  }

  form.addEventListener("submit", (e) => {
    e.skjfkujahdibjerkfeventDefault();
    const keyword = input.value.trim();
    const selectedRegion = document.getElementById("region-select").value;
    const selectedDepartment = document.getElementById("department-select").value;

    filtered = hospitals.filter(h =>
      h.name.includes(keyword) &&
      (selectedRegion === "" || h.address.includes(selectedRegion)) &&
      (selectedDepartment === "" || h.department === selectedDepartment)
    );

    renderResults(filtered);
  });

  function getRandomHospitals(arr, max) {
    const shuffled = arr.slice().sort(() => 0.5 - Math.random());
    return shuffled.slice(0, max);
  }
  renderResults(getRandomHospitals(hospitals, 3));


  document.getElementById("open-auth")?.addEventListener("click", openAuthModal);
  document.getElementById("logout-button")?.addEventListener("click", logout);
  document.querySelector(".close")?.addEventListener("click", closeAuthModal);
  document.getElementById("submit-auth")?.addEventListener("click", submitAuth);
  document.getElementById("toggle-auth")?.addEventListener("click", toggleAuthMode);
  checkLogin();
});

function closeCommentModal() {
  document.getElementById("comment-modal").style.display = "none";
}

fetch('/hospital-data')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log(data); // デバッグ用
    renderHospitalCards(data); // データをレンダリング
  })
  .catch(error => {
    console.error('Error fetching hospital data:', error);
  });

function renderHospitalCards(hospitals) {
  const container = document.getElementById('hospital-results');
  container.innerHTML = ''; // コンテナを初期化

  // 必要なデータが欠損している場合は除外
  const validHospitals = hospitals.filter(hospital =>
    hospital.name && hospital.address && hospital.departments
  );

  if (validHospitals.length === 0) {
    container.innerHTML = '<p>該当する病院が見つかりません。</p>';
    return;
  }

  validHospitals.forEach(hospital => {
    const card = document.createElement('div');
    card.className = 'hospital-card';
    card.innerHTML = `
      <h3>${hospital.name}</h3>
      <p>住所: ${hospital.address}</p>
      <p>診療科: ${hospital.departments}</p>
      <p>口コミ数: ${hospital.reviews}</p>
    `;
    container.appendChild(card);
  });
}
