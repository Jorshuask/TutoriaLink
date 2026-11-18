// Datos de ejemplo y almacenamiento compartido entre las páginas.
// Las claves se mantienen para conservar la información de la versión anterior.
var tutores = [
    { id: 1, nombre: "Ana Rodríguez", bio: "Estudiante de 5.º año · Ingeniería Civil",
      materias: ["Cálculo I", "Cálculo II", "Física I"], horas: ["14:00", "15:00"], dias: [1, 2, 3, 4, 5] },
    { id: 2, nombre: "Carlos Pérez", bio: "Docente auxiliar · Matemática",
      materias: ["Cálculo I", "Álgebra lineal"], horas: ["16:00", "17:00"], dias: [1, 3, 5] },
    { id: 3, nombre: "Sofía Gómez", bio: "Estudiante de 4.º año · Ingeniería de Software",
      materias: ["Cálculo I", "Programación"], horas: ["17:00", "18:00"], dias: [2, 4] }
];
var nombresDias = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];

function crearDatosIniciales() {
    return {
        solicitudes: [],
        materias: [
            { nombre: "Cálculo I", activa: true },
            { nombre: "Cálculo II", activa: true },
            { nombre: "Física I", activa: true },
            { nombre: "Álgebra lineal", activa: true },
            { nombre: "Programación", activa: true }
        ],
        usuarios: [
            { nombre: "Laura Méndez", rol: "Estudiante", activo: true },
            { nombre: "Ana Rodríguez", rol: "Tutor", activo: true }
        ],
        registros: [],
        disponibilidad: ["14:00", "15:00"],
        diasDisponibles: [1, 2, 3, 4, 5],
        materiasTutor: ["Cálculo I", "Cálculo II", "Física I"],
        perfiles: {}
    };
}

function cargarDatos() {
    var iniciales = crearDatosIniciales();
    try {
        var texto = localStorage.getItem("tutorialink-fase3");
        if (texto !== null) {
            var guardados = JSON.parse(texto);
            // Completar campos que no existían en versiones anteriores.
            for (var propiedad in iniciales) {
                if (guardados[propiedad] === undefined) {
                    guardados[propiedad] = iniciales[propiedad];
                }
            }
            return guardados;
        }
    } catch (error) {
        console.warn("No se pudieron leer los datos guardados.", error);
    }
    return iniciales;
}

var datos = cargarDatos();

// ===== INICIO DATOS DE EJEMPLO (para la demostración; se puede borrar todo este bloque) =====
// Agrega solicitudes de muestra una sola vez para que las pantallas no aparezcan vacías.
// Las fechas se calculan desde hoy: las pendientes y aceptadas siempre quedan en el futuro.
function fechaDeEjemplo(desdeHoy, diasPermitidos) {
    var fecha = new Date();
    fecha.setHours(12, 0, 0, 0);
    fecha.setDate(fecha.getDate() + desdeHoy);
    var paso = desdeHoy < 0 ? -1 : 1;
    while (diasPermitidos.indexOf(fecha.getDay()) === -1) {
        fecha.setDate(fecha.getDate() + paso);
    }
    var mes = String(fecha.getMonth() + 1);
    var dia = String(fecha.getDate());
    return fecha.getFullYear() + "-" + (mes.length < 2 ? "0" + mes : mes) + "-" + (dia.length < 2 ? "0" + dia : dia);
}

function agregarDatosDeEjemplo() {
    if (datos.ejemplosCargados) {
        return;
    }
    var ejemplos = [
        { id: 101, tutor: 1, materia: "Cálculo I", fecha: fechaDeEjemplo(2, [1, 2, 3, 4, 5]), hora: "14:00",
          modalidad: "Presencial", motivo: "Repasar límites y continuidad para el parcial.", estado: "Pendiente" },
        { id: 102, tutor: 1, materia: "Física I", fecha: fechaDeEjemplo(4, [1, 2, 3, 4, 5]), hora: "15:00",
          modalidad: "Virtual", motivo: "Dudas con los ejercicios de cinemática del taller 2.", estado: "Pendiente" },
        { id: 103, tutor: 1, materia: "Cálculo II", fecha: fechaDeEjemplo(1, [1, 2, 3, 4, 5]), hora: "15:00",
          modalidad: "Virtual", motivo: "Practicar integrales por partes y sustitución.", estado: "Aceptada" },
        { id: 104, tutor: 2, materia: "Álgebra lineal", fecha: fechaDeEjemplo(3, [1, 3, 5]), hora: "16:00",
          modalidad: "Presencial", motivo: "Entender cómo se calculan determinantes de 3x3.", estado: "Aceptada" },
        { id: 105, tutor: 1, materia: "Cálculo I", fecha: fechaDeEjemplo(-7, [1, 2, 3, 4, 5]), hora: "14:00",
          modalidad: "Presencial", motivo: "Repaso de derivadas antes de la prueba corta.", estado: "Realizada",
          resumen: "Se repasaron la regla de la cadena y derivadas implícitas. Recomendación: practicar los ejercicios 5 al 12 de la guía." },
        { id: 106, tutor: 3, materia: "Programación", fecha: fechaDeEjemplo(-5, [2, 4]), hora: "17:00",
          modalidad: "Virtual", motivo: "Revisar ciclos y arreglos en JavaScript.", estado: "Rechazada" }
    ];
    for (var i = 0; i < ejemplos.length; i++) {
        datos.solicitudes.push(ejemplos[i]);
    }
    datos.usuarios.push(
        { nombre: "José Castillo", correo: "jose.castillo@utp.ac.pa", rol: "Estudiante", activo: true },
        { nombre: "María Ortega", correo: "maria.ortega@utp.ac.pa", rol: "Estudiante", activo: true },
        { nombre: "Carlos Pérez", rol: "Tutor", activo: true },
        { nombre: "Sofía Gómez", rol: "Tutor", activo: true }
    );
    datos.ejemplosCargados = true;
    try {
        localStorage.setItem("tutorialink-fase3", JSON.stringify(datos));
    } catch (error) {
        console.warn("No se pudieron guardar los datos de ejemplo.", error);
    }
}
agregarDatosDeEjemplo();
// ===== FIN DATOS DE EJEMPLO =====
if (datos.perfiles.tutor) {
    tutores[0].nombre = datos.perfiles.tutor.nombre;
    if (datos.perfiles.tutor.bio !== "") {
        tutores[0].bio = datos.perfiles.tutor.bio;
    }
}

function guardarDatos(accion) {
    var registro = { accion: accion, fecha: new Date().toLocaleString("es-PA") };
    datos.registros.unshift(registro);
    try {
        localStorage.setItem("tutorialink-fase3", JSON.stringify(datos));
        return true;
    } catch (error) {
        mostrarMensaje("No se pudo guardar. Abre la aplicación desde un servidor local y permite el almacenamiento del navegador.");
        return false;
    }
}

function buscarTutor(id) {
    for (var i = 0; i < tutores.length; i++) {
        if (tutores[i].id === id) {
            return tutores[i];
        }
    }
    return null;
}

function materiasDelTutor(tutor) {
    if (tutor.id === 1) {
        return datos.materiasTutor;
    }
    return tutor.materias;
}

function diasDelTutor(tutor) {
    if (tutor.id === 1) {
        return datos.diasDisponibles;
    }
    return tutor.dias;
}

function horasDelTutor(tutor) {
    if (tutor.id === 1) {
        return datos.disponibilidad;
    }
    return tutor.horas;
}

function materiaActiva(nombre) {
    for (var i = 0; i < datos.materias.length; i++) {
        if (datos.materias[i].nombre === nombre && datos.materias[i].activa) {
            return true;
        }
    }
    return false;
}

function materiasActivasDelTutor(tutor) {
    var resultado = [];
    var materias = materiasDelTutor(tutor);
    for (var i = 0; i < materias.length; i++) {
        if (materiaActiva(materias[i])) {
            resultado.push(materias[i]);
        }
    }
    return resultado;
}

function horarioOcupado(tutorId, fecha, hora, ignorarId, soloConfirmadas) {
    for (var i = 0; i < datos.solicitudes.length; i++) {
        var solicitud = datos.solicitudes[i];
        var reserva = solicitud.estado === "Aceptada" || solicitud.estado === "Realizada";
        if (!soloConfirmadas && solicitud.estado === "Pendiente") {
            reserva = true;
        }
        if (solicitud.id !== ignorarId && solicitud.tutor === tutorId &&
            solicitud.fecha === fecha && solicitud.hora === hora && reserva) {
            return true;
        }
    }
    return false;
}
