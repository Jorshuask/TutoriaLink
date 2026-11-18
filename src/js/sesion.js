// La sesión solo guarda el rol de prueba; nunca guarda contraseñas.
// Esto organiza las vistas del frontend, no sustituye la seguridad de un servidor.
var rol = null;
try {
    rol = sessionStorage.getItem("tutorialink-sesion");
} catch (error) {
    console.warn("No se pudo leer la sesión.", error);
}

function paginaDelPanel(tipo) {
    if (tipo === "tutor") {
        return "panel-tutor.html";
    }
    if (tipo === "admin") {
        return "panel-admin.html";
    }
    return "panel-estudiante.html";
}

function rolValido(tipo) {
    return tipo === "estudiante" || tipo === "tutor" || tipo === "admin";
}

function cerrarSesion(evento) {
    evento.preventDefault();
    try {
        sessionStorage.removeItem("tutorialink-sesion");
        window.location.href = "index.html";
    } catch (error) {
        mostrarMensaje("El navegador no permite cerrar la sesión. Revisa sus permisos de almacenamiento.");
    }
}

function abrirMenu() {
    var navegacion = document.getElementById("navegacion");
    var abierto = navegacion.classList.toggle("abierto");
    document.getElementById("menu").setAttribute("aria-expanded", String(abierto));
}

function cerrarMenuConEscape(evento) {
    var navegacion = document.getElementById("navegacion");
    if (evento.key === "Escape" && navegacion.classList.contains("abierto")) {
        navegacion.classList.remove("abierto");
        document.getElementById("menu").setAttribute("aria-expanded", "false");
        document.getElementById("menu").focus();
    }
}

function prepararSesion() {
    var permitidos = document.body.getAttribute("data-roles").split(" ");
    var botonMenu = document.getElementById("menu");
    if (permitidos.indexOf("publico") !== -1) {
        botonMenu.hidden = true;
        if (rolValido(rol)) {
            window.location.replace(paginaDelPanel(rol));
            return false;
        }
        return true;
    }
    if (!rolValido(rol)) {
        window.location.replace("index.html");
        return false;
    }
    if (permitidos.indexOf(rol) === -1) {
        window.location.replace(paginaDelPanel(rol));
        return false;
    }
    var enlaces = document.querySelectorAll("#navegacion a[data-roles]");
    var archivo = window.location.pathname.split("/").pop();
    for (var i = 0; i < enlaces.length; i++) {
        var tipos = enlaces[i].getAttribute("data-roles").split(" ");
        enlaces[i].hidden = tipos.indexOf(rol) === -1;
        if (enlaces[i].getAttribute("href") === archivo) {
            enlaces[i].setAttribute("aria-current", "page");
            enlaces[i].classList.add("activo");
        }
        if (enlaces[i].getAttribute("href") === "mi-perfil.html" && rol === "tutor") {
            enlaces[i].textContent = "Mi perfil y materias";
        }
        if (enlaces[i].getAttribute("href") === "solicitudes.html" && rol === "estudiante") {
            enlaces[i].textContent = "Mis solicitudes";
        }
        if (enlaces[i].getAttribute("href") === "historial.html" && rol === "tutor") {
            enlaces[i].textContent = "Seguimiento";
        }
    }
    document.querySelector(".logo").href = paginaDelPanel(rol);
    document.getElementById("navegacion").hidden = false;
    botonMenu.addEventListener("click", abrirMenu);
    document.addEventListener("keydown", cerrarMenuConEscape);
    document.getElementById("salir").addEventListener("click", cerrarSesion);
    return true;
}

var sesionPermitida = prepararSesion();
// Un aviso de una página anterior, por ejemplo al terminar el registro.
try {
    var avisoPendiente = sessionStorage.getItem("tutorialink-aviso");
    if (avisoPendiente && sesionPermitida) {
        mostrarMensaje(avisoPendiente);
        sessionStorage.removeItem("tutorialink-aviso");
    }
} catch (error) {
    console.warn("No se pudo recuperar el aviso.", error);
}

function avisarEnOtraPagina(texto, destino) {
    try {
        sessionStorage.setItem("tutorialink-aviso", texto);
    } catch (error) {
        console.warn("El aviso no se conservará al cambiar de página.", error);
    }
    window.location.href = destino;
}
