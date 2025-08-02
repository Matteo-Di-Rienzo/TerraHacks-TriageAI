const patientForm = document.getElementById("patient-form")


patientForm.addEventListener("submit", e => {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const age = parseInt(document.getElementById("age").value);
  const height = parseInt(document.getElementById("height").value);
  const weight = parseInt(document.getElementById("weight").value);
  const incidentTime = document.getElementById("incidentTime").value;
  const admittanceTime = document.getElementById("admittanceTime").value;
  const concern = document.getElementById("concern").value;

  fetch("/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, age, height, weight, 
                          incidentTime, admittanceTime,  
                          concern})
  })
    .then(res => res.json())
    .then(() => {
      document.getElementById("patient-form").reset()
    })
    .catch(err => {
      console.error("Failed to load", err)});
  });

