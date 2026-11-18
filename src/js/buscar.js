function cargarFiltroMaterias() {
    var select = document.getElementById("materia");
    for (var i = 0; i < datos.materias.length; i++) {
        if (datos.materias[i].activa) {
            agregarOpcion(select, datos.materias[i].nombre, datos.materias[i].nombre);
        }
    }
}

function mostrarTarjetaTutor(tutor) {
    var contenedor = document.getElementById("resultados");
    var tarjeta = document.createElement("article");
    tarjeta.className = "tarjeta res";
    var partes = tutor.nombre.split(" ");
    var iniciales = "";
    for (var i = 0; i < partes.length; i++) {
        iniciales += partes[i].charAt(0);
    }
    var foto = agregarTexto(tarjeta, "div", iniciales, "foto");
    foto.setAttribute("aria-hidden", "true");
    var informacion = document.createElement("div");
    informacion.className = "info";
    agregarTexto(informacion, "h2", tutor.nombre);
    agregarTexto(informacion, "p", tutor.bio);
    var materias = materiasActivasDelTutor(tutor);
    var etiquetas = document.createElement("p");
    for (var j = 0; j < materias.length; j++) {
        agregarTexto(etiquetas, "span", materias[j], "chip");
    }
    informacion.appendChild(etiquetas);
    agregarTexto(informacion, "p", "Horarios: " + horasDelTutor(tutor).join(", "));
    var acciones = document.createElement("div");
    acciones.className = "acciones";
    var perfil = agregarEnlace(acciones, "Ver perfil", "perfil-tutor.html?tutor=" + tutor.id, "btn sec");
    perfil.setAttribute("aria-label", "Ver perfil de " + tutor.nombre);
    var solicitar = agregarEnlace(acciones, "Solicitar", "solicitar.html?tutor=" + tutor.id, "btn");
    solicitar.setAttribute("aria-label", "Solicitar tutoría con " + tutor.nombre);
    informacion.appendChild(acciones);
    tarjeta.appendChild(informacion);
    contenedor.appendChild(tarjeta);
}

function buscarTutores(evento) {
    if (evento) {
        evento.preventDefault();
    }
    var materia = document.getElementById("materia").value;
    var dia = document.getElementById("dia").value;
    var hora = document.getElementById("hora").value;
    var cantidad = 0;
    var resultados = document.getElementById("resultados");
    resultados.textContent = "";
    for (var i = 0; i < tutores.length; i++) {
        var tutor = tutores[i];
        var materias = materiasActivasDelTutor(tutor);
        if (materias.length === 0) {
            continue;
        }
        if (materia !== "" && materias.indexOf(materia) === -1) {
            continue;
        }
        if (dia !== "" && diasDelTutor(tutor).indexOf(Number(dia)) === -1) {
            continue;
        }
        if (hora !== "" && horasDelTutor(tutor).indexOf(hora) === -1) {
            continue;
        }
        mostrarTarjetaTutor(tutor);
        cantidad++;
    }
    document.getElementById("cantidad").textContent = cantidad + " tutores encontrados";
    if (cantidad === 0) {
        agregarTexto(resultados, "p", "No encontramos tutores con esos filtros. Prueba otra materia o día.", "tarjeta");
    }
}

if (sesionPermitida) {
    cargarFiltroMaterias();
    buscarTutores();
    document.getElementById("filtros").addEventListener("submit", buscarTutores);
}
