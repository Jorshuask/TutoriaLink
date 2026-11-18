var tutorSeleccionado = null;

function cargarFormularioSolicitud() {
    tutorSeleccionado = buscarTutor(idDelTutorEnUrl());
    if (tutorSeleccionado === null) {
        mostrarMensaje("Tutor no encontrado. Vuelve a Buscar tutores.");
        document.getElementById("solicitar").hidden = true;
        return;
    }
    document.getElementById("resumenTutor").textContent = "Tutor: " + tutorSeleccionado.nombre + " · duración: una hora";
    document.getElementById("fecha").min = fechaDeHoy();
    document.getElementById("diasAyuda").textContent = "Días disponibles: " + nombresDeDias(diasDelTutor(tutorSeleccionado));
    var materias = materiasActivasDelTutor(tutorSeleccionado);
    var horas = horasDelTutor(tutorSeleccionado);
    for (var i = 0; i < materias.length; i++) {
        agregarOpcion(document.getElementById("asignatura"), materias[i], materias[i]);
    }
    for (var j = 0; j < horas.length; j++) {
        agregarOpcion(document.getElementById("turno"), horas[j], horas[j]);
    }
}

function enviarSolicitud(evento) {
    evento.preventDefault();
    if (tutorSeleccionado === null) {
        return;
    }
    var fecha = document.getElementById("fecha").value;
    var hora = document.getElementById("turno").value;
    var materia = document.getElementById("asignatura").value;
    var modalidad = document.getElementById("modalidad").value;
    var motivo = document.getElementById("motivo").value.trim();
    var dia = new Date(fecha + "T12:00").getDay();
    var inicio = new Date(fecha + "T" + hora);
    if (fecha < fechaDeHoy() || inicio <= new Date() || diasDelTutor(tutorSeleccionado).indexOf(dia) === -1) {
        mostrarError("Selecciona una fecha futura y un día disponible del tutor.", "fecha");
        return;
    }
    if (horasDelTutor(tutorSeleccionado).indexOf(hora) === -1 || horarioOcupado(tutorSeleccionado.id, fecha, hora, null, false)) {
        mostrarError("Ese horario ya no está disponible. Selecciona otro.", "turno");
        return;
    }
    if (materiasActivasDelTutor(tutorSeleccionado).indexOf(materia) === -1) {
        mostrarError("Selecciona una materia disponible del tutor.", "asignatura");
        return;
    }
    if (motivo.length < 10) {
        mostrarError("Escribe un motivo de al menos 10 caracteres.", "motivo");
        return;
    }
    var solicitud = {
        id: Date.now(), tutor: tutorSeleccionado.id, materia: materia,
        fecha: fecha, hora: hora, modalidad: modalidad,
        motivo: motivo, estado: "Pendiente"
    };
    datos.solicitudes.push(solicitud);
    if (guardarDatos("Solicitud enviada")) {
        avisarEnOtraPagina("Tu solicitud se registró y está pendiente de respuesta.", "solicitudes.html");
    }
}

if (sesionPermitida) {
    cargarFormularioSolicitud();
    document.getElementById("solicitar").addEventListener("submit", enviarSolicitud);
}
