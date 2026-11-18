// Pequeñas funciones de apoyo para no repetir código en cada pantalla.
function mostrarMensaje(texto) {
    limpiarErrores();
    document.getElementById("aviso").textContent = texto;
}

function agregarTexto(contenedor, etiqueta, texto, clase) {
    var elemento = document.createElement(etiqueta);
    elemento.textContent = texto;
    if (clase) {
        elemento.className = clase;
    }
    contenedor.appendChild(elemento);
    return elemento;
}

function agregarOpcion(select, valor, texto) {
    var opcion = document.createElement("option");
    opcion.value = valor;
    opcion.textContent = texto;
    select.appendChild(opcion);
}

function agregarEnlace(contenedor, texto, destino, clase) {
    var enlace = agregarTexto(contenedor, "a", texto, clase);
    enlace.href = destino;
    return enlace;
}

function valoresSeleccionados(nombre) {
    var casillas = document.querySelectorAll('input[name="' + nombre + '"]:checked');
    var valores = [];
    for (var i = 0; i < casillas.length; i++) {
        valores.push(casillas[i].value);
    }
    return valores;
}

function nombresDeDias(numeros) {
    var nombres = [];
    for (var i = 0; i < numeros.length; i++) {
        nombres.push(nombresDias[numeros[i]]);
    }
    return nombres.join(", ");
}

function fechaDeHoy() {
    var fecha = new Date();
    var mes = String(fecha.getMonth() + 1).padStart(2, "0");
    var dia = String(fecha.getDate()).padStart(2, "0");
    return fecha.getFullYear() + "-" + mes + "-" + dia;
}

function idDelTutorEnUrl() {
    var parametros = new URLSearchParams(window.location.search);
    return Number(parametros.get("tutor"));
}

// El error se ve en pantalla y se anuncia al lector de pantalla.
// Si conocemos el campo, lo marcamos y ponemos allí el foco del teclado.
function mostrarError(texto, idCampo) {
    limpiarErrores();
    document.getElementById("aviso").textContent = "";
    var resumen = document.getElementById("error");
    resumen.textContent = texto;
    var campo = document.getElementById(idCampo);
    if (campo) {
        campo.setAttribute("aria-invalid", "true");
        var descripcion = campo.getAttribute("aria-describedby");
        if (descripcion) {
            campo.setAttribute("aria-describedby", descripcion + " error");
        } else {
            campo.setAttribute("aria-describedby", "error");
        }
        campo.focus();
    } else {
        resumen.focus();
    }
}

function limpiarErrores() {
    var campos = document.querySelectorAll('[aria-invalid="true"]');
    for (var i = 0; i < campos.length; i++) {
        campos[i].removeAttribute("aria-invalid");
        var descripcion = campos[i].getAttribute("aria-describedby");
        if (descripcion) {
            descripcion = descripcion.replace("error", "").trim();
            if (descripcion === "") {
                campos[i].removeAttribute("aria-describedby");
            } else {
                campos[i].setAttribute("aria-describedby", descripcion);
            }
        }
    }
    document.getElementById("error").textContent = "";
}

function enfocarTituloLista() {
    var titulo = document.getElementById("tituloLista");
    titulo.setAttribute("tabindex", "-1");
    titulo.focus();
}

// Al corregir un formulario se retiran las marcas del intento anterior.
document.addEventListener("input", limpiarErrores);
document.addEventListener("change", limpiarErrores);
