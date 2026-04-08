const API_URL = "http://127.0.0.1:8000/chat";

// Character counter for concern textarea
document.getElementById("text").addEventListener("input", function () {
  document.getElementById("char-count").textContent = this.value.length;
});

function getVal(id) {
  return document.getElementById(id).value.trim();
}

function showError(msg) {
  const box = document.getElementById("error-box");
  box.textContent = msg;
  box.classList.remove("hidden");
  box.scrollIntoView({ behavior: "smooth", block: "center" });
}

function clearError() {
  document.getElementById("error-box").classList.add("hidden");
}

function setLoading(on) {
  const btn = document.getElementById("submit-btn");
  const text = document.getElementById("btn-text");
  const spinner = document.getElementById("btn-spinner");
  btn.disabled = on;
  btn.classList.toggle("opacity-70", on);
  text.textContent = on ? "Thinking..." : "Get Health Advice";
  spinner.classList.toggle("hidden", !on);
}

function typewrite(element, text, speed = 12) {
  element.textContent = "";
  element.classList.remove("done");
  let i = 0;
  const timer = setInterval(() => {
    element.textContent += text[i];
    i++;
    if (i >= text.length) {
      clearInterval(timer);
      element.classList.add("done");
    }
  }, speed);
}

async function submitForm() {
  clearError();

  // --- Collect & validate required fields ---
  const name = getVal("name");
  const age = getVal("age");
  const gender = getVal("gender");
  const text = getVal("text");

  if (name.length < 5)   return showError("Name must be at least 5 characters.");
  if (!age)              return showError("Age is required.");
  if (!gender)           return showError("Please select a gender.");
  if (text.length < 10)  return showError("Please describe your concern (min 10 characters).");

  // --- Build payload ---
  const smooking = document.querySelector('input[name="smooking"]:checked')?.value || undefined;
  const height = getVal("height");
  const weight = getVal("weight");
  const exercise = getVal("exercise");
  const sleep_hours = getVal("sleep_hours");
  const city = getVal("city");

  const payload = {
    name,
    age: parseInt(age),
    gender,
    text,
    ...(city        && { city }),
    ...(height      && { height: parseFloat(height) }),
    ...(weight      && { weight: parseFloat(weight) }),
    ...(exercise    && { exercise }),
    ...(sleep_hours && { sleep_hours: parseFloat(sleep_hours) }),
    ...(smooking    && { smooking }),
  };

  // --- Send request ---
  setLoading(true);
  document.getElementById("response-card").classList.add("hidden");

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      const detail = err.detail?.[0]?.msg || err.detail || `Server error (${res.status})`;
      return showError(detail);
    }

    const data = await res.json();
    const card = document.getElementById("response-card");
    const responseText = document.getElementById("response-text");
    card.classList.remove("hidden");
    card.scrollIntoView({ behavior: "smooth", block: "start" });
    typewrite(responseText, data.response);

  } catch (e) {
    showError("Could not reach the server. Make sure the API is running on port 8000.");
  } finally {
    setLoading(false);
  }
}

// Allow Enter key in text area (Shift+Enter = newline, Enter alone won't submit)
// Submit on Ctrl+Enter
document.getElementById("text").addEventListener("keydown", function (e) {
  if (e.key === "Enter" && e.ctrlKey) submitForm();
});
