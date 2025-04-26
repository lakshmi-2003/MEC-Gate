document.addEventListener("DOMContentLoaded", function () {
    const hostelYes = document.getElementById("hostelYes");
    const hostelNo = document.getElementById("hostelNo");
    const roomDetails = document.getElementById("roomDetails");

    function toggleFields() {
        if (hostelYes.checked) {
            roomDetails.style.display = "block"; // Show Room Number
        } 
        if (hostelNo.checked) {
            roomDetails.style.display = "none"; // Hide Room Number
        }
    }

    hostelYes.addEventListener("change", toggleFields);
    hostelNo.addEventListener("change", toggleFields);

    document.getElementById("outpassForm").addEventListener("submit", function (event) {
        event.preventDefault();

        const hostelInput = document.querySelector('input[name="hostel"]:checked');

        const outpassData = {
            name: document.getElementById("name").value,
            department: document.getElementById("department").value,
            hostel: hostelInput ? hostelInput.value : "No",
            hostel_type: hostelInput && hostelInput.value === "Yes" ? document.getElementById("hostel_type").value : null,
            room_number: hostelInput && hostelInput.value === "Yes" ? document.getElementById("room_number").value : "",
            reason: document.getElementById("reason").value,
            outtime: document.getElementById("outtime").value,
            date: new Date().toISOString().split("T")[0] // Store today's date
        };

        fetch("/submit_outpass", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(outpassData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            document.getElementById("outpassForm").reset();
            toggleFields(); // Reset visibility
        })
        .catch(error => console.error("Error:", error));
    });
});