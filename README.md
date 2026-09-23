# rush3d.ar

Sitio estático de Rush (impresión 3D y diseño CAD, Buenos Aires). Se sirve desde un
Cloudflare Worker con **Static Assets** (no Pages).

## Estructura

- `index.html` — página completa (HTML + CSS + JS inline, como en producción).
- `images/` — imágenes referenciadas por el HTML.
- `wrangler.toml` — configuración para desplegar con Wrangler / Cloudflare Builds.

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
