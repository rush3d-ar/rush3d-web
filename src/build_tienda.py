"""Genera las páginas estáticas de la tienda (/tienda, /tienda/nafta, /tienda/arrepentimiento).
Uso: python3 src/build_tienda.py  (después de `npm run build` en src/)."""
import hashlib, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / 'assets'

def hashed(name, src):
    """Copia src a assets/<stem>-<hash>.<ext> (los /assets/* se cachean 1 año)."""
    h = hashlib.sha256(src.read_bytes()).hexdigest()[:8].upper()
    stem, ext = name.rsplit('.', 1)
    for old in A.glob(f'{stem}-*.{ext}'):
        old.unlink()
    out = A / f'{stem}-{h}.{ext}'
    shutil.copy(src, out)
    return f'/assets/{out.name}'

APP_CSS = '/assets/app.css?v=f67f3cc5'
TIENDA_CSS = hashed('tienda.css', ROOT / 'src' / 'tienda.css')
NAFTA_JS = hashed('nafta.js', ROOT / 'src' / 'dist' / 'nafta.js')
WA = 'https://wa.me/5491164131331'

def head(title, desc, path, og_img='/og-image.jpg', extra=''):
    return f'''<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://rush3d.ar{path}">
<meta name="theme-color" content="#0B0D10">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_AR">
<meta property="og:site_name" content="Rush 3D">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://rush3d.ar{path}">
<meta property="og:image" content="https://rush3d.ar{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{APP_CSS}">
<link rel="stylesheet" href="{TIENDA_CSS}">
{extra}
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XFLXBW8GWH"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-XFLXBW8GWH');</script>
<script>(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)}})(window,document,"clarity","script","yn0ithy1xb");</script>
<script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','379032344154547');fbq('track','PageView');</script>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "21ec021a967f48f7b74ebf53d17c0e7c"}}'></script>
</head>
<body class="t-page">
<a class="skip" href="#main">Saltar al contenido</a>
<header class="nav" data-nav>
  <div class="nav__in wrap">
    <a class="brand" href="/" aria-label="Rush, inicio">
      <img src="/images/logo-bolt.png" alt="" width="28" height="28">
      <span>RUSH</span>
    </a>
    <nav class="nav__links" aria-label="Secciones">
      <a href="/#que-hacemos">Qué hacemos</a>
      <a href="/#trabajos">Trabajos</a>
      <a href="/#proceso">Cómo trabajamos</a>
      <a href="/#materiales">Materiales</a>
      <a href="/tienda/" class="is-here" aria-current="page">Tienda</a>
    </nav>
    <a class="btn btn--red btn--sm nav__cta" href="/#contacto">Pedir presupuesto</a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Abrir menú" data-burger><span></span><span></span></button>
  </div>
</header>
<div class="menu" id="menu" hidden data-menu>
  <nav aria-label="Menú">
    <a href="/#que-hacemos"><i class="mono">01</i>Qué hacemos</a>
    <a href="/#trabajos"><i class="mono">02</i>Trabajos</a>
    <a href="/#proceso"><i class="mono">03</i>Cómo trabajamos</a>
    <a href="/#materiales"><i class="mono">04</i>Materiales</a>
    <a href="/tienda/"><i class="mono">05</i>Tienda</a>
    <a href="/#contacto"><i class="mono">06</i>Contacto</a>
  </nav>
  <a class="btn btn--red" href="{WA}?text=Hola%20Rush%2C%20quiero%20consultar%20por%20la%20tienda" target="_blank" rel="noopener">Escribir por WhatsApp</a>
</div>
'''

FOOT = f'''<footer class="foot">
  <div class="wrap">
    <div class="foot__top">
      <p class="foot__claim">¿Tenés una pieza en mente?<br><a href="/#contacto">Hablemos →</a></p>
      <nav class="foot__links" aria-label="Pie">
        <a href="/#que-hacemos">Qué hacemos</a><a href="/#trabajos">Trabajos</a><a href="/#materiales">Materiales</a><a href="/tienda/">Tienda</a>
        <a href="/tienda/arrepentimiento/">Botón de arrepentimiento</a><a href="https://instagram.com/rush3d.ar" target="_blank" rel="noopener">Instagram</a>
      </nav>
    </div>
    <p class="foot__word" aria-hidden="true">RUSH</p>
    <div class="foot__bot mono"><span>© 2026 Rush 3D</span><span>Hecho capa por capa en zona norte del GBA</span></div>
  </div>
</footer>
<script>
(function(){{
  var b=document.querySelector('[data-burger]'),m=document.querySelector('[data-menu]');
  if(b&&m)b.addEventListener('click',function(){{var o=b.getAttribute('aria-expanded')!=='true';b.setAttribute('aria-expanded',String(o));m.hidden=!o;document.body.style.overflow=o?'hidden':'';}});
  if(m)m.addEventListener('click',function(e){{if(e.target.closest('a')){{b.setAttribute('aria-expanded','false');m.hidden=true;document.body.style.overflow='';}}}});
}})();
</script>
'''

# ---------- /tienda/ ----------
catalog = head('Tienda · RUSH Originals', 'Diseños propios de Rush 3D, impresos en Buenos Aires y personalizables en color. Hacé tu pedido online y te contactamos para el pago.', '/tienda/') + '''
<main id="main" class="wrap">
  <nav class="t-crumbs mono" aria-label="Ubicación"><a href="/">Inicio</a><span>/</span><b>Tienda</b></nav>
  <section class="t-hero">
    <span class="t-eyebrow mono">RUSH Originals</span>
    <h1>Diseños nuestros, impresos a tu gusto</h1>
    <p>Piezas que diseñamos de cero en el taller. Elegís los colores, nos mandás el pedido y te escribimos por WhatsApp con el precio y las formas de pago.</p>
  </section>
  <section class="t-grid" aria-label="Productos">
    <a class="t-card" href="/tienda/nafta/">
      <div class="t-card__img"><img src="/images/nafta-card.webp" alt="Lámpara NAFTA con la luz prendida, pantalla roja y base de madera" width="800" height="800" loading="lazy"></div>
      <div class="t-card__body">
        <span class="t-card__num mono">RUSH Originals · 001</span>
        <h2>Lámpara NAFTA</h2>
        <p>Pantalla de doble curva con estrías. 25 colores de pantalla y 6 maderas de base.</p>
        <span class="t-card__cta">Personalizar <span aria-hidden="true">→</span></span>
      </div>
    </a>
  </section>
</main>
''' + FOOT + '</body>\n</html>\n'
(ROOT / 'tienda' / 'index.html').write_text(catalog)

# ---------- /tienda/nafta/ ----------
ld = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Product","name":"Lámpara NAFTA","brand":{"@type":"Brand","name":"Rush 3D"},"description":"Lámpara de mesa impresa en 3D: pantalla de doble curva con estrías en PLA Matte (25 colores) y base de PLA con fibra de madera (6 tonos). Diseño propio de Rush 3D.","image":"https://rush3d.ar/images/nafta-card.webp","url":"https://rush3d.ar/tienda/nafta/"}
</script>
<link rel="preload" href="/models/nafta.glb" as="fetch" crossorigin>'''
ficha = head('Lámpara NAFTA · RUSH Originals', 'Lámpara de mesa impresa en 3D con pantalla de doble curva. Elegí entre 25 colores y 6 maderas, mirá cómo queda con la luz prendida y hacé tu pedido.', '/tienda/nafta/', '/images/nafta-card.webp', ld) + f'''
<main id="main" class="wrap">
  <nav class="t-crumbs mono" aria-label="Ubicación"><a href="/">Inicio</a><span>/</span><a href="/tienda/">Tienda</a><span>/</span><b>NAFTA</b></nav>
  <div class="t-product">
    <section class="t-viewer" id="naftaViewer" aria-label="Vista 3D de la lámpara">
      <canvas id="naftaCanvas" aria-hidden="true"></canvas>
      <div class="t-loading mono" id="naftaLoading">Cargando modelo…</div>
      <div class="t-hud">
        <div class="t-hud__row">
          <span class="t-tag mono">RUSH Originals · <b>001</b></span>
          <span class="t-tag mono" id="hudState">Luz <b>apagada</b></span>
        </div>
        <div class="t-hud__row t-hud__row--bot">
          <div class="t-ctrl">
            <button class="t-pill mono" id="lightBtn" type="button" aria-pressed="false"><i aria-hidden="true"></i><span id="lightLbl">Prender luz</span></button>
            <div class="t-seg mono" role="group" aria-label="Tono de la luz">
              <button id="warmBtn" type="button" aria-pressed="true">Cálida 2700K</button>
              <button id="coldBtn" type="button" aria-pressed="false">Fría 6500K</button>
            </div>
          </div>
          <span class="t-hint mono">Arrastrá para girar</span>
        </div>
      </div>
    </section>

    <div class="t-info">
      <div class="t-title">
        <span class="t-eyebrow mono">RUSH Originals · diseño propio</span>
        <h1>Lámpara NAFTA</h1>
        <p>Pantalla de doble curva con estrías verticales, impresa en una sola pieza que enrosca sobre una base de PLA con fibra de madera. Con la luz prendida, las paredes finas dejan pasar el color y las estrías marcan franjas.</p>
      </div>
      <div class="t-specs">
        <div><span class="mono">Diámetro</span><strong>16 cm</strong></div>
        <div><span class="mono">Alto</span><strong>18,3 cm</strong></div>
        <div><span class="mono">Piezas</span><strong>2</strong></div>
      </div>

      <div class="t-opt">
        <div class="t-opt__head"><h2>Pantalla</h2><span class="mono">Bambu Lab PLA Matte · 25 colores</span></div>
        <p class="t-picked">Color: <b id="bodyName">Scarlet Red</b></p>
        <div class="t-swatches" id="bodySw" role="group" aria-label="Color de la pantalla"></div>
      </div>
      <div class="t-opt">
        <div class="t-opt__head"><h2>Base</h2><span class="mono">Bambu Lab PLA Wood · 6 tonos</span></div>
        <p class="t-picked">Tono: <b id="baseName">White Oak</b></p>
        <div class="t-swatches t-swatches--wood" id="baseSw" role="group" aria-label="Tono de la base"></div>
        <p class="t-note">Los colores en pantalla son aproximados; cada monitor los muestra distinto. Si dudás entre dos, te mandamos foto del rollo.</p>
      </div>

      <form class="t-form" id="orderForm" novalidate>
        <div class="t-opt__head"><h2>Tus datos</h2><span class="mono">Te contactamos para el pago</span></div>
        <div class="t-grid2">
          <div class="t-field"><label for="f-name">Nombre y apellido</label><input id="f-name" name="nombre" autocomplete="name" required><span class="t-err" id="e-name"></span></div>
          <div class="t-field"><label for="f-mail">Mail</label><input id="f-mail" name="email" type="email" autocomplete="email" required><span class="t-err" id="e-mail"></span></div>
        </div>
        <div class="t-field"><label for="f-wa">WhatsApp</label><input id="f-wa" name="whatsapp" type="tel" autocomplete="tel" inputmode="tel" placeholder="11 5555 5555" required><span class="t-err" id="e-wa"></span></div>
        <fieldset class="t-field">
          <legend>Entrega</legend>
          <div class="t-radios">
            <label class="t-radio"><input type="radio" name="entrega" id="f-envio" value="Envío" checked><span>Envío<small>A todo el país</small></span></label>
            <label class="t-radio"><input type="radio" name="entrega" id="f-retiro" value="Retiro"><span>Retiro<small>José León Suárez</small></span></label>
          </div>
        </fieldset>
        <div class="t-field" id="locWrap"><label for="f-loc">Localidad y código postal</label><input id="f-loc" name="localidad" autocomplete="postal-code" placeholder="Ej: San Isidro, 1642"><span class="t-err" id="e-loc"></span></div>
        <div class="t-field"><label for="f-msg">Comentario (opcional)</label><textarea id="f-msg" name="comentario" placeholder="Para qué ambiente es, si es un regalo, etc."></textarea></div>
        <div class="t-hp" aria-hidden="true"><label for="f-hp">No completar</label><input id="f-hp" name="_honey" tabindex="-1" autocomplete="off"></div>
        <button class="btn btn--red t-submit" id="orderBtn" type="submit"><span id="orderBtnLbl">Enviar pedido</span> <span class="arr" aria-hidden="true">→</span></button>
        <p class="t-formerr" id="formErr" role="alert"></p>
        <p class="t-fine">No cobramos nada acá. Recibimos tu pedido por mail y te escribimos por WhatsApp con el precio y las formas de pago. Si te arrepentís de una compra, usá el <a href="/tienda/arrepentimiento/">botón de arrepentimiento</a>.</p>
      </form>

      <div class="t-sent" id="sent" hidden role="status">
        <span class="t-sent__ok mono">Pedido recibido</span>
        <h2>Listo, ya tenemos tu pedido</h2>
        <p>Te mandamos una copia a <b id="sMail"></b>. En menos de 24 h te escribimos por WhatsApp con el precio y las formas de pago.</p>
        <dl>
          <dt>Pantalla</dt><dd id="sBody"></dd>
          <dt>Base</dt><dd id="sBase"></dd>
          <dt>Entrega</dt><dd id="sEntrega"></dd>
        </dl>
        <button class="t-linkbtn" id="backBtn" type="button">Hacer otro pedido</button>
      </div>
    </div>
  </div>
</main>
''' + FOOT + f'<script type="module" src="{NAFTA_JS}"></script>\n</body>\n</html>\n'
(ROOT / 'tienda' / 'nafta' / 'index.html').write_text(ficha)

# ---------- /tienda/arrepentimiento/ ----------
arr = head('Botón de arrepentimiento · Rush 3D', 'Pedí la revocación de una compra hecha en Rush 3D dentro de los 10 días corridos desde que la recibiste.', '/tienda/arrepentimiento/') + '''
<main id="main" class="wrap">
  <nav class="t-crumbs mono" aria-label="Ubicación"><a href="/">Inicio</a><span>/</span><a href="/tienda/">Tienda</a><span>/</span><b>Arrepentimiento</b></nav>
  <div class="t-legal">
    <h1>Botón de arrepentimiento</h1>
    <p>Si compraste en Rush 3D a distancia, podés revocar la compra dentro de los 10 días corridos desde que recibiste el producto, sin dar explicaciones. Completá el formulario y en menos de 24 h te respondemos con un código de trámite y los pasos para la devolución.</p>
    <form class="t-form" id="arrForm" novalidate>
      <div class="t-grid2">
        <div class="t-field"><label for="a-name">Nombre y apellido</label><input id="a-name" autocomplete="name" required><span class="t-err" id="ae-name"></span></div>
        <div class="t-field"><label for="a-mail">Mail</label><input id="a-mail" type="email" autocomplete="email" required><span class="t-err" id="ae-mail"></span></div>
      </div>
      <div class="t-grid2">
        <div class="t-field"><label for="a-wa">WhatsApp</label><input id="a-wa" type="tel" autocomplete="tel" inputmode="tel"><span class="t-err" id="ae-wa"></span></div>
        <div class="t-field"><label for="a-date">Fecha en que lo recibiste</label><input id="a-date" type="date"><span class="t-err" id="ae-date"></span></div>
      </div>
      <div class="t-field"><label for="a-prod">Qué compraste</label><input id="a-prod" placeholder="Ej: Lámpara NAFTA, pantalla Scarlet Red" required><span class="t-err" id="ae-prod"></span></div>
      <div class="t-field"><label for="a-msg">Comentario (opcional)</label><textarea id="a-msg"></textarea></div>
      <div class="t-hp" aria-hidden="true"><label for="a-hp">No completar</label><input id="a-hp" tabindex="-1" autocomplete="off"></div>
      <button class="btn btn--red t-submit" id="arrBtn" type="submit">Enviar solicitud</button>
      <p class="t-formerr" id="arrErr" role="alert"></p>
    </form>
    <div class="t-sent" id="arrSent" hidden role="status">
      <span class="t-sent__ok mono">Solicitud recibida</span>
      <h2>Recibimos tu solicitud</h2>
      <p>Te mandamos una copia por mail. En menos de 24 h te respondemos con el código de trámite.</p>
    </div>
  </div>
</main>
<script>
(function(){
  var f=document.getElementById('arrForm');
  function chk(id,err,ok,msg){document.getElementById(id).closest('.t-field').classList.toggle('is-bad',!ok);document.getElementById(err).textContent=ok?'':msg;return ok;}
  f.addEventListener('submit',function(e){
    e.preventDefault();document.getElementById('arrErr').textContent='';
    var n=document.getElementById('a-name').value.trim(),m=document.getElementById('a-mail').value.trim(),p=document.getElementById('a-prod').value.trim();
    var ok=[chk('a-name','ae-name',n.length>=3,'Escribí tu nombre y apellido.'),chk('a-mail','ae-mail',/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(m),'Revisá el mail, parece incompleto.'),chk('a-prod','ae-prod',p.length>=3,'Contanos qué compraste.')].every(Boolean);
    if(!ok)return;
    var b=document.getElementById('arrBtn');b.disabled=true;b.textContent='Enviando…';
    fetch('https://formsubmit.co/ajax/contacto.rush3d@gmail.com',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({
      _subject:'Botón de arrepentimiento · '+n,_template:'table',_captcha:'false',_honey:document.getElementById('a-hp').value,
      _autoresponse:'Hola '+n.split(' ')[0]+', recibimos tu solicitud de arrepentimiento por: '+p+'. En menos de 24 h te respondemos con el código de trámite. — Rush 3D',
      Tipo:'Solicitud de arrepentimiento (revocación)',Nombre:n,email:m,WhatsApp:document.getElementById('a-wa').value||'—',
      Recibido:document.getElementById('a-date').value||'—',Producto:p,Comentario:document.getElementById('a-msg').value||'—'})})
    .then(function(r){return r.json().then(function(d){if(!r.ok||String(d.success)!=='true')throw 0;});})
    .then(function(){f.hidden=true;document.getElementById('arrSent').hidden=false;})
    .catch(function(){document.getElementById('arrErr').textContent='No pudimos enviar la solicitud. Probá de nuevo o escribinos a contacto.rush3d@gmail.com.';})
    .finally(function(){b.disabled=false;b.textContent='Enviar solicitud';});
  });
})();
</script>
''' + FOOT + '</body>\n</html>\n'
(ROOT / 'tienda' / 'arrepentimiento' / 'index.html').write_text(arr)
print('OK', TIENDA_CSS, NAFTA_JS)
