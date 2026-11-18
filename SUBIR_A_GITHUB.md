# Subir el proyecto a GitHub

## Opción desde el navegador

1. Abre el repositorio del equipo: https://github.com/Jorshuask/TutoriaLink.
2. Abre **Add file → Upload files**. Arrastra el contenido de esta carpeta, con sus subcarpetas. `index.html`, los demás HTML, `src`, `docs` y `.nojekyll` deben quedar en la raíz del repositorio.
3. Escribe un mensaje que describa los cambios y confirma la carga. No subas el ZIP como sustituto del código.
4. Revisa que GitHub muestre el README, el código y el PDF de `docs`.

Si el repositorio ya contiene fases previas, conserva su historial y sus documentos e integra este frontend en la ubicación elegida por el equipo. Evita sobrescribir archivos sin revisarlos.

## Opción con Git

Dentro de la carpeta de entrega nueva, que no incluye el historial `.git` de la carpeta de trabajo:

```powershell
git init
git add .
git commit -m "Agregar frontend y documentación de Fase 3"
git branch -M main
git remote add origin https://github.com/Jorshuask/TutoriaLink.git
git push -u origin main
```

Estos comandos presuponen un repositorio remoto vacío. Para un repositorio existente, clónalo y copia los archivos antes de hacer commit y push. La carpeta de trabajo original conserva los commits de implementación; esta copia es una exportación de archivos y no reconstruye el historial anterior.

## Publicar el frontend en GitHub Pages

En el repositorio del equipo: Settings → Pages → Deploy from a branch → la rama con los archivos (normalmente main) → /(root). No elijas /docs, porque ahí solo está la documentación. Conserva el archivo .nojekyll. Guarda y usa la URL que GitHub muestre. Se espera https://jorshuask.github.io/TutoriaLink/ si no se configura un dominio personalizado; todavía no se ha desplegado esta versión durante esta revisión. El enlace del repositorio muestra el código; el enlace de Pages abre la aplicación. Ambos conservan las limitaciones de almacenamiento local de este frontend.

## Entrega en eCampus

El PDF de Fase 3 exige implementación frontend y repositorio actualizado, pero no precisa el formato de subida. Las guías de fases 1 y 2 sí exigían PDF y enlace del repositorio en el comentario. Para cubrir ambos entregables, prepara el PDF `docs/Informe_Fase3_TutoriaLink.pdf` y el enlace real al repositorio, siguiendo cualquier instrucción específica de la actividad de Fase 3 en eCampus.

El repositorio del equipo ya está indicado. Completa los aportes individuales revisados y el enlace real de los prompts en el anexo del Word, y vuelve a exportar a PDF antes de entregar. Esta versión no se ha subido automáticamente al repositorio.
