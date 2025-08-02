const patientForm = document.getElementById("patient-form")


patientForm.addEventListener("submit", e => {
  e.preventDefault();
  
  const name = document.getElementById("name").value;
  const age = parseInt(document.getElementById("age").value);
  const concern = document.getElementById("concern").value;

  fetch("/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, age, concern })
  })
    .then(res => res.json())
    .then(() => {
      document.getElementById("patient-form").reset()
    })
    .catch(err => {
      console.error("Failed to load", err)});
  });

// Gemini button handler (add after the above code)
const geminiBtn = document.getElementById("gemini-btn");
geminiBtn.addEventListener("click", () => {
fetch("/gemini", { method: "POST" })
.then(res => res.json())
.then(data => {
    alert(data.gemini_response);
});
});