function cargarResumen() {
    var pendientes = 0;
    var aceptadas = 0;
    var activas = 0;
    for (var i = 0; i < datos.solicitudes.length; i++) {
        var solicitud = datos.solicitudes[i];
        if (rol === "tutor" && solicitud.tutor !== 1) {
            continue;
        }
        if (solicitud.estado === "Pendiente") {
            pendientes++;
        }
        if (solicitud.estado === "Aceptada") {
            aceptadas++;
        }
    }
    for (var j = 0; j < datos.materias.length; j++) {
        if (datos.materias[j].activa) {
            activas++;
        }
    }
    document.getElementById("pendientes").textContent = pendientes;
    document.getElementById("aceptadas").textContent = aceptadas;
    document.getElementById("activas").textContent = activas;
}

if (sesionPermitida) {
    cargarResumen();
}
