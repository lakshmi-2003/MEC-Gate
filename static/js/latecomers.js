document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("latecomerForm").addEventListener("submit", function (event) {
        event.preventDefault();

        const latecomerData = {
            name: document.getElementById("name").value,
            department: document.getElementById("department").value,
            intime: document.getElementById("intime").value,
            reason: document.getElementById("reason").value,
            date: new Date().toISOString().split("T")[0] // Store today's date
        };

        fetch("/submit_latecomer", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(latecomerData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            document.getElementById("latecomerForm").reset();
        })
        .catch(error => console.error("Error:", error));
    });
});