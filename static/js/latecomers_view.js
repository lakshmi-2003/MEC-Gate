document.getElementById("fetchData").addEventListener("click", function () {
    let selectedDate = document.getElementById("datePicker").value;

    fetch("/get_latecomers_entries", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `selected_date=${selectedDate}`
    })
    .then(response => response.json())
    .then(data => {
        let tableBody = document.getElementById("latecomersTable");
        tableBody.innerHTML = "";  

        if (data.success) {
            data.data.forEach((row,index) => {
                let tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${index+1}</td>
                    <td>${row.name}</td>
                    <td>${row.department}</td>
                    <td>${row.outtime}</td>
                    <td>${row.reason}</td>
                `;
                tableBody.appendChild(tr);
            });
        } else {
            let tr = document.createElement("tr");
            tr.innerHTML = `<td colspan="7" class="no-records">${data.message}</td>`;
            tableBody.appendChild(tr);
        }
    });
});