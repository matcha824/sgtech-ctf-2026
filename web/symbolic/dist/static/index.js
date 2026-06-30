var submissionText;
var resultContainer;
var resultBody;
var errorContainer;
var errorText;

window.onload = () => {
    submissionText = document.getElementById("submission-box");
    resultContainer = document.getElementById("result");
    resultBody = document.getElementById("result-body");
    errorContainer = document.getElementById("error");
    errorText = document.getElementById("error-box")
}

function renderResults(results) {
    resultBody.innerHTML = "";

    for (const [symbol, solutions] of Object.entries(results)) {
        const values = solutions.length ? solutions : ["No results found"];

        for (let index = 0; index < values.length; index++) {
            const row = document.createElement("tr");
            const termCell = document.createElement("td");
            const valueCell = document.createElement("td");

            termCell.textContent = index === 0 ? symbol : "";
            valueCell.textContent = values[index];

            row.appendChild(termCell);
            row.appendChild(valueCell);
            resultBody.appendChild(row);
        }
    }
}

async function submit() {
    let res = await fetch("/solve", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ expression: submissionText.textContent })
    });

    let data = await res.json()

    if (res.status != 200) {
        errorText.innerText = `Error processing expression: ${data.error}`
        errorContainer.hidden = false;
        resultContainer.hidden = true;
        return
    }

    renderResults(data.result)
    errorContainer.hidden = true;
    resultContainer.hidden = false;
}
