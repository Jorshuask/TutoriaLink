function cargarUsuarios() {
    var lista = document.getElementById("listaUsuarios");
    lista.textContent = "";
    for (var i = 0; i < datos.usuarios.length; i++) {
        var usuario = datos.usuarios[i];
        var tarjeta = document.createElement("article");
        tarjeta.className = "tarjeta";
        agregarTexto(tarjeta, "h2", usuario.nombre);
        var estado = "Inactivo";
        var accion = "Activar";
        if (usuario.activo) {
            estado = "Activo";
            accion = "Desactivar";
        }
        agregarTexto(tarjeta, "p", usuario.rol + " · " + estado);
        var boton = agregarTexto(tarjeta, "button", accion, "btn sec");
        boton.type = "button";
        boton.setAttribute("aria-label", accion + ": " + usuario.nombre);
        boton.dataset.indice = i;
        boton.addEventListener("click", cambiarEstadoUsuario);
        lista.appendChild(tarjeta);
    }
}

function cambiarEstadoUsuario(evento) {
    if (!confirm("¿Confirmas este cambio de estado?")) {
        return;
    }
    var indice = Number(evento.currentTarget.dataset.indice);
    datos.usuarios[indice].activo = !datos.usuarios[indice].activo;
    if (guardarDatos("Estado de usuario actualizado")) {
        cargarUsuarios();
        var botonNuevo = document.querySelector('#listaUsuarios button[data-indice="' + indice + '"]');
        botonNuevo.focus();
        mostrarMensaje("Estado actualizado.");
    }
}

if (sesionPermitida) {
    cargarUsuarios();
}
