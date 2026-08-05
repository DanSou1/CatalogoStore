# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

ExperienceLove — a static, vanilla HTML/CSS/JS product catalog site ("Venta de productos con conexión a whatsapp"). No build step, no package manager, no framework. All product data lives in a single JSON file, and checkout is handled by generating a WhatsApp deep link rather than a real payment/checkout flow.

## Running / developing

There is no build or test tooling. Open `index.html` directly in a browser, or serve the folder with any static file server (e.g. `npx serve .`) — a real HTTP server is needed for `fetch("./js/productos.json")` and the service worker registration to work correctly (they will fail under `file://` in some browsers).

There are no linters, formatters, or automated tests configured in this repo.

## Architecture

Two pages share the same data/cart model via `localStorage`:

- **`index.html`** — product listing page. Loads `js/main.js`, which fetches `js/productos.json` on page load, renders product cards into `#contenedor-productos`, and wires category filter buttons.
- **`carrito.html`** — cart page. Loads `js/carrito.js`, which reads the cart out of `localStorage` and renders it independently (it does not re-fetch `productos.json`).
- Both pages load `js/menu.js` for the shared slide-out mobile nav (`aside`).

**Product catalog (`js/productos.json`)**: flat array of products, each with `id`, `titulo`, `imagen` (relative path into `img/<categoria>/`), `categoria: { nombre, id }`, and `precio`. Product `id`s are prefixed by category, e.g. `lenceria-01`.

**Category wiring is implicit and string-matched, not config-driven**: the sidebar buttons in `index.html` (`#cosmeticos`, `#lenceria`, `#Juegos`, `#Juguetes`, `#Bondage`, `#Lubricantes`, `#Sachet`, `#Promociones`) have `id` attributes that `main.js` matches directly against each product's `categoria.id` field via `producto.categoria.id === e.currentTarget.id`. **The casing must match exactly** — most category ids are capitalized (`Juegos`, `Bondage`, `Lubricantes`, `Sachet`, `Promociones`) but two are lowercase (`cosmeticos`, `lenceria`). When adding a new product or category, the `categoria.id` in `productos.json` must exactly match the corresponding button `id` in `index.html`, and product images go under `img/<categoria-folder>/`.

**Cart state (`js/main.js` + `js/carrito.js`)**: cart is a plain array of product objects (each with an added `cantidad` field) persisted to `localStorage` under the key `productos-en-carrito`. There is no cart module/API — both pages read/write this key directly and re-render their own DOM. The `#numerito` cart-count badge in the header is only updated by `main.js` (on `index.html`), not `carrito.js`.

**Checkout (`js/carrito.js` → `comprarCarrito`)**: builds a plain-text order summary and opens `https://wa.me/<numeroWhatsApp>?text=<mensaje>` in a new tab. The destination WhatsApp number is hardcoded in `carrito.js` (`numeroWhatsApp`). No server-side order processing exists.

**Service worker (`js/sw.js`)**: registered from inline script in `index.html` only (not `carrito.html`). Caches the app shell (`index.html`, `carrito.html`, `main.css`, the three JS files) at install, and caches `img/` responses on first fetch. Note the runtime image-caching check (`requestUrl.pathname.startsWith('./img/')`) compares against an absolute pathname, so it will never actually match — image caching via that branch is effectively dead code; images still get cached via the generic fetch handler fallback.

**Styling**: single stylesheet `css/main.css`, no preprocessor. Bootstrap Icons and Toastify (add-to-cart/remove toasts) and SweetAlert2 (cart-clear confirmation dialog) are all pulled in via CDN `<script>`/`<link>` tags, not npm.

## Content notes

- All UI text and product data is in Spanish (es-CO); this is a Colombian-market store.
- Prices are plain integers (COP), no currency formatting/locale library is used — displayed as `$${precio}`.
