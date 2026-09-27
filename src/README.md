# Código fuente

Lo que está en esta carpeta no se publica (ver `/.assetsignore`).

- `nafta.js` — visor 3D, personalización y pedido de la Lámpara NAFTA.
- `tienda.css` — estilos de la tienda (se cargan después de /assets/app.css).
- `build_tienda.py` — genera `/tienda/`, `/tienda/nafta/` y `/tienda/arrepentimiento/`.

## Compilar

```
cd src
npm install
npm run build              # genera src/dist/nafta.js
python3 build_tienda.py    # copia CSS/JS con hash y regenera las páginas de la tienda
```

Los archivos de `/assets` se cachean un año, por eso `build_tienda.py` les agrega un hash al nombre.
El modelo 3D está en `/models/nafta.glb` (comprimido con gltfpack + meshopt; el espesor de pared
va en COLOR_0 y el shader lo usa para simular cuánta luz atraviesa la pantalla).
