// Path to the questions data file.
// To swap in a different question set, change this path.
const QUESTIONS_URL = "data/questions.json";

// ── Rendering ────────────────────────────────────────────────────────────────

/**
 * Fetches questions and populates #question-list.
 * Each question becomes a <li> with a labelled checkbox.
 */
async function loadQuestions() {
  const res = await fetch(QUESTIONS_URL);
  if (!res.ok) throw new Error(`Failed to load questions: ${res.status}`);
  const questions = await res.json();

  const list = document.getElementById("question-list");
  const totalEl = document.getElementById("score-total");

  totalEl.textContent = questions.length;

  list.innerHTML = questions
    .map(
      ({ id, text }) => `
    <li>
      <label>
        <input type="checkbox" name="q" value="${id}" />
        <span>${text}</span>
      </label>
    </li>`
    )
    .join("");
}

// ── Scoring ───────────────────────────────────────────────────────────────────

/**
 * Counts unchecked boxes and displays the result.
 * Score = total questions − number checked (higher = purer).
 */
function calculateScore() {
  const all = document.querySelectorAll('input[name="q"]');
  const checked = document.querySelectorAll('input[name="q"]:checked').length;
  const score = all.length - checked;

  document.getElementById("score-value").textContent = score;
  document.getElementById("score-panel").hidden = false;

  // Scroll the score into view on mobile where it may be off-screen
  document.getElementById("score-panel").scrollIntoView({ behavior: "smooth" });
}

// ── Bootstrap ─────────────────────────────────────────────────────────────────

document.getElementById("submit-btn").addEventListener("click", calculateScore);

loadQuestions().catch((err) => {
  document.getElementById("question-list").innerHTML =
    `<li class="error">Could not load questions. ${err.message}</li>`;
});
