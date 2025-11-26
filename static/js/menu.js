console.log("menu.js cargado correctamente");

// Inicializar mapa centrado en Bogotá
var map = L.map("map").setView([4.65, -74.06], 14);

L.tileLayer("https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png", {
    maxZoom: 20
}).addTo(map);

// Tus marcadores...











// Lista de parqueaderos simulados
const parkings = [
    { name: "Parqueadero 1", coords: [4.654, -74.06] },
    { name: "Parqueadero 2", coords: [4.651, -74.065] },
    { name: "Parqueadero 3", coords: [4.658, -74.058] }
];

// Agregar marcadores
parkings.forEach(p => {
    L.marker(p.coords)
        .addTo(map)
        .bindPopup(`<b>${p.name}</b><br>Disponible`);
});

function irCuenta() {

    const user_id = localStorage.getItem("user_id");

    if (!user_id) {
        alert("Error: no se encontró el usuario.");
        return;
    }

    fetch(`/api/estado_verificacion/${user_id}`)
        .then(res => res.json())
        .then(data => {

            if (!data.success) {
                alert("Error consultando estado.");
                return;
            }

            if (!data.verificado) {
                window.location.href = "/verificacion";
            } else {
                window.location.href = "/micuenta";
            }
        });
}
