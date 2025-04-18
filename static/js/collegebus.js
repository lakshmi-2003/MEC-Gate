document.addEventListener("DOMContentLoaded", function () {
    fetchBusLogs();

    function fetchBusLogs() {
        fetch("/get_bus_logs")
            .then(response => response.json())
            .then(data => {
                console.log("DEBUG Data from Flask:", data); // ✅ Debugging
                const tableBody = document.querySelector("#busLogs");

                // ✅ Clear existing content before adding new rows
                tableBody.innerHTML = "";

                // ✅ If no buses are found, show a message
                if (data.length === 0) {
                    tableBody.innerHTML = "<tr><td colspan='7'>No buses available</td></tr>";
                    return;
                }

                // ✅ Loop through data and populate the table
                data.forEach((bus, index) => {
                    const row = document.createElement("tr");

                    row.innerHTML = `
                        <td>${index + 1}</td>
                        <td>${bus.bus_number}</td>
                        <td>${bus.bus_route}</td>
                        <td>${bus.date}</td>
                        <td class="intime-cell" data-id="${bus.bus_id}">
                        ${bus.intime !== '-' ? bus.intime : `<button class="intime-btn" data-id="${bus.bus_id}">Set In-Time</button>`}
                        </td>
                        <td class="outtime-cell" data-id="${bus.bus_id}">
                            ${bus.outtime === '-' ? `<button class="outtime-btn" data-id="${bus.bus_id}" ${bus.intime === '-' ? 'disabled' : ''}>Set Out-Time</button>` : bus.outtime}
                        </td>
                    `;

                    tableBody.appendChild(row);
                });

                attachEventListeners();
            })
            .catch(error => console.error("Error fetching data:", error));
    }
    document.querySelector("#searchInput").addEventListener("keyup", function () {
        const searchValue = this.value.toLowerCase();
        document.querySelectorAll("#busLogs tr").forEach(row => {
            const busNumber = row.querySelector(".bus-number")?.textContent.toLowerCase();
            if (busNumber.includes(searchValue)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });

    function attachEventListeners() {
        document.querySelectorAll(".intime-btn").forEach(button => {
            button.addEventListener("click", function () {
                const busId = this.dataset.id;
                const intimeCell = this.parentElement;

                fetch(`/set_intime/${busId}`, { method: "POST" })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            intimeCell.innerHTML = data.intime; // Replace button with intime
                            const outtimeBtn = document.querySelector(`.outtime-cell[data-id="${busId}"] button`);
                            if (outtimeBtn) outtimeBtn.disabled = false; // Enable outtime button
                        }
                    });
            });
        });

        document.querySelectorAll(".outtime-btn").forEach(button => {
            button.addEventListener("click", function () {
                const busId = this.dataset.id;
                const outtimeCell = this.parentElement;

                fetch(`/set_outtime/${busId}`, { method: "POST" })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            outtimeCell.innerHTML = data.outtime; // Replace button with outtime
                        }
                    });
            });
        });
    }
});
