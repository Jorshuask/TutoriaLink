"""Prueba el frontend multipágina en Edge con un servidor local temporal."""
from pathlib import Path
from datetime import date, timedelta
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from html.parser import HTMLParser
from urllib.parse import urlsplit
import subprocess
from playwright.sync_api import sync_playwright

base = Path(__file__).parent.resolve()
(base / 'docs/capturas').mkdir(exist_ok=True)

class RevisarEnlaces(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for nombre, valor in attrs:
            if nombre in ['href', 'src'] and valor:
                ruta = urlsplit(valor).path
                if ruta and not urlsplit(valor).scheme:
                    assert (base / ruta).exists(), 'Enlace inexistente: ' + valor

for archivo in base.glob('*.html'):
    RevisarEnlaces().feed(archivo.read_text(encoding='utf-8'))
for archivo in (base / 'src/js').glob('*.js'):
    subprocess.run(['node', '--check', str(archivo)], check=True, capture_output=True)
    assert '=>' not in archivo.read_text(encoding='utf-8')

class ServidorSilencioso(SimpleHTTPRequestHandler):
    def log_message(self, formato, *args):
        pass

servidor = ThreadingHTTPServer(('127.0.0.1', 0), partial(ServidorSilencioso, directory=str(base)))
Thread(target=servidor.serve_forever, daemon=True).start()
url = 'http://127.0.0.1:' + str(servidor.server_port) + '/'
try:
    with sync_playwright() as p:
        navegador = p.chromium.launch(channel='msedge', headless=True)
        page = navegador.new_page(viewport={'width': 1366, 'height': 900})
        errores = []
        page.on('pageerror', lambda error: errores.append(str(error)))
        page.on('dialog', lambda dialogo: dialogo.accept())

        def entrar(usuario):
            page.locator('#usuario').fill(usuario)
            page.locator('#clave').fill('cualquier contraseña')
            page.get_by_role('button', name='Iniciar sesión', exact=True).click()
            page.wait_for_url('**/panel-' + usuario + '.html')

        def cambiar(usuario):
            page.get_by_role('link', name='Cerrar sesión', exact=True).click()
            page.wait_for_url('**/index.html')
            entrar(usuario)

        def ir(archivo):
            page.goto(url + archivo)

        def captura(nombre):
            page.screenshot(path=str(base / 'docs/capturas' / nombre), full_page=True)

        def ancho(valor):
            page.set_viewport_size({'width': valor, 'height': 900})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')

        # Entrar a una página protegida sin sesión debe volver al inicio.
        ir('disponibilidad.html')
        page.wait_for_url('**/index.html')
        assert page.get_by_role('heading', name='Iniciar sesión').count() == 1
        captura('login.png')
        page.locator('#usuario').fill('desconocido')
        page.locator('#clave').fill('123')
        page.get_by_role('button', name='Iniciar sesión', exact=True).click()
        assert 'Escribe estudiante' in page.locator('#error').inner_text()

        page.get_by_role('link', name='Crear cuenta', exact=True).click()
        page.wait_for_url('**/registro.html')
        page.locator('#nombreRegistro').fill('Estudiante de prueba')
        page.locator('#correoRegistro').fill('prueba@example.test')
        page.locator('#claveRegistro').fill('123')
        page.locator('#confirmarRegistro').fill('456')
        page.get_by_role('button', name='Crear cuenta', exact=True).click()
        assert 'deben coincidir' in page.locator('#error').inner_text()
        page.locator('#confirmarRegistro').fill('123')
        page.get_by_role('button', name='Crear cuenta', exact=True).click()
        page.wait_for_url('**/index.html')
        assert page.evaluate("JSON.parse(localStorage.getItem('tutorialink-fase3')).usuarios.length") == 3
        assert 'clave' not in page.evaluate("localStorage.getItem('tutorialink-fase3')")

        entrar('estudiante')
        assert page.get_by_role('heading', name='Panel del estudiante').count() == 1
        assert page.locator('footer, .barra').count() == 0
        page.get_by_role('link', name='Buscar tutores', exact=True).click()
        page.wait_for_url('**/buscar.html')
        assert page.locator('#resultados article').count() == 3
        captura('escritorio.png')
        page.locator('#materia').select_option('Programación')
        page.locator('#filtros button').click()
        assert page.locator('#resultados article').count() == 1
        page.locator('#materia').select_option('')
        page.locator('#filtros button').click()
        page.get_by_role('link', name='Ver perfil', exact=False).first.click()
        page.wait_for_url('**/perfil-tutor.html?tutor=1')
        assert page.locator('#nombreTutor').inner_text() == 'Ana Rodríguez'
        page.get_by_role('link', name='Solicitar tutoría', exact=True).click()
        page.wait_for_url('**/solicitar.html?tutor=1')
        fecha = date.today() + timedelta(days=1)
        while fecha.weekday() > 4:
            fecha += timedelta(days=1)
        page.locator('#fecha').fill(fecha.isoformat())
        page.locator('#motivo').fill('Necesito repasar límites y sus propiedades.')
        page.get_by_role('button', name='Enviar solicitud', exact=True).click()
        page.wait_for_url('**/solicitudes.html')
        assert page.locator('.estado').inner_text() == 'Pendiente'
        page.reload()
        assert page.locator('.estado').inner_text() == 'Pendiente'
        # El mismo horario no se puede solicitar de nuevo.
        ir('solicitar.html?tutor=1')
        page.locator('#fecha').fill(fecha.isoformat())
        page.locator('#motivo').fill('Necesito repasar límites de nuevo.')
        page.get_by_role('button', name='Enviar solicitud', exact=True).click()
        assert 'ya no está disponible' in page.locator('#error').inner_text()
        cambiar('tutor')
        page.get_by_role('link', name='Solicitudes', exact=True).click()
        page.get_by_role('button', name='Aceptar', exact=False).click()
        assert page.locator('.estado').inner_text() == 'Aceptada'
        page.locator('.seguimiento textarea').fill('Repasamos límites y dejamos ejercicios para practicar.')
        page.get_by_role('button', name='Guardar seguimiento y finalizar', exact=False).click()
        assert 'cuando termine' in page.locator('#error').inner_text()
        page.get_by_role('link', name='Calendario', exact=True).click()
        assert page.locator('#listaSolicitudes article').count() == 1

        cambiar('admin')
        page.get_by_role('link', name='Materias', exact=True).click()
        page.locator('#nueva').fill('Estadística')
        page.get_by_role('button', name='Agregar materia', exact=True).click()
        assert page.get_by_role('heading', name='Estadística', exact=True).count() == 1
        page.get_by_role('link', name='Usuarios', exact=True).click()
        page.get_by_role('button', name='Desactivar', exact=False).first.click()
        assert 'Inactivo' in page.locator('#listaUsuarios').inner_text()
        page.get_by_role('link', name='Registros', exact=True).click()
        assert page.locator('#listaRegistros p').count() > 0
        cambiar('estudiante')
        ir('materias.html')
        page.wait_for_url('**/panel-estudiante.html')
        ir('buscar.html')
        for valor in [390, 768, 1366]:
            ancho(valor)
            if valor == 390:
                page.get_by_role('button', name='Menú', exact=True).click()
                assert page.locator('#menu').get_attribute('aria-expanded') == 'true'
                captura('movil.png')

        cambiar('tutor')
        page.get_by_role('link', name='Disponibilidad', exact=True).click()
        ancho(1366)
        for casilla in page.locator('input[name="dia"]').all():
            casilla.uncheck()
        page.get_by_role('button', name='Guardar horarios', exact=True).click()
        assert 'al menos un día' in page.locator('#error').inner_text()
        page.locator('input[name="dia"][value="6"]').check()
        page.get_by_role('button', name='Guardar horarios', exact=True).click()
        page.reload()
        assert page.locator('input[name="dia"][value="6"]').is_checked()
        captura('disponibilidad.png')
        ancho(390)
        captura('disponibilidad-movil.png')
        ancho(1366)
        cambiar('estudiante')
        page.get_by_role('link', name='Buscar tutores', exact=True).click()
        page.locator('#dia').select_option('1')
        page.locator('#filtros button').click()
        assert 'Ana Rodríguez' not in page.locator('#resultados').inner_text()
        page.locator('#dia').select_option('6')
        page.locator('#filtros button').click()
        assert page.locator('#resultados article').count() == 1
        page.get_by_role('link', name='Solicitar', exact=False).click()
        assert 'Sábado' in page.locator('#diasAyuda').inner_text()
        page.locator('#fecha').fill(fecha.isoformat())
        page.locator('#motivo').fill('Repaso de límites para el examen.')
        page.get_by_role('button', name='Enviar solicitud', exact=True).click()
        assert 'día disponible' in page.locator('#error').inner_text()

        cambiar('tutor')
        page.get_by_role('link', name='Mi perfil y materias', exact=True).click()
        page.wait_for_url('**/mi-perfil.html')
        captura('perfil.png')
        for valor in [390, 768, 1366]:
            ancho(valor)
            if valor == 390:
                captura('perfil-movil.png')
        for casilla in page.locator('input[name="materiaTutor"]').all():
            casilla.uncheck()
        page.get_by_role('button', name='Guardar cambios', exact=True).click()
        assert 'al menos una materia' in page.locator('#error').inner_text()
        page.locator('input[name="materiaTutor"][value="Estadística"]').check()
        page.get_by_role('button', name='Guardar cambios', exact=True).click()
        page.reload()
        assert page.locator('input[name="materiaTutor"][value="Estadística"]').is_checked()
        cambiar('estudiante')
        page.get_by_role('link', name='Buscar tutores', exact=True).click()
        page.locator('#materia').select_option('Estadística')
        page.locator('#filtros button').click()
        assert page.locator('#resultados article').count() == 1
        page.get_by_role('link', name='Solicitar', exact=False).click()
        assert page.locator('#asignatura').input_value() == 'Estadística'
        page.get_by_role('link', name='Cerrar sesión', exact=True).click()
        page.wait_for_url('**/index.html')
        ir('mi-perfil.html')
        page.wait_for_url('**/index.html')
        assert page.locator('#clave').input_value() == ''
        assert not errores, errores
        navegador.close()
finally:
    servidor.shutdown()
    servidor.server_close()
print('OK: 17 páginas, enlaces locales y sintaxis JS. Registro, sesión entre páginas, tres roles, filtros, solicitudes y conflicto de horario, aceptación, calendario, perfil, días, materias, administración y responsive. Sin errores JavaScript.')
