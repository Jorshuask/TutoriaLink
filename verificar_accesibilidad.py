"""Auditoría axe, teclado y rutas bajo /TutoriaLink/ como en GitHub Pages.
La auditoría automática no sustituye probar con usuarios y lectores de pantalla.
"""
from pathlib import Path
from datetime import date, timedelta
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from functools import partial
import json, re, tempfile, urllib.request, tarfile, io, hashlib, base64
from playwright.sync_api import sync_playwright

base = Path(__file__).parent.resolve()
version = '4.10.3'
cache = Path(tempfile.gettempdir()) / ('tutorialink-axe-core-' + version + '.min.js')
if not cache.exists():
    with urllib.request.urlopen('https://registry.npmjs.org/axe-core/' + version, timeout=30) as r:
        meta = json.load(r)
    with urllib.request.urlopen(meta['dist']['tarball'], timeout=30) as r:
        paquete = r.read()
    assert 'sha512-' + base64.b64encode(hashlib.sha512(paquete).digest()).decode() == meta['dist']['integrity']
    with tarfile.open(fileobj=io.BytesIO(paquete), mode='r:gz') as tar:
        cache.write_bytes(tar.extractfile('package/axe.min.js').read())

class ServidorPages(SimpleHTTPRequestHandler):
    def do_GET(self):
        if not self.path.startswith('/TutoriaLink/'):
            self.send_error(404)
            return
        self.path = self.path[len('/TutoriaLink'):]
        super().do_GET()

    def log_message(self, formato, *args):
        pass

servidor = ThreadingHTTPServer(('127.0.0.1', 0), partial(ServidorPages, directory=str(base)))
Thread(target=servidor.serve_forever, daemon=True).start()
url = 'http://127.0.0.1:' + str(servidor.server_port) + '/TutoriaLink/'
ayer = (date.today() - timedelta(days=1)).isoformat()
manana = (date.today() + timedelta(days=1)).isoformat()
semilla = [
    {'id': 101, 'tutor': 1, 'materia': 'Cálculo I', 'fecha': manana, 'hora': '14:00', 'modalidad': 'Virtual', 'motivo': 'Repasar límites.', 'estado': 'Pendiente'},
    {'id': 102, 'tutor': 1, 'materia': 'Física I', 'fecha': manana, 'hora': '15:00', 'modalidad': 'Presencial', 'motivo': 'Repasar movimiento.', 'estado': 'Aceptada'},
    {'id': 103, 'tutor': 1, 'materia': 'Cálculo II', 'fecha': ayer, 'hora': '14:00', 'modalidad': 'Virtual', 'motivo': 'Repasar integrales.', 'estado': 'Aceptada'},
    {'id': 104, 'tutor': 1, 'materia': 'Cálculo I', 'fecha': ayer, 'hora': '15:00', 'modalidad': 'Virtual', 'motivo': 'Repasar límites.', 'estado': 'Realizada', 'resumen': 'Se practicaron límites con ejercicios.'},
    {'id': 105, 'tutor': 1, 'materia': 'Física I', 'fecha': ayer, 'hora': '16:00', 'modalidad': 'Virtual', 'motivo': 'Repasar movimiento.', 'estado': 'Rechazada'}
]
resultados = []
fallos = []

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        for rol in ['publico', 'estudiante', 'tutor', 'admin']:
            context = browser.new_context(viewport={'width': 1366, 'height': 900})
            page = context.new_page()
            page.goto(url + 'index.html')
            page.evaluate("localStorage.setItem('tutorialink-fase3', JSON.stringify(datos))")
            page.evaluate('(solicitudes) => { var d=JSON.parse(localStorage.getItem("tutorialink-fase3")); d.solicitudes=solicitudes; localStorage.setItem("tutorialink-fase3",JSON.stringify(d)); }', semilla)
            if rol != 'publico':
                page.evaluate('(rol) => sessionStorage.setItem("tutorialink-sesion",rol)', rol)
            for archivo in sorted(base.glob('*.html')):
                texto = archivo.read_text(encoding='utf-8')
                roles = re.search('data-roles="([^"]+)"', texto).group(1).split()
                if rol not in roles:
                    continue
                destino = archivo.name
                if destino in ['perfil-tutor.html', 'solicitar.html']:
                    destino += '?tutor=1'
                response = page.goto(url + destino)
                assert response.status == 200
                assert page.url.startswith(url)
                assert page.locator('h1').count() == 1
                for campo in page.locator('input, select, textarea').all():
                    if campo.is_visible():
                        assert campo.get_attribute('id') or campo.locator('xpath=ancestor::label').count() > 0
                for enlace in page.locator('[href], [src]').all():
                    valor = enlace.get_attribute('href') or enlace.get_attribute('src')
                    assert not valor.startswith('/'), valor
                page.add_script_tag(path=str(cache))
                axe = page.evaluate("""async () => await axe.run(document, {
                    runOnly: {type:'tag', values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}
                })""")
                item = {'pagina': destino, 'rol': rol, 'violaciones': [], 'revisiones_manuales': []}
                for v in axe['violations']:
                    item['violaciones'].append({'id': v['id'], 'impacto': v['impact'], 'descripcion': v['help'], 'nodos': [n['target'] for n in v['nodes']]})
                for v in axe['incomplete']:
                    item['revisiones_manuales'].append({'id': v['id'], 'descripcion': v['help'], 'cantidad_nodos': len(v['nodes'])})
                resultados.append(item)
                if item['violaciones']:
                    fallos.append(item)
                print(rol + ': ' + destino + ' -> ' + str(len(item['violaciones'])) + ' hallazgos', flush=True)
            context.close()

        # Recorrido de acceso solo con teclado y salto al contenido.
        context = browser.new_context(viewport={'width': 1366, 'height': 900})
        page = context.new_page()
        page.goto(url + 'index.html')
        page.keyboard.press('Tab')
        assert page.locator(':focus').inner_text() == 'Saltar al contenido'
        page.keyboard.press('Enter')
        assert page.evaluate('document.activeElement.id') == 'contenido'
        page.keyboard.press('Tab')
        assert page.evaluate('document.activeElement.id') == 'usuario'
        page.keyboard.type('invalido')
        page.keyboard.press('Tab')
        page.keyboard.type('abc')
        page.keyboard.press('Tab')
        page.keyboard.press('Enter')
        assert page.locator('#usuario').get_attribute('aria-invalid') == 'true'
        assert page.evaluate('document.activeElement.id') == 'usuario'
        assert 'error' in page.locator('#usuario').get_attribute('aria-describedby')
        page.keyboard.press('Control+A')
        page.keyboard.type('estudiante')
        page.keyboard.press('Tab')
        page.keyboard.press('Tab')
        page.keyboard.press('Enter')
        page.wait_for_url('**/panel-estudiante.html')
        page.set_viewport_size({'width': 390, 'height': 844})
        page.goto(url + 'buscar.html')
        page.keyboard.press('Tab')
        page.keyboard.press('Tab')
        page.keyboard.press('Tab')
        assert page.evaluate('document.activeElement.id') == 'menu'
        page.keyboard.press('Enter')
        assert page.locator('#menu').get_attribute('aria-expanded') == 'true'
        page.keyboard.press('Tab')
        assert page.locator(':focus').get_attribute('href') == 'panel-estudiante.html'
        page.keyboard.press('Escape')
        assert page.evaluate('document.activeElement.id') == 'menu'
        assert page.locator('#menu').get_attribute('aria-expanded') == 'false'
        # Equivalente de disposición estrecha para revisar reflow y texto espaciado.
        for archivo in ['buscar.html', 'mi-perfil.html', 'solicitar.html?tutor=1']:
            page.goto(url + archivo)
            page.set_viewport_size({'width': 320, 'height': 900})
            page.add_style_tag(content='* { line-height: 1.5 !important; letter-spacing: .12em !important; word-spacing: .16em !important; } p { margin-bottom: 2em !important; }')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), archivo
        page.emulate_media(forced_colors='active')
        assert page.evaluate('matchMedia("(forced-colors: active)").matches')
        snapshot = page.locator('main').aria_snapshot()
        assert 'Solicitar tutoría' in snapshot and 'Motivo de la tutoría' in snapshot
        (base / 'docs/arbol-accesible-ejemplo.txt').write_text(snapshot, encoding='utf-8')
        context.close()
        browser.close()
finally:
    servidor.shutdown()
    servidor.server_close()

informe = {
    'fecha': str(date.today()), 'motor': 'axe-core ' + version, 'navegador': 'Microsoft Edge headless',
    'simulacion_pages': '/TutoriaLink/', 'evaluaciones': len(resultados),
    'paginas_distintas': len(set(x['pagina'].split('?')[0] for x in resultados)),
    'evaluaciones_con_violaciones': len(fallos), 'resultados': resultados,
    'limite': 'No certifica conformidad WCAG. Falta revisión con NVDA/VoiceOver, usuarios y ampliación real del navegador.'
}
(base / 'docs/Resultado_accesibilidad.json').write_text(json.dumps(informe, ensure_ascii=False, indent=2), encoding='utf-8')
assert not fallos, json.dumps(fallos, ensure_ascii=False)
print('OK: axe sin violaciones detectadas; teclado, mensajes de error y rutas de GitHub Pages comprobados.')
