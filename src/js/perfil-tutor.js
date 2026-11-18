function cargarPerfilTutor() {
    var tutor = buscarTutor(idDelTutorEnUrl());
    if (tutor === null) {
        document.getElementById("nombreTutor").textContent = "Tutor no encontrado";
        document.getElementById("detalleTutor").hidden = true;
        return;
    }
    document.getElementById("nombreTutor").textContent = tutor.nombre;
    document.getElementById("bioTutor").textContent = tutor.bio;
    document.getElementById("materiasTutor").textContent = "Materias: " + materiasActivasDelTutor(tutor).join(", ");
    document.getElementById("diasTutor").textContent = "Días disponibles: " + nombresDeDias(diasDelTutor(tutor));
    document.getElementById("horasTutor").textContent = "Horas: " + horasDelTutor(tutor).join(", ");
    document.getElementById("enlaceSolicitud").href = "solicitar.html?tutor=" + tutor.id;
}

if (sesionPermitida) {
    cargarPerfilTutor();
}
