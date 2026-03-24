//alert("Hola mundo")
let map;
let geocoder;
let marker = null;

// Inicializar mapa
function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 13,
        center: { lat: 28.6353, lng: -106.0889 }
    });

    geocoder = new google.maps.Geocoder();
}

// Mostrar mapa tipo modal
function verUbicacion(direccion) {

    const overlay = document.getElementById("mapa-overlay");
    overlay.style.display = "flex";

    // Si no existe el mapa, crearlo
    if (!map) {
        initMap();
    }

    geocoder.geocode({ address: direccion }, function(results, status) {

        if (status === "OK") {

            const location = results[0].geometry.location;

            map.setCenter(location);

            // eliminar marcador anterior
            if (marker) {
                marker.setMap(null);
            }

            marker = new google.maps.Marker({
                map: map,
                position: location
            });

        } else {
            alert("Error: " + status);
        }
    });
}

// Cerrar mapa
function cerrarMapa() {
    document.getElementById("mapa-overlay").style.display = "none";
}

function cerrarMapa(event) {

    const overlay = document.getElementById("mapa-overlay");

    // Solo cerrar si clic fuera del contenido
    if (!event || event.target.id === "mapa-overlay") {
        overlay.style.display = "none";
    }
}