document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("vpn-form");
    if (!form) {
        console.error("Formulario no encontrado. Verifica que el ID 'vpn-form' existe en el HTML.");
        return;
    }

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const data = {
            zone1_name: document.getElementById("zone1-name").value,
            zone1_interface: document.getElementById("zone1-interface").value,
            zone1_ip: document.getElementById("zone1-network").value,
            zone1_network: document.getElementById("zone1-network").value,
            zone2_name: document.getElementById("zone2-name").value,
            zone2_interface: document.getElementById("zone2-interface").value,
            zone2_ip: document.getElementById("remote-ip").value,
            zone2_network: document.getElementById("zone2-network").value,
            ike_secret: document.getElementById("ike-secret").value,
        };

        fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById("output").textContent = result.config;
        })
        .catch(error => console.error("Error:", error));
    });
});