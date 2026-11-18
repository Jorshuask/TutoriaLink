function registrarCuenta(evento) {
    evento.preventDefault();
    var nombre = document.getElementById("nombreRegistro").value.trim();
    var correo = document.getElementById("correoRegistro").value.trim();
    var tipo = document.getElementById("rolRegistro").value;
    var clave = document.getElementById("claveRegistro").value;
    var confirmar = document.getElementById("confirmarRegistro").value;
    if (nombre === "") {
        mostrarError("Escribe tu nombre completo.", "nombreRegistro");
        return;
    }
    if (clave !== confirmar) {
        mostrarError("Las contraseñas deben coincidir.", "confirmarRegistro");
        return;
    }
    for (var i = 0; i < datos.usuarios.length; i++) {
        var usuario = datos.usuarios[i];
        if (usuario.correo && usuario.correo.toLowerCase() === correo.toLowerCase()) {
            mostrarError("Este correo ya está registrado.", "correoRegistro");
            return;
        }
    }
    var nuevo = { nombre: nombre, correo: correo, rol: "Estudiante", activo: true };
    if (tipo === "tutor") {
        nuevo.rol = "Tutor";
    }
    // La contraseña se valida, pero no se almacena en esta versión frontend.
    datos.usuarios.push(nuevo);
    if (guardarDatos("Registro de cuenta")) {
        avisarEnOtraPagina("Cuenta registrada en este navegador. Para entrar utiliza " + tipo + " y cualquier contraseña.", "index.html");
    }
}

if (sesionPermitida) {
    document.getElementById("registro").addEventListener("submit", registrarCuenta);
}
