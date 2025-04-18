function showPopup(id) {
    document.getElementById(id).style.display = "flex";
}

function closePopup(id) {
    document.getElementById(id).style.display = "none";
}

// Add Bus Function
function addBus() {
    let bus_number = document.getElementById("bus_number").value;
    let bus_route = document.getElementById("bus_route").value;

    fetch('/add_bus', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bus_number: bus_number, bus_route: bus_route })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        closePopup('addBusPopup');
        location.reload(); // Refresh page to update bus list
    });
}

// Remove Bus Function
function removeBus() {
    let bus_number = document.getElementById("remove_bus_number").value;

    fetch('/remove_bus', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bus_number: bus_number })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        closePopup('removeBusPopup');
        location.reload();
    });
}