// Estas tres páginas comparten el mismo listado: solicitudes, calendario e historial.
var paginaLista = window.location.pathname.split("/").pop();

function compararFechas(primera, segunda) {
    return (primera.fecha + primera.hora).localeCompare(segunda.fecha + segunda.hora);
}

function obtenerSolicitudesDeLaPagina() {
    var lista = [];
    for (var i = 0; i < datos.solicitudes.length; i++) {
        var solicitud = datos.solicitudes[i];
        if (rol === "tutor" && solicitud.tutor !== 1) {
            continue;
        }
        if (paginaLista === "calendario.html" && solicitud.estado !== "Aceptada") {
            continue;
        }
        if (paginaLista === "historial.html" && solicitud.estado !== "Realizada" &&
            solicitud.estado !== "Cancelada" && solicitud.estado !== "Rechazada") {
            continue;
        }
        lista.push(solicitud);
    }
    if (paginaLista === "calendario.html") {
        lista.sort(compararFechas);
    }
    return lista;
}

function agregarBotonSolicitud(contenedor, solicitud, accion, texto, clase) {
    var boton = agregarTexto(contenedor, "button", texto, clase);
    boton.type = "button";
    boton.dataset.id = solicitud.id;
    boton.dataset.accion = accion;
    boton.setAttribute("aria-label", texto + ": " + solicitud.materia + ", " + solicitud.fecha + " a las " + solicitud.hora);
    boton.addEventListener("click", cambiarEstadoSolicitud);
}

function agregarFormularioSeguimiento(tarjeta, solicitud) {
    var formulario = document.createElement("form");
    formulario.className = "seguimiento";
    formulario.dataset.id = solicitud.id;
    var etiqueta = agregarTexto(formulario, "label", "Resumen y recomendaciones");
    etiqueta.htmlFor = "resumen" + solicitud.id;
    etiqueta.textContent += " de " + solicitud.materia + " del " + solicitud.fecha + " (obligatorio)";
    var resumen = document.createElement("textarea");
    resumen.id = etiqueta.htmlFor;
    resumen.name = "resumen";
    resumen.minLength = 10;
    resumen.maxLength = 1000;
    resumen.required = true;
    formulario.appendChild(resumen);
    var boton = agregarTexto(formulario, "button", "Guardar seguimiento y finalizar", "btn");
    boton.type = "submit";
    boton.setAttribute("aria-label", "Guardar seguimiento y finalizar: " + solicitud.materia + ", " + solicitud.fecha);
    formulario.addEventListener("submit", guardarSeguimiento);
    tarjeta.appendChild(formulario);
}

function mostrarSolicitud(solicitud) {
    var tarjeta = document.createElement("article");
    tarjeta.className = "tarjeta";
    var tutor = buscarTutor(solicitud.tutor);
    agregarTexto(tarjeta, "h2", solicitud.materia + " · " + tutor.nombre);
    agregarTexto(tarjeta, "p", solicitud.fecha + " a las " + solicitud.hora + " · " + solicitud.modalidad);
    var claseEstado = "estado ok";
    if (solicitud.estado === "Pendiente") {
        claseEstado = "estado pend";
    } else if (solicitud.estado === "Rechazada" || solicitud.estado === "Cancelada") {
        claseEstado = "estado no";
    }
    agregarTexto(tarjeta, "span", solicitud.estado, claseEstado);
    agregarTexto(tarjeta, "p", solicitud.motivo);
    var acciones = document.createElement("div");
    acciones.className = "acciones";
    if (rol === "estudiante" && (solicitud.estado === "Pendiente" || solicitud.estado === "Aceptada")) {
        agregarBotonSolicitud(acciones, solicitud, "cancelar", "Cancelar solicitud", "btn peligro");
    }
    if (rol === "tutor" && solicitud.estado === "Pendiente") {
        agregarBotonSolicitud(acciones, solicitud, "aceptar", "Aceptar", "btn");
        agregarBotonSolicitud(acciones, solicitud, "rechazar", "Rechazar", "btn peligro");
    }
    tarjeta.appendChild(acciones);
    if (rol === "tutor" && solicitud.estado === "Aceptada") {
        agregarFormularioSeguimiento(tarjeta, solicitud);
    }
    if (solicitud.resumen) {
        var detalle = document.createElement("div");
        detalle.className = "detalle";
        agregarTexto(detalle, "h3", "Seguimiento");
        agregarTexto(detalle, "p", solicitud.resumen);
        tarjeta.appendChild(detalle);
    }
    document.getElementById("listaSolicitudes").appendChild(tarjeta);
}

function cargarSolicitudes() {
    var contenedor = document.getElementById("listaSolicitudes");
    contenedor.textContent = "";
    if (paginaLista === "solicitudes.html") {
        if (rol === "tutor") {
            document.getElementById("tituloLista").textContent = "Solicitudes recibidas";
        } else {
            document.getElementById("tituloLista").textContent = "Mis solicitudes";
        }
    }
    var lista = obtenerSolicitudesDeLaPagina();
    if (lista.length === 0) {
        agregarTexto(contenedor, "p", "Todavía no hay registros en esta sección.", "tarjeta");
    }
    for (var i = 0; i < lista.length; i++) {
        mostrarSolicitud(lista[i]);
    }
}

function buscarSolicitud(id) {
    for (var i = 0; i < datos.solicitudes.length; i++) {
        if (datos.solicitudes[i].id === id) {
            return datos.solicitudes[i];
        }
    }
    return null;
}

function cambiarEstadoSolicitud(evento) {
    var boton = evento.currentTarget;
    var solicitud = buscarSolicitud(Number(boton.dataset.id));
    var accion = boton.dataset.accion;
    if (solicitud === null) {
        return;
    }
    if (accion === "cancelar" && rol === "estudiante" &&
        (solicitud.estado === "Pendiente" || solicitud.estado === "Aceptada")) {
        if (!confirm("¿Cancelar esta solicitud?")) {
            return;
        }
        solicitud.estado = "Cancelada";
    } else if (rol === "tutor" && solicitud.tutor === 1 && solicitud.estado === "Pendiente") {
        if (accion !== "aceptar" && accion !== "rechazar") {
            return;
        }
        if (!confirm("¿Deseas " + accion + " esta solicitud?")) {
            return;
        }
        if (accion === "aceptar") {
            if (new Date(solicitud.fecha + "T" + solicitud.hora) <= new Date()) {
                mostrarError("Esta fecha ya pasó. Rechaza la solicitud y pide una nueva fecha.");
                return;
            }
            if (horarioOcupado(solicitud.tutor, solicitud.fecha, solicitud.hora, solicitud.id, true)) {
                mostrarError("El horario ya está ocupado.");
                return;
            }
            solicitud.estado = "Aceptada";
        } else {
            solicitud.estado = "Rechazada";
        }
    } else {
        return;
    }
    if (guardarDatos("Solicitud " + solicitud.estado)) {
        cargarSolicitudes();
        enfocarTituloLista();
        mostrarMensaje("Solicitud actualizada: " + solicitud.estado + ".");
    }
}

function guardarSeguimiento(evento) {
    evento.preventDefault();
    var formulario = evento.currentTarget;
    var solicitud = buscarSolicitud(Number(formulario.dataset.id));
    if (solicitud === null || rol !== "tutor" || solicitud.tutor !== 1 || solicitud.estado !== "Aceptada") {
        return;
    }
    var finalizacion = new Date(solicitud.fecha + "T" + solicitud.hora).getTime() + 3600000;
    if (finalizacion > Date.now()) {
        mostrarError("Podrás finalizar la tutoría cuando termine su hora programada.");
        return;
    }
    var resumen = formulario.elements.resumen.value.trim();
    if (resumen.length < 10) {
        mostrarError("Escribe al menos 10 caracteres de seguimiento.");
        return;
    }
    solicitud.resumen = resumen;
    solicitud.estado = "Realizada";
    if (guardarDatos("Seguimiento registrado")) {
        cargarSolicitudes();
        enfocarTituloLista();
        mostrarMensaje("Seguimiento guardado. Puedes verlo en Historial.");
    }
}

if (sesionPermitida) {
    cargarSolicitudes();
}
