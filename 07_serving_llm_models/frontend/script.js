// =============================================================================
// script.js — Frontend Logic for AI Health Advisor
// =============================================================================
// Responsibilities:
//   1. Live character counter on the concern textarea
//   2. Client-side validation before sending the request
//   3. Build the JSON payload (only include optional fields that have a value)
//   4. POST to /chat and handle success / error responses
//   5. Typewriter animation for the AI response
//   6. Ctrl+Enter shortcut to submit from the textarea
// =============================================================================


// API endpoint — relative URL works because FastAPI serves both the
// frontend (GET /) and the API (POST /chat) from the same origin.
const API_URL = "/chat";


// =============================================================================
// Live character counter
// =============================================================================
// Updates the counter below the textarea as the user types.

document.getElementById("text").addEventListener("input", function () {
  document.getElementById("char-count").textContent = this.value.length;
});


// =============================================================================
// Keyboard shortcut — Ctrl+Enter submits the form
// =============================================================================

document.getElementById("text").addEventListener("keydown", function (e) {
  if (e.key === "Enter" && e.ctrlKey) {
    submitForm();
  }
});


// =============================================================================
// Helpers
// =============================================================================

/** Return the trimmed value of an input element by ID. */
function getVal(id) {
  return document.getElementById(id).value.trim();
}

/** Show a validation or network error message in the error box. */
function showError(msg) {
  const box = document.getElementById("error-box");
  box.textContent = msg;
  box.classList.remove("hidden");
  box.scrollIntoView({ behavior: "smooth", block: "center" });
}

/** Hide the error box. */
function clearError() {
  document.getElementById("error-box").classList.add("hidden");
}

/**
 * Toggle the submit button's loading state.
 * @param {boolean} on - true to show spinner, false to restore normal state.
 */
function setLoading(on) {
  const btn     = document.getElementById("submit-btn");
  const btnText = document.getElementById("btn-text");
  const spinner = document.getElementById("btn-spinner");

  btn.disabled = on;
  btn.classList.toggle("opacity-70", on);
  btnText.textContent = on ? "Thinking..." : "Get Health Advice";
  spinner.classList.toggle("hidden", !on);
}


// =============================================================================
// Typewriter animation
// =============================================================================
// Writes the LLM response one character at a time for a realistic typing effect.
// The blinking cursor (defined in style.css) is removed once typing finishes.

/**
 * @param {HTMLElement} element - The element to type into.
 * @param {string}      text    - The full text to animate.
 * @param {number}      speed   - Milliseconds between each character.
 */
function typewrite(element, text, speed = 10) {
  element.textContent = "";
  element.classList.remove("done");

  let i = 0;
  const timer = setInterval(() => {
    element.textContent += text[i];
    i++;

    if (i >= text.length) {
      clearInterval(timer);
      element.classList.add("done"); // removes the blinking cursor
    }
  }, speed);
}


// =============================================================================
// Form submission
// =============================================================================

async function submitForm() {
  clearError();

  // ── Collect required fields ──────────────────────────────────────────────
  const name   = getVal("name");
  const age    = getVal("age");
  const gender = getVal("gender");
  const text   = getVal("text");

  // ── Client-side validation ───────────────────────────────────────────────
  // These mirror the Pydantic constraints so the user gets instant feedback
  // without a round-trip to the server.
  if (name.length < 5)  return showError("Full name must be at least 5 characters.");
  if (!age)             return showError("Age is required.");
  if (!gender)          return showError("Please select a gender.");
  if (text.length < 10) return showError("Please describe your concern in at least 10 characters.");

  // ── Collect optional fields ──────────────────────────────────────────────
  const city        = getVal("city");
  const height      = getVal("height");
  const weight      = getVal("weight");
  const exercise    = getVal("exercise");
  const sleep_hours = getVal("sleep_hours");

  // The checked radio button — value is "" if "Prefer not to say" is selected.
  const smooking = document.querySelector('input[name="smooking"]:checked')?.value || "";

  // ── Build payload ────────────────────────────────────────────────────────
  // Required fields are always included.
  // Optional fields are only added when the user provided a value —
  // this matches the schema where they are Optional (default None).
  const payload = {
    name,
    age:    parseInt(age),
    gender,
    text,
    ...(city        && { city }),
    ...(height      && { height:      parseFloat(height) }),
    ...(weight      && { weight:      parseFloat(weight) }),
    ...(exercise    && { exercise }),
    ...(sleep_hours && { sleep_hours: parseFloat(sleep_hours) }),
    ...(smooking    && { smooking }),
  };

  // ── Send request ─────────────────────────────────────────────────────────
  setLoading(true);
  document.getElementById("response-card").classList.add("hidden");

  try {
    const res = await fetch(API_URL, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(payload),
    });

    if (!res.ok) {
      // Parse the FastAPI error response — 422 returns structured detail array.
      const err    = await res.json().catch(() => ({}));
      const detail = err.detail?.[0]?.msg || err.detail || `Server error (${res.status})`;
      return showError(detail);
    }

    const data = await res.json();

    // Show and animate the response card.
    const card         = document.getElementById("response-card");
    const responseText = document.getElementById("response-text");

    card.classList.remove("hidden");
    card.scrollIntoView({ behavior: "smooth", block: "start" });

    typewrite(responseText, data.response);

  } catch {
    // Network-level failure (server not running, port wrong, etc.)
    showError("Could not reach the server. Make sure the API is running — uv run uvicorn 07_serving_llm_models.llm_health_api:app --reload");

  } finally {
    // Always restore the button, even if an error occurred.
    setLoading(false);
  }
}
