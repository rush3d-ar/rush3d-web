# rush3d.ar

Sitio estático de Rush (impresión 3D y diseño CAD, Buenos Aires). Se sirve desde un
Cloudflare Worker con **Static Assets** (no Pages).

## Estructura

- `index.html` — página completa (HTML + CSS + JS inline, como en producción).
- `images/` — imágenes referenciadas por el HTML.
- `wrangler.toml` — configuración para desplegar con Wrangler / Cloudflare Builds.

## Imágenes pendientes

La sección "Trabajos" (2 casos + galería de 3 piezas) usa 5 fotos de producto que
todavía no subimos. Para no romper el sitio en vivo mientras tanto, esos bloques
quedaron comentados en `index.html` (buscar el comentario que empieza con
"Casos y galería pendientes") y la sección muestra un texto genérico en su lugar.

Nombres de archivo ya reservados en `images/` para cuando estén las fotos:

- `images/case-sportclub-nfc.jpg` — cartel NFC para SportClub Martínez
- `images/case-camioneta-1967.jpg` — plafón de camioneta 1967
- `images/gallery-portallaves-garage.jpg`
- `images/gallery-maceta-dos-piezas.jpg`
- `images/gallery-maceta-dragon.jpg`

Cuando subas esas 5 imágenes a `images/`, descomentar ese bloque en `index.html`
y restaurar el texto original de la sección.

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
- Analytics y tracking instalados en `index.html`: Cloudflare Web Analytics,
  Google Analytics 4 (G-XFLXBW8GWH), Meta Pixel (379032344154547) y Microsoft
  Clarity (yn0ithy1xb).
- Google Search Console verificado para el dominio rush3d.ar.
