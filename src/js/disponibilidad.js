function cargarDisponibilidad() {
    var dias = document.querySelectorAll('input[name="dia"]');
    var horas = document.querySelectorAll('input[name="horario"]');
    for (var i = 0; i < dias.length; i++) {
        dias[i].checked = datos.diasDisponibles.indexOf(Number(dias[i].value)) !== -1;
    }
    for (var j = 0; j < horas.length; j++) {
        horas[j].checked = datos.disponibilidad.indexOf(horas[j].value) !== -1;
    }
}

function guardarDisponibilidad(evento) {
    evento.preventDefault();
    var dias = valoresSeleccionados("dia");
    var horas = valoresSeleccionados("horario");
    if (dias.length === 0) {
        mostrarError("Selecciona al menos un día disponible.");
        return;
    }
    if (horas.length === 0) {
        mostrarError("Selecciona al menos un horario.");
        return;
    }
    datos.diasDisponibles = [];
    for (var i = 0; i < dias.length; i++) {
        datos.diasDisponibles.push(Number(dias[i]));
    }
    datos.disponibilidad = horas;
    if (guardarDatos("Disponibilidad actualizada")) {
        mostrarMensaje("Días y horarios guardados. Las sesiones ya aceptadas conservan su fecha y hora.");
    }
}

if (sesionPermitida) {
    cargarDisponibilidad();
    document.getElementById("disponibilidad").addEventListener("submit", guardarDisponibilidad);
}
