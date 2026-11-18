function iniciarSesion(evento) {
    evento.preventDefault();
    var usuario = document.getElementById("usuario").value.trim().toLowerCase();
    var clave = document.getElementById("clave").value;
    if (!rolValido(usuario)) {
        mostrarError("Escribe estudiante, admin o tutor como usuario.", "usuario");
        document.getElementById("usuario").focus();
        return;
    }
    if (clave === "") {
        mostrarError("Escribe una contraseña.", "clave");
        return;
    }
    try {
        sessionStorage.setItem("tutorialink-sesion", usuario);
        window.location.href = paginaDelPanel(usuario);
    } catch (error) {
        mostrarMensaje("El navegador no permite guardar la sesión. Abre la web desde un servidor local.");
    }
}

if (sesionPermitida) {
    document.getElementById("login").addEventListener("submit", iniciarSesion);
}
