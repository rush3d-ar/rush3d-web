# rush3d.ar

Sitio estático de Rush (impresión 3D y diseño CAD, Buenos Aires). Se sirve desde un
Cloudflare Worker con **Static Assets** (no Pages).

## Estructura

- `index.html` — página completa (HTML + CSS + JS inline, como en producción).
- `images/` — imágenes referenciadas por el HTML.
- `wrangler.toml` — configuración para desplegar con Wrangler / Cloudflare Builds.

## Imágenes pendientes

El sitio en vivo tiene 7 imágenes embebidas como `data:` base64 dentro del HTML.
Ya extraje y coloqué en `images/` los 2 logos (se usan varias veces, así que
convenía tenerlos como archivo aparte):

- `images/logo-word-mask.png`
- `images/logo-bolt.png`

Las **5 fotos de producto** (casos de "Trabajos" y la galería) quedaron
referenciadas en `index.html` con estos nombres, pero **todavía no están en
`images/`** — hay que subirlas manualmente (arrastrándolas en la interfaz web
de GitHub alcanza):

- `images/case-sportclub-nfc.jpg` — cartel NFC para SportClub Martínez
- `images/case-camioneta-1967.jpg` — plafón de camioneta 1967
- `images/gallery-portallaves-garage.jpg`
- `images/gallery-maceta-dos-piezas.jpg`
- `images/gallery-maceta-dragon.jpg`

Preferí pedirte estas 5 en vez de reconstruirlas byte a byte desde el base64
de producción: seguramente tengas los archivos originales (mejor calidad que
un JPEG re-codificado) a mano en tu teléfono o carpeta de fotos del taller.
Si no los tenés, decime y las extraigo igual del sitio en vivo.

Hasta que subas esas 5 imágenes, esas secciones del sitio se van a ver rotas
si desplegás este repo tal cual — no afecta al resto del sitio.

## Cómo desplegar

Con el repo conectado a Cloudflare Workers (Settings → Builds → Git
repository → GitHub), cada push a la rama configurada dispara un build y
deploy automático. También se puede desplegar a mano con:

```
npx wrangler deploy
```

## Notas técnicas

- El formulario de contacto usa [FormSubmit](https://formsubmit.co/) apuntando
  a `contacto.rush3d@gmail.com` (sin backend propio).
- Ya tiene instalado Cloudflare Web Analytics (beacon en el `<script>` final).
- Falta agregar: Google Search Console, Google Analytics (GA4), Microsoft
  Clarity y Meta Pixel — ver tareas pendientes en la conversación con Iván.
