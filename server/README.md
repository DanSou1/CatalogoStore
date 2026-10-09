# Servidor de firma para Wompi

Esta carpeta no se despliega en GitHub Pages — es una función aparte,
necesaria porque la clave secreta de integridad de Wompi nunca debe vivir en
el código del sitio. Se despliega una sola vez en Cloudflare Workers (capa
gratuita).

## Pasos

1. Crea una cuenta gratuita en [cloudflare.com](https://cloudflare.com) si no
   tienes una.
2. Desde esta carpeta (`server/`), instala Wrangler (la herramienta de
   Cloudflare) y autentícate:
   ```
   npx wrangler login
   ```
3. Configura tu clave secreta de integridad (la "Integrity Secret" de tu
   dashboard de Wompi, en Developers → API Keys) como secreto — **nunca la
   escribas en ningún archivo del repositorio**:
   ```
   npx wrangler secret put WOMPI_INTEGRITY_SECRET
   ```
   (te va a pedir pegarla; queda guardada cifrada en Cloudflare, no en el
   código).
4. Despliega:
   ```
   npx wrangler deploy
   ```
   Esto imprime la URL pública del Worker (algo como
   `https://wompi-signature.<tu-usuario>.workers.dev`).
5. Pega esa URL en `js/wompi-config.js`, en `WOMPI_SIGNATURE_ENDPOINT`.

Si cambias de dominio o usas un dominio propio en vez de
`dansou1.github.io`, actualiza también `ORIGEN_PERMITIDO` en
`wompi-signature.js` antes de desplegar de nuevo.
