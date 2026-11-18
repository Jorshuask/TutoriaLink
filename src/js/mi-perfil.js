function cargarMiPerfil() {
    var perfil = datos.perfiles[rol];
    if (!perfil) {
        var nombre = "Laura Méndez";
        if (rol === "tutor") {
            nombre = "Ana Rodríguez";
        } else if (rol === "admin") {
            nombre = "Administrador";
        }
        perfil = { nombre: nombre, correo: "", bio: "" };
    }
    document.getElementById("nombrePerfil").value = perfil.nombre;
    document.getElementById("correoPerfil").value = perfil.correo;
    document.getElementById("biografia").value = perfil.bio;
    if (rol !== "tutor") {
        return;
    }
    document.getElementById("tituloPerfil").textContent = "Mi perfil y materias";
    document.getElementById("seccionMaterias").hidden = false;
    var opciones = document.getElementById("opcionesMaterias");
    for (var i = 0; i < datos.materias.length; i++) {
        var materia = datos.materias[i];
        if (!materia.activa) {
            continue;
        }
        var etiqueta = document.createElement("label");
        var casilla = document.createElement("input");
        casilla.type = "checkbox";
        casilla.name = "materiaTutor";
        casilla.value = materia.nombre;
        casilla.checked = datos.materiasTutor.indexOf(materia.nombre) !== -1;
        etiqueta.appendChild(casilla);
        etiqueta.appendChild(document.createTextNode(" " + materia.nombre));
        opciones.appendChild(etiqueta);
    }
}

function guardarMiPerfil(evento) {
    evento.preventDefault();
    var nombre = document.getElementById("nombrePerfil").value.trim();
    if (nombre === "") {
        mostrarError("Escribe tu nombre.", "nombrePerfil");
        return;
    }
    if (rol === "tutor") {
        var seleccion = valoresSeleccionados("materiaTutor");
        if (seleccion.length === 0) {
            mostrarError("Selecciona al menos una materia que impartes.");
            return;
        }
        datos.materiasTutor = seleccion;
    }
    datos.perfiles[rol] = {
        nombre: nombre,
        correo: document.getElementById("correoPerfil").value.trim(),
        bio: document.getElementById("biografia").value.trim()
    };
    if (guardarDatos("Perfil y materias actualizados")) {
        mostrarMensaje("Perfil guardado.");
    }
}

if (sesionPermitida) {
    cargarMiPerfil();
    document.getElementById("miPerfil").addEventListener("submit", guardarMiPerfil);
}
