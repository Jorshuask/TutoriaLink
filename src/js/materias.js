function cargarMaterias() {
    var lista = document.getElementById("listaMaterias");
    lista.textContent = "";
    for (var i = 0; i < datos.materias.length; i++) {
        var materia = datos.materias[i];
        var tarjeta = document.createElement("article");
        tarjeta.className = "tarjeta";
        agregarTexto(tarjeta, "h2", materia.nombre);
        var estado = "Inactiva";
        var accion = "Activar";
        if (materia.activa) {
            estado = "Activa";
            accion = "Desactivar";
        }
        agregarTexto(tarjeta, "p", estado);
        var boton = agregarTexto(tarjeta, "button", accion, "btn sec");
        boton.type = "button";
        boton.setAttribute("aria-label", accion + ": " + materia.nombre);
        boton.dataset.indice = i;
        boton.addEventListener("click", cambiarEstadoMateria);
        lista.appendChild(tarjeta);
    }
}

function agregarMateria(evento) {
    evento.preventDefault();
    var nombre = document.getElementById("nueva").value.trim();
    if (nombre === "") {
        mostrarError("Escribe el nombre de la materia.", "nueva");
        return;
    }
    for (var i = 0; i < datos.materias.length; i++) {
        if (datos.materias[i].nombre.toLowerCase() === nombre.toLowerCase()) {
            mostrarError("Esta materia ya está registrada.", "nueva");
            return;
        }
    }
    datos.materias.push({ nombre: nombre, activa: true });
    if (guardarDatos("Materia agregada")) {
        document.getElementById("nuevaMateria").reset();
        cargarMaterias();
        document.getElementById("nueva").focus();
        mostrarMensaje("Materia agregada. El tutor puede seleccionarla en Mi perfil y materias.");
    }
}

function cambiarEstadoMateria(evento) {
    if (!confirm("¿Confirmas este cambio de estado?")) {
        return;
    }
    var indice = Number(evento.currentTarget.dataset.indice);
    datos.materias[indice].activa = !datos.materias[indice].activa;
    if (guardarDatos("Estado de materia actualizado")) {
        cargarMaterias();
        var botonNuevo = document.querySelector('#listaMaterias button[data-indice="' + indice + '"]');
        botonNuevo.focus();
        mostrarMensaje("Estado actualizado.");
    }
}

if (sesionPermitida) {
    cargarMaterias();
    document.getElementById("nuevaMateria").addEventListener("submit", agregarMateria);
}
