"""Genera el PDF y Word de Fase 3 a partir del contenido y las capturas locales."""
from pathlib import Path
from datetime import date
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from docx import Document
from docx.shared import Inches

BASE=Path(__file__).resolve().parent
DOCS=BASE/'docs'
DOCS.mkdir(exist_ok=True)
# Utiliza Times New Roman del sistema sin redistribuir sus archivos de fuente.
fontdir=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'
if (fontdir/'times.ttf').exists():
    for name,file in [('TNR','times.ttf'),('TNR-Bold','timesbd.ttf'),('TNR-Italic','timesi.ttf'),('TNR-BoldItalic','timesbi.ttf')]:
        pdfmetrics.registerFont(TTFont(name,str(fontdir/file)))
    pdfmetrics.registerFontFamily('TNR',normal='TNR',bold='TNR-Bold',italic='TNR-Italic',boldItalic='TNR-BoldItalic')
    normal,bold='TNR','TNR-Bold'
else:
    normal,bold='Times-Roman','Times-Bold'
styles=getSampleStyleSheet()
for name in ['BodyText','Normal','Title','Heading1','Heading2']:
    styles[name].fontName=bold if name in ['Heading1','Heading2'] else normal
    styles[name].textColor=colors.black
styles['BodyText'].fontSize=11
styles['BodyText'].leading=14
styles['Heading1'].fontSize=13
styles['Heading1'].leading=16
styles.add(ParagraphStyle(name='Portada',fontName=normal,fontSize=12,leading=17,alignment=1,textColor=colors.black))
pdf=[]
word=Document()
for name in ['Normal','Title','Heading 1','Heading 2']:
    word.styles[name].font.name='Times New Roman'
    from docx.shared import Pt, RGBColor
    word.styles[name].font.size=Pt(12 if name!='Heading 1' else 13)
    word.styles[name].font.color.rgb=RGBColor(0,0,0)

def par(text):
    pdf.append(Paragraph(escape(text),styles['BodyText']))
    pdf.append(Spacer(1,9))
    word.add_paragraph(text)

def heading(text):
    pdf.append(Paragraph(escape(text),styles['Heading1']))
    pdf.append(Spacer(1,10))
    word.add_heading(text,1)

def page():
    pdf.append(PageBreak())
    word.add_page_break()

def table(headers,rows,widths):
    cells=[[Paragraph(escape(str(x)),styles['BodyText']) for x in row] for row in [headers]+rows]
    t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#f1f1f1')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#b2bdca')),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#d5dce6')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    pdf.append(t)
    w=word.add_table(rows=1,cols=len(headers));w.style='Table Grid'
    for cell,text in zip(w.rows[0].cells,headers):cell.text=text
    for row in rows:
        for cell,text in zip(w.add_row().cells,row):cell.text=str(text)

# Los logos se dibujan fuera del flujo del texto: no reservan una fila.
# El PDF los posiciona con el canvas y Word usa imágenes flotantes sin ajuste.
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Emu

seccion = word.sections[0]
seccion.page_width = Pt(A4[0])
seccion.page_height = Pt(A4[1])
seccion.left_margin = Pt(44)
seccion.right_margin = Pt(44)
seccion.top_margin = Pt(40)
seccion.bottom_margin = Pt(40)

def agregarLogoFlotante(parrafo, nombre, x, y, descripcion):
    dibujo = parrafo.add_run().add_picture(str(DOCS/'identidad'/nombre), width=Pt(62))
    anchor = dibujo._inline
    anchor.tag = qn('wp:anchor')
    for clave,valor in [('distT','0'),('distB','0'),('distL','0'),('distR','0'),
                        ('simplePos','0'),('relativeHeight','0'),('behindDoc','1'),
                        ('locked','0'),('layoutInCell','0'),('allowOverlap','1')]:
        anchor.set(clave,valor)
    simple = OxmlElement('wp:simplePos')
    simple.set('x','0'); simple.set('y','0')
    anchor.insert(0,simple)
    for indice,tipo,valor in [(1,'H',x),(2,'V',y)]:
        posicion = OxmlElement('wp:position'+tipo)
        posicion.set('relativeFrom','page')
        offset = OxmlElement('wp:posOffset')
        offset.text = str(int(Pt(valor)))
        posicion.append(offset)
        anchor.insert(indice,posicion)
    sinAjuste = OxmlElement('wp:wrapNone')
    posicionDocPr = list(anchor).index(anchor.find(qn('wp:docPr')))
    anchor.insert(posicionDocPr,sinAjuste)
    anchor.find(qn('wp:docPr')).set('descr',descripcion)

cover=[
'UNIVERSIDAD TECNOLÓGICA DE PANAMÁ',
'FACULTAD DE INGENIERÍA DE SISTEMAS COMPUTACIONALES',
'LICENCIATURA EN INGENIERÍA DE SOFTWARE',
'',
'INGENIERÍA WEB',
'',
'PROYECTO SEMESTRAL',
'TutoríaLink',
'Fase 3: implementación frontend y diseño responsive',
'',
'Grupo de proyecto: 8',
'Grupo académico: 1SF-133',
'',
'Integrantes:',
'Whorlyn Bustos — 8-1022-657',
'Emmanuel Hernández — 8-1028-609',
'Jeremy Martínez — 8-1024-1470',
'Jorshua Jiménez — 8-1026-2297',
'',
'Profesora: Dra. Elba Valderrama Bahamóndez',
'',
'II semestre de 2026',
'Noviembre de 2026',
'',
'Repositorio:',
'https://github.com/Jorshuask/TutoriaLink'
]
for indice,text in enumerate(cover):
    if text:
        pdf.append(Paragraph(escape(text),styles['Portada']))
    else:
        pdf.append(Spacer(1,14))
    w = word.add_paragraph(text)
    w.alignment = WD_ALIGN_PARAGRAPH.CENTER
    w.paragraph_format.space_before = Pt(0)
    w.paragraph_format.space_after = Pt(0)
    w.paragraph_format.line_spacing = Pt(17)
    if indice == 0:
        agregarLogoFlotante(w,'logo-utp.png',44,40,'Logo de la UTP')
        agregarLogoFlotante(w,'logo-fisc.png',A4[0]-44-62,40,'Logo de la Facultad de Ingeniería de Sistemas Computacionales')
page()
heading('1. Objetivo e implementación')
par('Convertir la propuesta de TutoríaLink de la Fase 2 en una primera implementación frontend que permita recorrer las funciones principales de estudiantes, tutores y administrador. Se utiliza HTML, CSS y JavaScript sin frameworks, servicios externos ni compilación. La implementación se organiza en 17 archivos HTML y scripts de pantalla con funciones tradicionales, condicionales y bucles for.')
par('La aplicación se abre mediante index.html servido desde localhost, Live Server o GitHub Pages. Se incluye iniciar.bat para servir los archivos con Python. No se recomienda abrir los HTML con doble clic, porque el almacenamiento de file:// puede variar entre navegadores. El usuario puede entrar con estudiante, tutor o admin y cualquier contraseña no vacía. El registro valida nombre, correo y confirmación de contraseña y crea una cuenta local; no almacena contraseñas ni habilita autenticación individual. El acceso continúa usando los tres usuarios de prueba solicitados.')
heading('2. Funciones disponibles')
table(['Área','Implementación'],[
['Cuenta','Registro local, inicio y cierre de sesión, edición de perfil. La sesión se conserva al recargar la pestaña.'],
['Estudiante','Búsqueda por materia, día y hora; perfil del tutor; solicitud; consulta de estado; cancelación; calendario como listado; historial.'],
['Tutor','Solicitudes recibidas de Ana Rodríguez, aceptación/rechazo, días y horas disponibles, selección de materias, calendario y seguimiento tras terminar la sesión.'],
['Administrador','Listado y activación/desactivación de usuarios, alta y cambio de estado de materias, registros de cambios.'],
['Persistencia','Datos en localStorage del navegador y rol en sessionStorage. Sin PHP, MySQL ni sincronización entre usuarios.']
],[105,402])
heading('3. Cambios de interfaz')
par('Se conserva la identidad azul del prototipo y se utiliza el logo proporcionado por el equipo. Los enlaces del encabezado están alineados a la derecha, sin subrayado inferior. Se retiraron la barra de demostración, el pie de página y el bloque de accesos duplicados del panel.')
par('Mi perfil y materias usa campos de nombre y correo en una fila, presentación debajo y una lista de materias separada por una línea. Mi disponibilidad presenta días y horas en dos columnas. Se eliminaron los recuadros anidados y se redujeron bordes redondeados y negritas. En móvil los formularios pasan a una columna.')
page()
heading('4. Correspondencia con las fases anteriores')
table(['Referencia','Estado de esta implementación'],[
['RF-01 a RF-03: cuentas y roles','Interfaces implementadas. Acceso por rol simulado; la autenticación segura llega con el backend en la Fase 4.'],
['RF-04 a RF-06: tutores y solicitudes','Búsqueda, perfil, selección de materias, disponibilidad y formulario de solicitud implementados.'],
['RF-07 a RF-10: gestión y calendario','Aceptación, rechazo, estado, cancelación y listado de sesiones aceptadas. La reprogramación queda para la Fase 4.'],
['RF-11 y RF-12: seguimiento','Resumen y recomendaciones tras finalizar la sesión e historial. La valoración queda para la Fase 4.'],
['RF-13 a RF-15: gestión y validaciones','Alta/estado de materias, estado de usuarios, validación de campos y horarios ocupados, confirmaciones y mensajes. La edición completa de usuarios y materias queda para la Fase 4.'],
['Sitemap de Fase 2','Se implementan las pantallas principales. Portada pública/Cómo funciona, recuperación, notificaciones, contacto y vistas de detalle independientes se completan en la Fase 4; por ahora los detalles se muestran en tarjetas.']
],[153,354])
heading('5. Responsive y accesibilidad')
par('Se utilizan encabezados jerárquicos, etiquetas y obligatoriedad visibles, controles nativos, estados expresados con texto, confirmaciones role=status y errores role=alert asociados a sus campos con aria-invalid y aria-describedby. Hay enlace para saltar al contenido y foco visible. Los botones repetidos nombran la tutoría o usuario sobre el que actúan. Tras actualizar listas se recupera un punto útil de foco. El menú móvil comunica su estado y se cierra con Escape devolviendo el foco al botón.')
par('Se comprobaron anchos de 390, 768 y 1366 px y reflow a 320 px con espaciado de texto aumentado en formularios. Se comprobó el modo de colores forzados. La aplicación no usa audio ni video y comunica toda la información mediante texto; las personas sordas no necesitan escuchar ninguna señal para completar las tareas. Estas medidas preparan el contenido para tecnologías de apoyo sin exigir una extensión especial.')
par('axe-core 4.10.3 revisó 24 combinaciones de rol y pantalla de los 17 HTML y no detectó violaciones automáticas. Se probaron con teclado el salto al contenido, acceso, error de campo y menú móvil; se revisó el árbol accesible. En seis evaluaciones hay nodos de contraste cuyo resultado automático no es concluyente y deben revisarse manualmente. Faltan pruebas reales con NVDA/VoiceOver, zoom real y usuarios; no se certifica conformidad WCAG completa. Resultados: docs/Resultado_accesibilidad.json y docs/Accesibilidad y GitHub Pages.md.')
heading('6. Validaciones y evidencias')
par('Las pruebas automatizadas se ejecutaron en Microsoft Edge con Playwright y un servidor local temporal: inicio por los tres roles, cierre y persistencia de sesión, registro con contraseñas coincidentes, ausencia de contraseñas guardadas, búsqueda, solicitud, aceptación, calendario y alta de materia. Se verificaron días y materias persistentes y su aplicación en búsqueda y solicitudes. No se observaron errores JavaScript en estos recorridos. node --check valida la sintaxis del JavaScript.')
par('Las capturas corresponden a perfiles de navegador temporales usados en las pruebas; por eso pueden mostrar materias o selecciones añadidas durante la verificación. El detalle está en docs/VERIFICACION.txt y el script verificable en verificar.py.')
page()
heading('Revisión de la rúbrica de evaluación')
par('La rúbrica de Fase 3 suma 100 puntos y la fase vale 8 %. La tabla resume la evidencia de cada criterio.')
table(['Criterio','Puntos','Evidencia'],[['Implementación de las interfaces principales','15','17 páginas HTML: acceso, registro, paneles de estudiante, tutor y administrador, búsqueda de tutores, solicitudes, calendario, historial, perfil, disponibilidad, usuarios, materias y ayuda.'],['Estructura y calidad del HTML/CSS','15','HTML semántico por pantalla, formularios en HTML y una hoja de estilos compartida. Enlaces y sintaxis de JavaScript verificados.'],['Navegación funcional','15','Enlaces entre páginas reales, menú según el rol, navegación con teclado, salto al contenido y menú móvil.'],['Formularios y componentes de interfaz','10','Registro, acceso de prueba, filtros, solicitud, perfil, disponibilidad, materias y seguimiento, con validaciones y mensajes. Aún sin base de datos, como permite la guía.'],['Diseño responsive','15','Probado en 390, 768 y 1366 px y en formularios a 320 px, sin desplazamiento horizontal.'],['Correspondencia con prototipo, sitemap y navegación','10','Se mantienen la identidad, los roles y los flujos principales del prototipo de la Fase 2. Portada pública, recuperación de contraseña, notificaciones y contacto quedan para la Fase 4, junto al backend.'],['Proceso de implementación evidenciado mediante Git','10','Código en el repositorio del equipo: https://github.com/Jorshuask/TutoriaLink'],['Aplicación de reglas de accesibilidad','10','axe-core 4.10.3: 24 evaluaciones en 17 páginas sin violaciones. Etiquetas, errores asociados a campos, foco visible, teclado y colores forzados.']],[145,48,314])

for filename,caption in [('login.png','7.1. Inicio de sesión'),('escritorio.png','7.2. Búsqueda de tutores en escritorio'),('perfil.png','7.3. Perfil y materias del tutor'),('disponibilidad.png','7.4. Disponibilidad del tutor')]:
    path=DOCS/'capturas'/filename
    if path.exists():
        page();heading(caption)
        img=Image(str(path));scale=min(507/img.imageWidth,610/img.imageHeight)
        img.drawWidth=img.imageWidth*scale;img.drawHeight=img.imageHeight*scale
        pdf.append(img);word.add_picture(str(path),width=Inches(6))
page();heading('7.5. Formularios en móvil')
for filename in ['perfil-movil.png','disponibilidad-movil.png']:
    path=DOCS/'capturas'/filename
    if path.exists():
        img=Image(str(path));scale=min(230/img.imageWidth,600/img.imageHeight)
        img.drawWidth=img.imageWidth*scale;img.drawHeight=img.imageHeight*scale
        if filename=='perfil-movil.png':first=img
        else:second=img
        word.add_picture(str(path),width=Inches(2.6))
if 'first' in locals() and 'second' in locals():pdf.append(Table([[first,second]],colWidths=[253,254],style=TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')])))
page();heading('8. Organización del código y Git')
par('Cada pantalla tiene su propio HTML: index, registro, los tres paneles, buscar, perfil-tutor, solicitar, solicitudes, calendario, historial, mi-perfil, disponibilidad, usuarios, materias, registros y ayuda. src/estilos.css define la presentación; src/js contiene datos.js, utilidades.js, sesion.js y los scripts de pantalla; src/assets contiene el logo. Se usan enlaces href entre archivos reales, no rutas con # ni una función que genere todas las vistas. docs reúne el informe, el enunciado, referencias y capturas. README.md explica cómo ejecutar el proyecto y SUBIR_A_GITHUB.md describe cómo subirlo.')
par('El código está en el repositorio del equipo (https://github.com/Jorshuask/TutoriaLink) y se publica con GitHub Pages en https://jorshuask.github.io/TutoriaLink/ .')
heading('Por qué funciona el inicio de sesión entre páginas')
par('sesion.js lee el rol de sessionStorage en cada página del mismo origen y pestaña y redirige a quien no haya entrado. login.js guarda ese rol y abre el HTML del panel. El frontend no comprueba contraseñas reales ni sustituye los permisos del servidor. En Fase 4 se podrá usar una sesión PHP sin necesidad de convertir la web en una aplicación de una sola página. El archivo docs/Como entender el codigo.md explica el recorrido para principiantes.')
heading('9. Alcance y publicación')
par('Esta fase implementa las interfaces principales y la simulación local de sus flujos. No sustituye la Fase 4: faltan autenticación de servidor, autorización real, base de datos y sincronización. Tampoco se presentan como completas todas las pantallas del sitemap de la Fase 2; lo que queda para la Fase 4 se detalla en la sección 4.')

par('Repositorio: https://github.com/Jorshuask/TutoriaLink . Versión publicada: https://jorshuask.github.io/TutoriaLink/ (GitHub Pages, rama main, carpeta raíz).')
heading('Fuentes técnicas consultadas')
par('W3C WAI, notificaciones en formularios: https://www.w3.org/WAI/tutorials/forms/notifications/ . WCAG 2.2: https://www.w3.org/TR/WCAG22/ . Deque axe-core: https://github.com/dequelabs/axe-core . GitHub Pages, fuente de publicación: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site .')
par('Logos de la UTP y de la Facultad de Ingeniería de Sistemas Computacionales: https://utp.ac.pa/logos-para-medios-digitales . Cédulas verificadas en la portada de la Fase 2 del grupo 8.')
heading('10. Fuentes del proyecto')
par('Enunciado de Fase 3 (una página); guía del proyecto y Fase 1 de la profesora, especialmente página 4; guía de Fase 2 de la profesora; Fase1_Grupo8_TutoriaLink.pdf; Fase2_Grupo8_TutoriaLink_Arquitectura_y_Diseno.pdf; README y prototipo HTML/CSS del proyecto original. Se incluyen los documentos de referencia en docs/referencias.')
page();heading('Anexo. Uso de inteligencia artificial')
par('Siguiendo las indicaciones del curso, el Grupo 8 deja constancia de que en esta fase utilizó Codex (asistente de programación de OpenAI) como herramienta de apoyo. La IA se usó para generar y ajustar partes del código HTML, CSS y JavaScript, ejecutar pruebas automáticas de navegación, responsive y accesibilidad, y redactar un primer borrador de este informe. El diseño, los requisitos y el prototipo provienen de las Fases 1 y 2 del equipo. El equipo revisó el resultado, decidió los cambios y es responsable de explicar el funcionamiento del código.')
table(['Parte del trabajo','Herramienta','Uso de la IA','Trabajo del equipo'],[
['Frontend (HTML, CSS, JS)','Codex','Generación y ajuste de páginas, estilos y scripts a partir del prototipo.','Definir pantallas y flujos, revisar el comportamiento y el diseño.'],
['Pruebas y accesibilidad','Codex','Pruebas automáticas con Playwright y axe-core; capturas.','Revisar resultados y probar la navegación manualmente.'],
['Informe','Codex','Primer borrador del texto y armado del PDF.','Revisar, corregir y validar el contenido.']
],[100,72,170,165])
heading('Principales instrucciones dadas a la IA')
for text in ['Implementar de forma sencilla el frontend de TutoríaLink según el enunciado de la Fase 3 y el prototipo de la Fase 2.','Ajustar el diseño visual para que sea más limpio y coherente con el prototipo del equipo.','Separar cada pantalla en su propio HTML y simplificar el JavaScript para que sea fácil de explicar.','Revisar la accesibilidad (HTML semántico, teclado, contraste y lectores de pantalla) y el diseño responsive.','Preparar el informe de la fase y los archivos para subirlos al repositorio.']:
    par('• '+text)

def dibujarLogosPortada(canvas,doc):
    from reportlab.lib.utils import ImageReader
    from PIL import Image as ImagenPIL
    # Alineados con las primeras tres líneas; no modifican su posición.
    for nombre,x in [('logo-utp.png',44),('logo-fisc.png',A4[0]-44-62)]:
        ruta = DOCS/'identidad'/nombre
        with ImagenPIL.open(ruta) as imagen:
            ancho,alto = imagen.size
        escala = min(62/ancho,62/alto)
        anchoFinal = ancho*escala
        altoFinal = alto*escala
        canvas.drawImage(ImageReader(str(ruta)),x,A4[1]-46-altoFinal,
                         width=anchoFinal,height=altoFinal,mask='auto')

# Generar primero en una carpeta temporal. Si el usuario tiene abierto el PDF,
# conservarlo y guardar la nueva versión con otro nombre, sin cerrar su lector.
import shutil
import tempfile

def copiarDocumento(origen, destino):
    try:
        shutil.copy2(origen, destino)
        return destino
    except OSError:
        alternativo = destino.with_name(destino.stem + "_actualizado" + destino.suffix)
        shutil.copy2(origen, alternativo)
        print("El archivo habitual no se pudo reemplazar. Nueva versión:", alternativo)
        return alternativo

with tempfile.TemporaryDirectory() as temporal:
    pdfTemporal = Path(temporal) / 'informe.pdf'
    wordTemporal = Path(temporal) / 'informe.docx'
    SimpleDocTemplate(str(pdfTemporal),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=40,bottomMargin=40,title='TutoríaLink — Fase 3',author='Grupo 8').build(pdf,onFirstPage=dibujarLogosPortada)
    word.save(wordTemporal)
    copiarDocumento(pdfTemporal, DOCS/'Informe_Fase3_TutoriaLink.pdf')
    copiarDocumento(wordTemporal, DOCS/'Informe_Fase3_TutoriaLink.docx')
    copiarDocumento(pdfTemporal, BASE/'Resolucion sencilla.pdf')
    copiarDocumento(wordTemporal, BASE/'Resolucion sencilla.docx')
print('Informe PDF y Word actualizados.')
