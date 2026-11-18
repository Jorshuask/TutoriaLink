# Cómo entender el código de TutoríaLink

## ¿Está mal usar varios HTML?

No. Es una estructura normal para una web y facilita estudiar cada pantalla. Los enlaces `href` abren archivos reales. No se necesita un framework ni una aplicación de una sola página para mantener la sesión.

## Ejemplo: iniciar sesión

1. `index.html` contiene el formulario y sus dos campos.
2. Al final de la carga, `login.js` conecta el formulario con la función `iniciarSesion`.
3. La función lee los campos mediante `document.getElementById`, comprueba el usuario y guarda el rol en sessionStorage.
4. `window.location.href` abre el HTML del panel correspondiente.
5. El panel carga `sesion.js`, que lee el mismo rol y muestra los enlaces adecuados.

```javascript
function iniciarSesion(evento) {
    evento.preventDefault();
    // Aquí se leen y validan los campos del formulario.
}

document.getElementById("login").addEventListener("submit", iniciarSesion);
```

`preventDefault()` evita que el formulario recargue la página antes de que termine nuestra función. `addEventListener` indica qué función debe ejecutarse cuando ocurre un evento.

## Qué estudiar primero

1. `index.html` y `src/js/login.js`: un formulario y una función.
2. `src/js/sesion.js`: conservar el rol y cambiar de página.
3. `disponibilidad.html` y `src/js/disponibilidad.js`: leer y guardar casillas.
4. `mi-perfil.html` y `src/js/mi-perfil.js`: campos de texto y materias.
5. `src/js/datos.js`: arreglos de objetos y almacenamiento.
6. `buscar.html` y `src/js/buscar.js`: recorrer tutores con un `for` y aplicar filtros.
7. `solicitar.html` y `src/js/solicitar.js`: validar y guardar un registro.
8. `src/js/solicitudes.js`: mostrar listas y modificar su estado.

## HTML y datos variables

Los títulos y formularios están escritos en sus archivos HTML. Los resultados de búsqueda y las solicitudes dependen de los datos, por eso JavaScript crea esos elementos con `document.createElement` y escribe sus textos con `textContent`. No se genera toda la pantalla dentro de una cadena de texto ni se inserta el contenido del usuario como HTML.

## Por qué hay archivos compartidos

`datos.js`, `utilidades.js` y `sesion.js` se cargan en ese orden antes del archivo de cada pantalla. Esto evita repetir funciones de almacenamiento y sesión en 17 páginas. La etiqueta `defer` permite ejecutar los scripts después de que el navegador lea el HTML y respeta su orden.

El menú sí se repite en cada HTML para que sea visible al estudiar el archivo; `sesion.js` oculta los enlaces de otros roles. Eso es una decisión de sencillez para esta fase. En PHP se podrá compartir el encabezado con un `include`.

## Sesión y servidor local

sessionStorage conserva el rol entre páginas del mismo origen y de la misma pestaña. localStorage conserva materias, solicitudes y perfiles al recargar. El puerto y la dirección forman parte del origen. Abre siempre la web desde la misma dirección, por ejemplo http://localhost:8000.

Con archivos abiertos por doble clic (`file://`) no se puede asegurar que todos los navegadores compartan el almacenamiento. Usa `iniciar.bat`, Live Server o GitHub Pages. Esto sigue siendo un frontend estático: el servidor local solo entrega archivos y no autentica usuarios.

En la Fase 4, PHP podrá mantener una sesión real del lado del servidor y comprobar los permisos en cada petición. Tener varios HTML ahora no impide hacerlo después.
