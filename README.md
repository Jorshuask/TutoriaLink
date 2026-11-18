# TutoríaLink — Fase 3

Repositorio del equipo: https://github.com/Jorshuask/TutoriaLink

Versión en línea: https://jorshuask.github.io/TutoriaLink/

Proyecto semestral de Ingeniería Web · UTP · Grupo 8 · 1SF-133 · II semestre de 2026.

## Abrir la aplicación

La web ahora tiene un archivo HTML por pantalla. Para que todas las páginas compartan correctamente los datos y la sesión, ábrela desde un servidor local:

1. Ejecuta `iniciar.bat` si tienes Python instalado.
2. Abre http://localhost:8000 en el navegador.
3. Mantén abierta la ventana del servidor mientras usas la web. Ctrl+C lo detiene.

También puedes abrir `index.html` con Live Server de Visual Studio Code. En GitHub Pages no hace falta ejecutar un servidor local.

No se recomienda abrir los archivos con doble clic: el almacenamiento de las páginas `file://` depende del navegador y puede estar separado por archivo. Mantén la misma dirección y puerto durante las pruebas; cada origen tiene sus propios datos.

| Usuario | Contraseña | Panel |
| --- | --- | --- |
| estudiante | Cualquier texto no vacío | panel-estudiante.html |
| tutor | Cualquier texto no vacío | panel-tutor.html |
| admin | Cualquier texto no vacío | panel-admin.html |

El acceso es una simulación frontend. Las contraseñas no se guardan. El registro crea datos de cuenta locales, pero el inicio sigue usando los tres usuarios de prueba.

## Código para principiantes

Cada HTML contiene los títulos, formularios y estructura de su pantalla. Cada JavaScript se ocupa del comportamiento de esa pantalla. Se usan funciones tradicionales, `if`, bucles `for` y eventos; no hay framework ni enrutador que genere toda la web.

Consulta `docs/Como entender el codigo.md` para el recorrido paso a paso.

## Pantallas

- `index.html`, `registro.html`: inicio de sesión y registro.
- `panel-estudiante.html`, `panel-tutor.html`, `panel-admin.html`: paneles por rol.
- `buscar.html`, `perfil-tutor.html`, `solicitar.html`: búsqueda, perfil y solicitud.
- `solicitudes.html`, `calendario.html`, `historial.html`: listados de tutorías.
- `mi-perfil.html`, `disponibilidad.html`: datos, materias, días y horas del tutor.
- `materias.html`, `usuarios.html`, `registros.html`: administración.
- `ayuda.html`: instrucciones de uso.

## Archivos compartidos

- `src/estilos.css`: diseño común, organizado por secciones.
- `src/js/datos.js`: datos de ejemplo y lectura/escritura en localStorage.
- `src/js/utilidades.js`: funciones pequeñas para mensajes y elementos repetidos.
- `src/js/sesion.js`: sesión en sessionStorage, menú y navegación por rol.
- Los demás archivos de `src/js` corresponden a las pantallas: por ejemplo, `registro.js` acompaña a `registro.html`.

Las páginas solicitudes, calendario e historial comparten `solicitudes.js`, porque muestran los mismos registros con distintos filtros. El HTML de cada una sigue siendo independiente.

## Documentación

`docs/Informe_Fase3_TutoriaLink.pdf` es el informe actualizado. Incluye portada, integrantes, capturas, validaciones, alcance de la fase y el anexo sobre el uso de inteligencia artificial. La versión editable está en Word. Las referencias y capturas se encuentran en `docs`.

## Equipo

Whorlyn Bustos, Emmanuel Hernández, Jeremy Martínez y Jorshua Jiménez.
Profesora: Dra. Elba Valderrama Bahamóndez.

## Validación

`python verificar.py` comprueba enlaces, sintaxis JavaScript y recorridos con un servidor temporal. Requiere Python, Playwright, Node y Microsoft Edge. Para usar la aplicación solo necesitas un navegador y una forma de servir estos archivos estáticos.

## Próxima fase (Fase 4)

Recuperación de contraseña, notificaciones, portada pública, contacto, reprogramación, valoración, pantallas individuales de detalle y edición completa de usuarios/materias. La Fase 4 debe incorporar PHP, MySQL, autenticación y permisos reales. Los controles actuales de rol solo organizan las vistas locales.

Los datos guardados desde la versión anterior se conservan si se usa el mismo origen del navegador. Al pasar de archivos locales a localhost o a GitHub Pages se inicia otro almacenamiento; los datos del origen anterior no se borran.


## Accesibilidad y evaluación de la rúbrica

La web incluye navegación por teclado, salto al contenido, etiquetas, avisos para lectores de pantalla, foco recuperado tras actualizar listas y nombres accesibles que distinguen acciones repetidas. La información no depende del audio ni solo del color.

Se ejecutaron 24 evaluaciones con axe-core en las 17 pantallas, sin violaciones automáticas detectadas. Esto no certifica conformidad completa: faltan revisión con lectores de pantalla reales y comprobaciones manuales de contraste. Consulta `docs/Accesibilidad y GitHub Pages.md`, `docs/Resultado_accesibilidad.json` y el informe en `docs`.

`python verificar_accesibilidad.py` reproduce la auditoría, las pruebas de teclado y el alojamiento simulado bajo `/TutoriaLink/`. La librería de auditoría se descarga solo para las pruebas, no se carga en la web.

## Publicación prevista: GitHub Pages

Sube los archivos a la raíz de Jorshuask/TutoriaLink y conserva `.nojekyll`. En Settings → Pages elige Deploy from a branch, la rama correspondiente y **/(root)**. No elijas /docs: es la documentación, no el sitio.

URL esperada cuando lo actives: https://jorshuask.github.io/TutoriaLink/ . Esta revisión deja los archivos preparados; no ha desplegado esta versión. Los datos siguen siendo locales a cada navegador y GitHub Pages no incorpora el backend PHP/MySQL.
