function cargarRegistros() {
    var lista = document.getElementById("listaRegistros");
    if (datos.registros.length === 0) {
        agregarTexto(lista, "p", "Todavía no hay cambios registrados.", "tarjeta");
    }
    for (var i = 0; i < datos.registros.length; i++) {
        var registro = datos.registros[i];
        agregarTexto(lista, "p", registro.fecha + " · " + registro.accion, "tarjeta");
    }
}

if (sesionPermitida) {
    cargarRegistros();
}
