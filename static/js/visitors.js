document.addEventListener("DOMContentLoaded", function () {
    const vehicleYes = document.getElementById("vehicleYes");
    const vehicleNo = document.getElementById("vehicleNo");
    const vehicleDetails = document.getElementById("vehicleDetails");

    function toggleVehicleDetails() {
        vehicleDetails.style.display = vehicleYes.checked ? "block" : "none";
    }

    vehicleYes.addEventListener("change", toggleVehicleDetails);
    vehicleNo.addEventListener("change", toggleVehicleDetails);
    vehicleDetails.style.display = "none"; // Hide by default

    // Form submission
    document.getElementById("visitorForm").addEventListener("submit", function (event) {
        event.preventDefault();

        const vehicleInput = document.querySelector('input[name="vehicle"]:checked');
        const vehicleValue = vehicleInput ? vehicleInput.value : "No";

        const visitorData = {
            name: document.getElementById("name").value,
            mobile: document.getElementById("mobile").value,
            purpose: document.getElementById("purpose").value,
            vehicle: vehicleValue,
            vehicle_type: vehicleValue === "Yes" ? document.getElementById("vehicle_type").value : "",
            vehicle_number: vehicleValue === "Yes" ? document.getElementById("vehicle_number").value : "",
            intime: document.getElementById("intime").value
        };

        fetch("/submit_visitor", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(visitorData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            document.getElementById("visitorForm").reset();
            toggleVehicleDetails(); // Hide vehicle fields after reset
            fetchVisitors(); // Reload table after submission
        })
        .catch(error => console.error("Error:", error));
    });

    function fetchVisitors() {
        fetch("/get_visitors")
        .then(response => response.json())
        .then(visitors => {
            console.log("Fetched Visitors:", visitors); // Debugging line

            const visitorTableBody = document.getElementById("visitorTableBody");
            visitorTableBody.innerHTML = ""; // Clear previous data

            visitors.forEach(visitor => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${visitor.name}</td>
                    <td>${visitor.mobile}</td>
                    <td>${visitor.purpose}</td>
                    <td>${visitor.intime}</td>
                    <td>
                        <button class="outtime-btn" data-id="${visitor.id}">Set Out-Time</button>
                    </td>
                `;
                visitorTableBody.appendChild(row);
            });

            // Attach event listeners to dynamically created buttons
            document.querySelectorAll(".outtime-btn").forEach(button => {
                button.addEventListener("click", function () {
                    updateOuttime(this.dataset.id);
                });
            });
        })
        .catch(error => console.error("Error fetching visitors:", error));
    }

    // Load visitors when the page loads
    fetchVisitors();
});

// ✅ Define `updateOuttime` globally
function updateOuttime(visitorId) {
    console.log("Updating Out-Time for ID:", visitorId); // Debugging line

    const now = new Date();
    const outtime = now.toLocaleTimeString('en-US', { hour12: false });

    fetch("/update_outtime", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: visitorId, outtime: outtime })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);

        // 🟢 **Update the specific row without full refresh**
        const row = document.querySelector(`button[data-id="${visitorId}"]`).closest("tr");
        if (row) {
            row.innerHTML = `
                <td>${row.cells[0].textContent}</td>
                <td>${row.cells[1].textContent}</td>
                <td>${row.cells[2].textContent}</td>
                <td>${row.cells[3].textContent}</td>
                <td>${outtime}</td>
            `;
        }
    })
    .catch(error => console.error("Error updating out-time:", error));
}