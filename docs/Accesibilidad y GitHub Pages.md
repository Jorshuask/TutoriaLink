# Accesibilidad y publicación en GitHub Pages

## Lo implementado

- Idioma español, un título principal por página, regiones de encabezado, navegación y contenido; logo con texto alternativo.
- Primer enlace para saltar al contenido; controles HTML nativos; foco visible; ningún control depende exclusivamente de usar ratón.
- Menú móvil con estado anunciado, control de apertura y cierre con Escape que devuelve el foco al botón.
- Etiquetas visibles, campos obligatorios indicados por texto, grupos de días/horarios/materias con leyenda e instrucciones.
- Resumen de errores mediante `role="alert"`; si se conoce el campo, `aria-invalid` y `aria-describedby` lo asocian al mensaje y se le devuelve el foco.
- Avisos de confirmación y conteos de resultados mediante regiones de estado. Los errores no desaparecen automáticamente; se retiran al corregir.
- Enlaces y botones repetidos con nombre accesible que incluye tutor, materia o fecha. Los estados se expresan con palabras además de color.
- Tras actualizar listas se conserva un punto de foco útil, evitando dejar al teclado perdido en el inicio del documento.
- Disposición adaptable, ampliación mediante navegador permitida y soporte de los colores forzados del sistema.
- No hay audio ni video, información comunicada solo por sonido ni reproducción automática. Todas las instrucciones y confirmaciones son texto; las personas sordas pueden usar el mismo recorrido. Si se incorpora multimedia, habrá que agregar subtítulos/transcripción según el contenido.

Estas medidas hacen que la web exponga una estructura útil a lectores de pantalla y tecnologías de apoyo. No requiere instalar una extensión especial para habilitar accesibilidad. No se ha certificado compatibilidad con todas las extensiones ni conformidad WCAG completa.

## Verificación realizada

Fecha: 16 de noviembre de 2026. Microsoft Edge headless y axe-core 4.10.3 con reglas WCAG 2 A/AA, 2.1 A/AA, 2.2 AA y buenas prácticas.

Se ejecutaron 24 evaluaciones de 17 HTML, cubriendo las variantes por rol, con solicitudes de varios estados. Cero violaciones automáticas detectadas. Seis evaluaciones contienen comprobaciones de contraste no concluyentes que requieren revisión manual; no equivalen a contraste aprobado.

Se probó solo con teclado el salto al contenido, el inicio de sesión, el foco y relación del error con el campo y el menú móvil con Escape. Se revisó reflow a 320 px y espaciado aumentado en formularios; se activaron colores forzados y se extrajo un ejemplo del árbol accesible. Las pruebas funcionales anteriores también pasaron tras estos cambios.

Los archivos Resultado_accesibilidad.json y arbol-accesible-ejemplo.txt registran los resultados. `python verificar_accesibilidad.py` reproduce la prueba; descarga axe-core a la caché temporal de pruebas si hace falta y verifica la integridad del paquete. La web no incorpora esa librería ni necesita descargarla para funcionar.

## Comprobaciones manuales recomendadas

1. Con NVDA + Edge/Firefox o VoiceOver + Safari, recorrer encabezados, enlaces, formularios y mensajes. Confirmar lectura comprensible y orden de foco, incluidos los diálogos de confirmación nativos.
2. Revisar las comprobaciones de contraste no concluyentes del JSON, los controles nativos y los estados con una herramienta de contraste.
3. Probar zoom real del navegador al 200 % y 400 %, sin perder información ni controles.
4. Completar el recorrido de solicitar, aceptar/rechazar y registrar seguimiento con teclado y lector de pantalla, además de probar con usuarios de tecnologías de apoyo.
5. Repetir una comprobación breve en la URL publicada.

## Preparación de GitHub Pages

La aplicación usa archivos estáticos y rutas relativas, sin backend, bibliotecas remotas ni rutas que empiecen en `/`. Se comprobó su carga bajo `/TutoriaLink/`, con el servidor de prueba rechazando peticiones fuera de esa ruta. El archivo `.nojekyll` evita el procesamiento con Jekyll.

Sube el contenido de la carpeta de entrega a la raíz del repositorio Jorshuask/TutoriaLink. `index.html`, `src` y `.nojekyll` deben quedar en esa raíz, junto a los demás HTML. En Settings → Pages, selecciona Deploy from a branch, la rama que contenga los archivos (normalmente main) y /(root). No selecciones /docs: en este proyecto esa carpeta contiene documentación, no la página de entrada.

URL esperada al habilitarlo, si se mantiene ese repositorio y no hay un dominio personalizado: https://jorshuask.github.io/TutoriaLink/ . No se presenta como una URL desplegada y verificada todavía.

GitHub Pages sirve el frontend. Las solicitudes y perfiles se conservan solo en el navegador de cada visitante y no se comparten entre equipos. La sesión de prueba funciona entre las páginas del mismo origen y pestaña. El backend PHP/MySQL de la Fase 4 necesitará otro alojamiento.

## Fuentes de consulta

- W3C WAI, notificaciones en formularios: https://www.w3.org/WAI/tutorials/forms/notifications/
- W3C, WCAG 2.2: https://www.w3.org/TR/WCAG22/
- Deque, axe-core: https://github.com/dequelabs/axe-core
- GitHub, configuración de fuente de publicación: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- GitHub, sobre GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages
