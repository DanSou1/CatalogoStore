# CatalogoStore
Venta de productos con conexión a whatsapp

## Estilos locales
Los estilos Tailwind se sirven desde `css/tailwind.css`; la tienda no necesita descargar ni ejecutar Tailwind desde un CDN. Después de cambiar clases en HTML o JavaScript, regenerar desde la raíz:

```sh
npx --yes tailwindcss@3.4.17 -c tailwind.config.cjs -i css/tailwind-input.css -o css/tailwind.css --minify
```

Publicar también el CSS generado y actualizar `CACHE_NAME` en `js/sw.js` al cambiar recursos cacheados.
