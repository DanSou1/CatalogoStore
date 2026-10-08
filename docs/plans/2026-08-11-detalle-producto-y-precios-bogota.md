---
status: in_progress
author: Daniel
created_at: 2026-08-11
tags: [plan, catalogo, producto, precios, ui]
related:
  - docs/research/detalle-producto-y-precios-bogota-uiux.md
ui_ux_review: applied
ui_ux_review_reason: modal de detalle (nuevo, modo diseño) y trigger en card de producto (modo híbrido) revisados con design-reviewer; UX Spec cerrado inline en Fase 2
contracts_review: not_applicable
contracts_review_reason: sitio estático sin build ni endpoints/API (checkout via WhatsApp deep link) — no aplica
security_review: not_applicable
security_review_reason: pendiente de evaluación al cierre — no hay superficie de auth/input remoto nueva, solo contenido estático y llamadas de solo lectura a `productos.json`
mrs:
  qa: null
  pre_prod: null
  master: null
---

# Detalle de producto (modal) + enriquecimiento de contenido y precios — Plan de implementación

## Overview

Agregar un botón "Ver más información" en cada card del catálogo (`index.html`) que abre un modal con descripción, precio, medidas y (si aplica según la categoría) recomendaciones de cuidado/salud, con opción de agregar al carrito desde ahí. En paralelo, enriquecer los 76 productos de `js/productos.json` con ese contenido (investigado por categoría/tipo de producto, ya que no hay ficha técnica de proveedor) y con precios promedio de mercado en Bogotá. El contenido (descripción/medidas/cuidado y uso) se publica solo después de que el usuario apruebe una tabla de propuesta; el precio, por pedido explícito del usuario, se investiga y se aplica directo, quedando un registro con las fuentes para que el usuario corrija manualmente cualquier valor puntual que no le convenza.

## Análisis del estado actual

El sitio es 100% estático (HTML/CSS/JS vanilla, sin build ni framework — ver `CLAUDE.md`). El modelo de datos hoy es plano y mínimo: `id`, `titulo`, `imagen`, `categoria{nombre,id}`, `precio` (`js/productos.json:1-765`, 76 productos). No existe ningún campo de descripción, medidas o salud, ni ningún componente de modal/diálogo en `css/main.css` — esta es una superficie 100% nueva.

Las cards se generan íntegramente por template string en `cargarProductos()` (`js/main.js:23-44`), re-renderizado completo en cada filtro de categoría. El carrito (`js/carrito.js`) persiste el objeto de producto completo (con `cantidad` agregado) en `localStorage` bajo `productos-en-carrito`, así que cualquier campo nuevo que agreguemos a `productos.json` viaja automáticamente al carrito sin cambios adicionales en `carrito.js`.

### Hallazgos clave:

- **Ids duplicados existentes**: `bondage-02` y `lubricante-05` aparecen 2 veces cada uno en `productos.json` (categoría original + copia re-etiquetada `categoria: "Promociones"`, confirmado programáticamente — 76 productos totales, 2 pares duplicados). `Array.find()`/`findIndex()` por `id` (usado en `js/main.js:108`, `js/carrito.js:102/110/124`) siempre resuelve al primer match, lo que ya es una fuente de bugs latente en el carrito y lo sería también para el modal si no se corrige antes (ver D6).
- **El id del producto viaja como atributo `id` HTML real** (`js/main.js:36`), no como `data-id`. `agregarAlCarrito` lo lee vía `e.currentTarget.id` (`js/main.js:107`). Un segundo control (el trigger "Ver más información") en el mismo elemento no puede reusar `id` sin colisionar.
- **Cero estilos de foco** (`:focus`/`:focus-visible`) en todo `css/main.css` — el sitio depende del anillo por defecto del navegador. Los controles nuevos deben definir foco explícito (hallazgo del design review).
- Las imágenes en `img/<categoria>/` son casi 1:1 con los productos (conteo de archivos vs. productos por carpeta), pero ninguna trae escala/referencia de tamaño — no se puede derivar una medida exacta de una foto sola.
- No hay `service-manifest.yaml` en este repo → sin spec de stack; se usó `frontend-react` como fallback solo para elegir la skill de design-review (`web-ui-review`), pero toda la implementación es HTML/CSS/JS vanilla, sin JSX ni estado de componente.
- `js/sw.js` precachea una lista fija de archivos (`urlsToCache`, `js/sw.js:4-12`); cualquier archivo JS nuevo debe agregarse ahí explícitamente o quedará sin cachear/desactualizado offline.

## Estado final deseado

- Cada card del catálogo tiene un botón "Ver más información" que abre un modal con imagen, categoría, título completo (sin truncar), precio, descripción, medidas (si aplica) y un bloque "Cuidado y uso" (si aplica según categoría), con botón "Agregar al carrito" funcional desde el modal.
- Los 76 productos en `productos.json` tienen `descripcion` (todos), y `medidas`/`recomendacionesSalud` donde aplique, con contenido aprobado explícitamente por el usuario vía tabla de revisión.
- Los precios de `productos.json` reflejan un promedio de mercado en Bogotá investigado por tipo de producto, también aprobado explícitamente vía tabla comparativa antes de escribirse.
- Los ids duplicados (`bondage-02`, `lubricante-05`) quedan únicos.

**Verificación**: servir el sitio con `npx serve .` (requerido para que `fetch("./js/productos.json")` funcione — ver `CLAUDE.md`), recorrer las 7 categorías del menú abriendo el modal en al menos un producto de cada una, y confirmar que el carrito/WhatsApp reflejan los precios actualizados.

## Lo que NO estamos haciendo

- No creamos backend ni checkout real — el flujo de compra sigue siendo el link de WhatsApp existente (`js/carrito.js:166-194`), sin tocar `numeroWhatsApp`.
- No creamos una página de detalle con URL propia ni router — es un modal sobre `index.html` (D3).
- No agregamos el botón de detalle a `carrito.html` (D5) — solo al catálogo.
- No migramos el proyecto a un framework ni agregamos build tooling — sigue siendo HTML/CSS/JS vanilla, un único archivo `css/main.css`.
- No garantizamos medidas exactas de fábrica: son aproximaciones de mercado por tipo de producto, investigadas en la Fase 3 (no hay ficha técnica de proveedor disponible).
- No emitimos asesoría médica formal: "Cuidado y uso" es contenido de higiene/seguridad de producto propio de un retail del rubro, no una consulta clínica.
- No sobrescribimos contenido (descripción/medidas/cuidado y uso) sin aprobación humana explícita — pasa primero por una tabla de revisión (D1). El precio es la excepción explícita: se aplica directo por pedido del usuario (D2, revisada), quedando un registro con fuentes para corrección manual posterior.
- No agregamos filtros ni búsqueda por medidas/precio — fuera de alcance de este plan.

## Approach de implementación

El plan se divide en 5 fases con dos ejes independientes que se pueden verificar por separado: (1) UI del modal, que funciona con o sin los campos nuevos gracias a renderizado condicional, y (2) enriquecimiento de datos (contenido y precio). El eje de contenido tiene un paso de investigación/propuesta seguido de un paso de aplicación separado por una aprobación explícita del usuario (D1); el eje de precio investiga y aplica en la misma fase, sin gate intermedio (D2, revisada a pedido del usuario). El orden — ids duplicados primero, luego UI, luego contenido, luego precio — evita que el modal se construya sobre un bug de identidad de producto, y permite testear la UI visualmente antes de que exista contenido real (el modal debe degradar con gracia cuando `descripcion`/`medidas`/`recomendacionesSalud` no existen, que es el estado de `productos.json` hasta la Fase 4).

### Decisiones arquitectónicas

**D1: Fuente del contenido (descripción/medidas/cuidado)**
Decisión: se genera un borrador investigado por categoría/tipo de producto, entregado como tabla de revisión; el usuario aprueba o edita antes de que se escriba a `productos.json` (Fases 3→4).
Alternativas descartadas: publicar directo sin revisión (riesgo de dato incorrecto visible a clientes reales sin checkpoint); pedir al usuario/proveedor los datos reales (más confiable pero bloquea el plan indefinidamente sin ficha técnica disponible).
Rationale: no hay ficha técnica de proveedor — solo foto + título — así que el contenido es necesariamente aproximado; una revisión intermedia es el balance entre avanzar y no publicar datos incorrectos en un sitio con checkout real. Decisión del usuario.

**D2: Actualización de precio**
Decisión (revisada 2026-08-11 tras feedback del usuario en la revisión del plan): se investiga precio promedio de mercado en Bogotá por tipo de producto (no por SKU exacto, la mayoría son productos de dropshipping genérico sin marca rastreable) y se **aplica directo** a `precio` en `productos.json`, sin tabla de aprobación previa. El research doc con fuentes/rango queda igual como registro, para que el usuario pueda ajustar manualmente cualquier precio puntual que no le convenza después de verlo en vivo.
Alternativas descartadas: tabla de propuesta con aprobación explícita antes de escribir (decisión original de este plan) — el usuario prefirió no bloquear la fase con un checkpoint intermedio, dado que puede corregir precios individuales manualmente si hace falta.
Rationale: decisión explícita del usuario, priorizando avanzar sin esperar una revisión fila por fila de 76 precios, aceptando el riesgo de tener que corregir manualmente casos puntuales después.

**D3: Patrón de UI para el detalle**
Decisión: modal/overlay sobre `index.html`, sin página ni router nuevo.
Alternativas descartadas: página de detalle `producto.html?id=X` — dar URL compartible por producto, pero duplica lógica de fetch/carrito que hoy solo vive en `main.js`/`carrito.js` y requiere un archivo HTML nuevo.
Rationale: consistente con el patrón actual de una sola página con toggles de clase (el `<aside>` y el carrito ya funcionan así); más simple sin build ni router. Decisión del usuario.

**D4: Criterio para "recomendaciones de salud" (mostrado en UI como "Cuidado y uso", ver D10)**
Decisión: por categoría. Llevan el bloque: Lubricantes, Sachet, Juguetes, Cosméticos (contacto con piel/mucosas). No lo llevan por defecto: Juegos, Bondage no invasivo (accesorios/juegos de mesa, esposas, antifaces) — con excepción puntual si un producto específico lo amerita claramente (ej. pinzas para pezones dentro de Bondage).
Alternativas descartadas: evaluación producto por producto sin criterio — más preciso pero inconsistente y más trabajo de revisión sin garantía de criterio uniforme.
Rationale: consistente y fácil de mantener cuando se agreguen productos nuevos al catálogo. Decisión del usuario.

**D5: Alcance del botón de detalle**
Decisión: solo en `index.html` (catálogo). No se agrega a `carrito.html`.
Rationale: en el carrito el usuario ya eligió el producto y solo necesita sumar/restar/eliminar; mantiene `carrito.js`/`carrito.html` sin tocar y acota el alcance. Decisión del usuario.

**D6: Ids duplicados**
Decisión: se corrigen como fase propia (Fase 1), antes de construir el modal.
Alternativas descartadas: dejarlo fuera de alcance como deuda técnica conocida.
Rationale: el modal identifica productos por `id` (vía `data-id`); construirlo sobre ids ambiguos heredaría el mismo bug que ya existe en el carrito, en vez de solo documentarlo. Decisión del usuario.

**D7: Formato de `medidas`**
Decisión: texto libre por producto (string simple, ej. "12 cm x 3 cm de diámetro", "30 ml", "Talla única"). Si no aplica, se omite el campo por completo en vez de forzar un valor.
Alternativas descartadas: estructura fija `{ largo, diametro, volumen, unidad }` — más consistente para filtros futuros, pero deja campos vacíos en categorías donde no aplican (cosméticos, juegos) y exige renderizado condicional por campo en vez de por bloque.
Rationale: flexible para cualquier categoría, más simple de completar en la tabla de revisión y de renderizar (un solo `if` por bloque, no por campo). Decisión del usuario.

**D8: Arquitectura del modal — `<dialog>` nativo**
Decisión: elemento `<dialog>` con `showModal()`, no un `div` + clase al estilo del `<aside>` mobile existente.
Alternativas descartadas: calcar el patrón `.aside-visible` (`css/main.css:743-761`, scrim vía `box-shadow: 0 0 0 100vmax`) — ese scrim se ancla al box del propio elemento y se rompe con un panel centrado que hace scroll interno; y reimplementar focus trap/ESC/retorno de foco a mano (~60 líneas frágiles sin cobertura de test en el repo).
Rationale (design review, ver research doc `-uiux`): `<dialog>` da focus trap, ESC, `::backdrop` e inertización del fondo gratis vía la plataforma, con ~25 líneas de JS de orquestación contra ~80 de una implementación manual. El único trade-off (el `<dialog>` pinta en el top layer, por encima de cualquier z-index, así que un toast montado en `body` quedaría detrás del scrim) se resuelve montando el toast del CTA del modal dentro del propio `<dialog>` (opción `selector` de Toastify).

**D9: Trigger "Ver más información" en la card**
Decisión (revisada 2026-08-11 tras feedback del usuario post-implementación): botón pill con borde (ícono `visibility` 17px + etiqueta "Ver más información"), fondo/borde translúcidos sobre el plum, apilado bajo el precio dentro de `.producto-detalles`. Sigue siendo visualmente secundario a `.producto-agregar` (que es sólido, no con borde) pero con más peso de "botón" real que un link de texto.
Alternativas descartadas: (1) fila de dos acciones con trigger circular ícono-only al lado de "Agregar" — descartada en el review de diseño original porque el pedido explícito era una etiqueta legible y por restricciones de ancho en el grid mobile de 2 columnas (ver rationale original abajo); (2) acción de texto plano subrayado con ícono `info` (primera versión implementada) — el usuario la encontró poco amigable y el ícono `info` se confundía visualmente con un signo de exclamación; se reemplazó por el botón pill actual sin reabrir la decisión de layout (sigue apilado bajo el precio, sigue subordinado a "Agregar").
Rationale original (design review): la jerarquía de conversión de la tienda exige que "Agregar" siga siendo el elemento con más peso visual — se preserva en la revisión: el pill tiene borde y fondo translúcido, `.producto-agregar` sigue siendo sólido.
Rationale de la revisión: feedback directo del usuario sobre la primera implementación — decisión suya, no un nuevo hallazgo de research.

**D10: Estilo del bloque "Cuidado y uso"**
Decisión: callout con tinte de marca — `rgba(131,32,98,.06)` + `border-left: 3px solid var(--clr-plum)`, ícono `health_and_safety`, título "Cuidado y uso" (no "Recomendaciones de salud" en la UI, para evitar el registro clínico).
Alternativas descartadas: callout neutro gris (`--clr-surface-container-low`) — se aplanaba contra el resto del contenido, perdiendo el énfasis pedido, y el ícono neutro candidato (`spa`) ya está tomado semánticamente por la categoría "Cosméticos" en el nav; tratamiento en rojo/`--clr-error` — ya reservado en el proyecto para acciones destructivas (`.carrito-producto-eliminar`) y se leería como advertencia médica formal, no como nota de cuidado de un retail.
Rationale (design review): distingue el bloque sin verse alarmante, dentro del universo visual de la tienda, con precedente ya en el código (`.estado-icono-exito`, `css/main.css:442-449`).

**D11: Compatibilidad con GitHub Pages (agregada 2026-08-11 tras feedback del usuario)**
Decisión: todo lo agregado en este plan debe ser servible por GitHub Pages sin build step ni configuración de servidor — mismo modelo que el resto del sitio hoy.
Rationale: el usuario confirmó que el sitio se despliega en GitHub Pages, un host de archivos estáticos puro (sin server-side, sin variables de entorno, sin redirects/headers custom salvo `_headers`/`404.html` que este plan no usa). Esto ya está satisfecho por diseño (D3, D8): `<dialog>` es una API nativa del navegador sin dependencias nuevas, todos los paths nuevos (`js/detalle.js`, referencias a `productos.json`) usan rutas relativas (`./...`) igual que el resto del proyecto, y no se agrega ningún build tool. El único riesgo real es de **sensibilidad a mayúsculas/minúsculas**: GitHub Pages sirve desde un filesystem case-sensitive (Linux), a diferencia de Windows donde se está desarrollando — un mismatch de casing en un nombre de archivo o carpeta (ej. `img/Lubricantes/` vs. `img/lubricantes/`) que pasa desapercibido en local rompe en producción. Se agrega verificación explícita de esto en los criterios de éxito de cada fase que toca paths (Fase 2).

---

## Phase 1: Corrección de ids duplicados

### Overview

Asignar un id único a las dos entradas de `productos.json` que hoy reusan el id de su categoría original al reaparecer en "Promociones", eliminando la ambigüedad de `Array.find()`/`findIndex()` antes de que el modal (Fase 2) dependa de `id` para identificar productos.

### Cambios requeridos:

#### 1. `productos.json` — ids únicos para las entradas duplicadas en Promociones

**Archivo**: `js/productos.json` (modificar)
**Cambios**: las dos entradas con `categoria.id: "Promociones"` que reusan un id ya existente en otra categoría pasan a tener un id propio con sufijo `-promo`:
- La entrada `bondage-02` bajo `categoria: "Promociones"` (hoy en `js/productos.json:716-724`) → `bondage-02-promo`.
- La entrada `lubricante-05` bajo `categoria: "Promociones"` (hoy en `js/productos.json:706-714`) → `lubricante-05-promo`.

Ningún otro campo cambia. No se tocan las entradas originales (`bondage-02` en `js/productos.json:344-353`, `lubricante-05` en `js/productos.json:435-444`), que conservan su id.

**Comportamiento**: sin cambios de comportamiento visible — el catálogo, el filtro de categorías y el carrito siguen funcionando igual, salvo que ahora cada botón "Agregar"/"Ver más información" en la vista "Promociones" referencia inequívocamente a su propia entrada de precio/contenido en vez de compartir la de la categoría original. Verificado que ningún archivo `.js` referencia estos ids de forma hardcodeada (grep sin matches), así que no hay otro punto del código a tocar en esta fase.

### Criterios de éxito:

#### Verificación automatizada:

- [x] `productos.json` sigue siendo JSON válido: `node -e "JSON.parse(require('fs').readFileSync('js/productos.json'))"` no lanza error.
- [x] No quedan ids duplicados: `node -e "const p=JSON.parse(require('fs').readFileSync('js/productos.json')); const ids=p.map(x=>x.id); const dup=ids.filter((id,i)=>ids.indexOf(id)!==i); if(dup.length) throw new Error('duplicados: '+dup)"` no lanza error.

#### Verificación manual:

- [~] Con `npx serve .`, la categoría "PROMOCIONES!" sigue mostrando los mismos 6 productos que antes, con el mismo precio y título.
- [~] Agregar al carrito el "Antifas bondage" desde Promociones y luego el de la categoría "Bondage" quedan como 2 líneas separadas en el carrito (cantidad 1 cada uno), no se fusionan en una sola línea de cantidad 2.

---

## Phase 2: UI — botón "Ver más información" + modal de detalle

### Overview

Agregar el trigger a la card de producto y el modal de detalle completo (imagen, título, precio, descripción, medidas, "Cuidado y uso", agregar al carrito), siguiendo el UX Spec cerrado en el design review (D8, D9, D10). El modal debe funcionar correctamente con `productos.json` en su estado actual (sin `descripcion`/`medidas`/`recomendacionesSalud` todavía — esos llegan en la Fase 4) gracias al renderizado condicional.

### Dependencias con fases previas

Depende de la Fase 1: el `data-id` del trigger y del CTA del modal asume ids únicos por producto — con los duplicados sin corregir, abrir el modal de un producto en "Promociones" podría resolver al producto equivocado.

### Decisiones UX globales de la fase

(Cerradas con el usuario antes del loop por componente, ver Step 1 de `/ui-ux-review`)

1. El modal usa exclusivamente las variables de color/radio/sombra ya existentes en `css/main.css` (`--clr-*`, `--radius-*`, `--shadow-*`) — sin paleta nueva.
2. Se cierra con botón X, tecla ESC, o click fuera del panel (en el `<dialog>`, clic donde `e.target === dialog`).
3. El toast "Producto agregado" del CTA del modal reusa exactamente el mismo estilo Toastify que ya usa la card (gradiente `linear-gradient(to right, #832062, #1B1A1A)`, `border-radius: 2rem`, uppercase, `.75rem`), montado dentro del `<dialog>` (ver D8).

### Cambios requeridos:

#### 1. Modelo de datos — nuevos campos opcionales en `productos.json`

**Archivo**: `js/productos.json` (modificar — solo shape, contenido real en Fase 4)

```json
{
  "id": "string",
  "titulo": "string",
  "imagen": "string",
  "categoria": { "nombre": "string", "id": "string" },
  "precio": "number",
  "descripcion": "string",
  "medidas": "string (opcional — se omite el campo si no aplica)",
  "recomendacionesSalud": "string (opcional — se omite el campo si no aplica, ver D4)"
}
```

**Comportamiento**: en esta fase no se agregan estos campos a los 76 productos todavía (eso es la Fase 4) — el modal se construye para tolerar su ausencia total, que es el estado real de `productos.json` hasta entonces.

#### 2. Card de producto — trigger "Ver más información"

**Archivo**: `js/main.js` (modificar, `cargarProductos()` en `js/main.js:23-44`)
**Patrón a seguir**: el template string existente de la card (`js/main.js:31-38`).

**Comportamiento**: el template de la card agrega un botón entre `.producto-precio` y `.producto-agregar`, con `data-id="${producto.id}"` (no `id`, para no colisionar con el atributo `id` que ya usa `.producto-agregar`). Un único listener delegado en `#contenedorProductos` (no un `forEach` re-bindeado por render, a diferencia de `actualizarBotonesAgregar()`) detecta clicks en `.producto-ver-mas` vía `e.target.closest()` y dispara la apertura del modal con el `id` del `dataset`. `agregarAlCarrito` (`js/main.js:85-121`) cambia su primera línea para leer `e.currentTarget.dataset.id || e.currentTarget.id`, con lo que sigue funcionando igual para `.producto-agregar` (que conserva su atributo `id` tal cual) y también sirve para el botón "Agregar al carrito" del modal (que usa `data-id`).

##### UX Spec — Card de producto (trigger "Ver más información")

> **Revisado 2026-08-11 tras feedback del usuario** (post-implementación inicial): el diseño original (link de texto subrayado + ícono `info`) se percibía poco amigable y el ícono `info` se confundía visualmente con un signo de exclamación. Se reemplaza por un botón pill con borde (más peso de "botón" real, sigue siendo visualmente secundario a `.producto-agregar` que es sólido) y el ícono `visibility` (más asociado a "ver/previsualizar" en convenciones de e-commerce). El spec de abajo ya refleja la versión vigente — la versión original queda solo como decisión descartada, documentada en D9.

**Markup** (dentro de `.producto-detalles`, entre `.producto-precio` y `.producto-agregar`):
```html
<button class="producto-ver-mas" type="button" data-id="${producto.id}">
    <span class="material-symbols-outlined" aria-hidden="true">visibility</span>
    Ver más información
</button>
```

**Estilos** (`css/main.css`, junto al bloque `.producto-*` en `css/main.css:330-402`):
```css
.producto-precio { margin-bottom: 0; }

.producto-ver-mas {
    position: relative;
    align-self: flex-start;
    display: inline-flex;
    align-items: center;
    gap: .35rem;
    margin-bottom: .5rem;
    padding: .4rem .85rem;
    border: 1.5px solid rgba(255, 255, 255, .45);
    border-radius: var(--radius-full);
    background-color: rgba(255, 255, 255, .06);
    color: rgba(255, 255, 255, .92);
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .01em;
    cursor: pointer;
    touch-action: manipulation;
    transition: background-color .2s, border-color .2s, color .2s;
}

.producto-ver-mas .material-symbols-outlined { font-size: 17px; }

.producto-ver-mas::after {
    content: '';
    position: absolute;
    inset: -.35rem;
}

.producto-ver-mas:hover {
    background-color: rgba(255, 255, 255, .16);
    border-color: rgba(255, 255, 255, .8);
    color: var(--clr-surface);
}

.producto-ver-mas:focus-visible,
.producto-agregar:focus-visible {
    outline: 2px solid var(--clr-surface);
    outline-offset: 2px;
    border-radius: var(--radius-sm);
}
```

**Accesibilidad**: `<button type="button">`, ícono `visibility` con `aria-hidden="true"` (la etiqueta visible ya es el nombre accesible). Hit target ≥44×44px vía `::after` con `inset` negativo, sin costo de layout — el padding propio del botón ya suma altura real, así que el `inset` se redujo de `-.5rem` a `-.35rem` para no superponerse con el botón "Agregar" contiguo. Contraste blanco 92% sobre `--clr-plum` = ~6.8:1 (pasa 4.5:1 para texto pequeño); borde `rgba(255,255,255,.45)` da ~3:1 sobre el fondo plum (pasa el mínimo 3:1 para elementos no textuales).

**Estados**: `default` (fondo blanco 6%, borde blanco 45%, texto blanco 92%) · `hover` (fondo blanco 16%, borde blanco 80%, texto blanco 100%) · `focus-visible` (anillo blanco 2px, también agregado a `.producto-agregar` que hoy no tiene ninguno) · `active` (hereda hover). Sin `disabled` ni `loading` — el trigger siempre es válido y el modal se llena desde el array `productos` ya en memoria.

**Copy**: "Ver más información" en sentence case (no uppercase, para reforzarlo como secundario frente al "AGREGAR" en mayúsculas). Vocabulario consistente de punta a punta: card "Agregar" → modal "Agregar al carrito" → toast "Producto agregado".

#### 3. Modal de detalle de producto — markup, estilos e integración

**Archivo**: `index.html` (modificar — agregar el `<dialog>` + registrar `js/detalle.js`)
**Archivo**: `js/detalle.js` (nuevo)
**Archivo**: `css/main.css` (modificar — agregar bloque `.modal-*`)

**Integración en `index.html`**: el `<dialog>` se agrega como markup estático, fuera de `.wrapper` (para que ningún `transform`/`overflow` ancestro le cree un containing block que rompa `showModal()`), inmediatamente antes de los `<script>` de cierre de body:

```html
<!-- después de </div> que cierra .wrapper, antes de los <script> -->
<dialog id="modal-producto" class="modal-producto" aria-labelledby="modal-producto-titulo">
  <!-- contenido: ver markup completo abajo -->
</dialog>
<script src="./js/detalle.js"></script>
```

`js/detalle.js` se agrega al final de la lista de `<script>`, después de `js/main.js` (necesita que el array global `productos` ya esté declarado — ambos son scripts clásicos sin `type="module"`, comparten el mismo scope léxico de nivel superior del documento, igual que ya ocurre implícitamente entre los `<script>` existentes).

**Markup completo del `<dialog>`**:
```html
<dialog id="modal-producto" class="modal-producto" aria-labelledby="modal-producto-titulo">
  <div class="modal-panel">
    <span class="modal-handle" aria-hidden="true"></span>
    <button class="modal-cerrar" type="button" aria-label="Cerrar" autofocus>
      <span class="material-symbols-outlined" aria-hidden="true">close</span>
    </button>
    <div class="modal-media">
      <img class="modal-imagen" src="" alt="" width="440" height="550">
    </div>
    <div class="modal-contenido">
      <div class="modal-cuerpo">
        <p class="modal-categoria"></p>
        <h2 class="modal-titulo" id="modal-producto-titulo"></h2>
        <p class="modal-precio"></p>
        <p class="modal-descripcion" id="modal-producto-descripcion"></p>
        <div class="modal-fichas">
          <dl class="modal-ficha">
            <dt><span class="material-symbols-outlined" aria-hidden="true">straighten</span>Medidas</dt>
            <dd></dd>
          </dl>
          <div class="modal-nota">
            <p class="modal-nota-titulo">
              <span class="material-symbols-outlined" aria-hidden="true">health_and_safety</span>Cuidado y uso
            </p>
            <p class="modal-nota-texto"></p>
          </div>
        </div>
      </div>
      <div class="modal-pie">
        <button class="modal-agregar" type="button" data-id="">
          <span class="material-symbols-outlined" aria-hidden="true">add_shopping_cart</span>Agregar al carrito
        </button>
      </div>
    </div>
  </div>
</dialog>
```

`.modal-fichas` (y dentro, `.modal-ficha` / `.modal-nota` por separado) y `.modal-descripcion` se construyen/limpian condicionalmente desde JS al abrir el modal — ver tabla de reglas por estado abajo. El markup estático de arriba es la plantilla estructural completa; `abrirModal()` puede vaciar `.modal-fichas` y solo re-poblar los sub-bloques que apliquen para el producto actual.

**Estilos base**:
```css
.modal-producto {
    width: 100vw;
    max-width: none;
    height: 100dvh;
    max-height: none;
    margin: 0;
    padding: 0;
    border: 0;
    background: transparent;
    overflow: hidden;
}

.modal-producto[open] {
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-producto::backdrop {
    background-color: rgba(0, 0, 0, .75);
    animation: modal-scrim-entrada .25s ease-out;
}

.modal-panel {
    display: flex;
    width: min(880px, calc(100vw - 2 * var(--space-gutter)));
    max-height: min(640px, calc(100dvh - 2 * var(--space-gutter)));
    background-color: var(--clr-surface);
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-card);
    overflow: hidden;
    position: relative;
    animation: modal-panel-entrada .25s ease-out;
}

.modal-media {
    flex: 0 0 42%;
    background-color: var(--clr-surface-container-low);
}

.modal-imagen {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
}

.modal-contenido {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    overscroll-behavior: contain;
}

.modal-cuerpo {
    display: flex;
    flex-direction: column;
    gap: .5rem;
    padding: 2rem 1.75rem 1.25rem;
}

.modal-cerrar {
    position: absolute;
    top: .75rem;
    right: .75rem;
    z-index: 1;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 0;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, .9);
    backdrop-filter: blur(4px);
    color: var(--clr-charcoal);
    cursor: pointer;
    touch-action: manipulation;
    transition: background-color .2s;
}

.modal-cerrar:hover { background-color: var(--clr-surface-container); }
.modal-handle { display: none; }
```

**Tipografía**:
```css
.modal-categoria {
    font-size: .7rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .08em; color: var(--clr-on-surface-variant);
}

.modal-titulo {
    font-size: 1.5rem; font-weight: 700; line-height: 1.25;
    color: var(--clr-charcoal); text-wrap: balance;
}

.modal-precio {
    font-size: 1.75rem; font-weight: 800; color: var(--clr-plum);
    font-variant-numeric: tabular-nums; margin-top: .25rem;
}

.modal-descripcion {
    font-size: 1rem; font-weight: 400; line-height: 1.65;
    color: var(--clr-on-surface-variant); max-width: 58ch; margin-top: .75rem;
}
```

**Fichas y nota de cuidado**:
```css
.modal-fichas {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1.25rem;
    padding-top: 1.25rem;
    border-top: 1px solid var(--clr-outline-variant);
}

.modal-ficha dt {
    display: flex; align-items: center; gap: .4rem;
    font-size: .75rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .05em; color: var(--clr-on-surface-variant);
}

.modal-ficha dt .material-symbols-outlined { font-size: 20px; }

.modal-ficha dd {
    margin-top: .25rem; padding-left: 1.6rem;
    font-size: .95rem; font-weight: 500; color: var(--clr-charcoal);
}

.modal-nota {
    background-color: rgba(131, 32, 98, .06);
    border-left: 3px solid var(--clr-plum);
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
    padding: .9rem 1rem;
}

.modal-nota-titulo {
    display: flex; align-items: center; gap: .4rem;
    font-size: .8rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .05em; color: var(--clr-plum);
}

.modal-nota-titulo .material-symbols-outlined { font-size: 20px; }

.modal-nota-texto {
    margin-top: .35rem; font-size: .9rem; line-height: 1.55;
    color: var(--clr-on-surface-variant);
}
```

**Pie sticky + CTA**:
```css
.modal-pie {
    position: sticky; bottom: 0; margin-top: auto;
    padding: 1rem 1.75rem;
    background-color: var(--clr-surface);
    border-top: 1px solid var(--clr-outline-variant);
}

.modal-agregar {
    width: 100%;
    display: flex; align-items: center; justify-content: center; gap: .5rem;
    border: 0;
    background-color: var(--clr-plum);
    color: var(--clr-surface);
    padding: 1rem;
    text-transform: uppercase; letter-spacing: .04em;
    font-weight: 700; font-size: .85rem;
    border-radius: var(--radius-full);
    cursor: pointer; touch-action: manipulation;
    transition: background-color .2s;
}

.modal-agregar:hover { background-color: var(--clr-charcoal); }
.modal-agregar.confirmado { background-color: var(--clr-charcoal); }

.modal-cerrar:focus-visible,
.modal-agregar:focus-visible {
    outline: 2px solid var(--clr-plum);
    outline-offset: 2px;
}
```

**Responsive (≤600px, mismo breakpoint que ya usa `<aside>` en `css/main.css:735`)**:
```css
@media screen and (max-width: 600px) {
    .modal-producto[open] { align-items: flex-end; }

    .modal-panel {
        flex-direction: column;
        width: 100%;
        max-height: 92dvh;
        border-radius: var(--radius-xl) var(--radius-xl) 0 0;
        animation-name: modal-sheet-entrada;
        animation-duration: .2s;
    }

    .modal-handle {
        display: block;
        width: 36px; height: 4px;
        margin: .6rem auto .2rem;
        border-radius: var(--radius-full);
        background-color: var(--clr-outline-variant);
        flex-shrink: 0;
    }

    .modal-media { flex: none; }
    .modal-imagen { aspect-ratio: 16 / 10; height: auto; }
    .modal-cuerpo { padding: 1.25rem 1.25rem 1rem; }
    .modal-pie { padding: .85rem 1.25rem calc(.85rem + env(safe-area-inset-bottom)); }
}
```

**Movimiento**:
```css
@keyframes modal-scrim-entrada  { from { opacity: 0; } }
@keyframes modal-panel-entrada  { from { opacity: 0; transform: translateY(12px) scale(.98); } }
@keyframes modal-panel-salida   { to   { opacity: 0; transform: translateY(12px) scale(.98); } }
@keyframes modal-sheet-entrada  { from { transform: translateY(100%); } }
@keyframes modal-sheet-salida   { to   { transform: translateY(100%); } }

.modal-producto.cerrando .modal-panel { animation: modal-panel-salida .2s ease-in forwards; }
.modal-producto.cerrando::backdrop    { animation: modal-scrim-entrada .2s ease-in reverse forwards; }

@media screen and (max-width: 600px) {
    .modal-producto.cerrando .modal-panel { animation-name: modal-sheet-salida; }
}

@media (prefers-reduced-motion: reduce) {
    .modal-producto .modal-panel,
    .modal-producto::backdrop { animation-duration: .01ms !important; }
}
```

**Reglas por estado (campos opcionales)**:

| `medidas` | `recomendacionesSalud` | Comportamiento |
|---|---|---|
| presente | presente | `.modal-fichas` se emite con `<dl>` + `.modal-nota`, `gap: 1rem` |
| presente | ausente | `.modal-fichas` solo con `<dl>` |
| ausente | presente | `.modal-fichas` solo con `.modal-nota` |
| ausente | ausente | `.modal-fichas` no se emite (el `border-top` vive en el wrapper, no en un `<hr>` suelto — si el wrapper no se emite, no queda regla huérfana ni hueco) |

`descripcion` ausente → no se emite `.modal-descripcion` y se remueve el atributo `aria-describedby` del `<dialog>` (no debe apuntar a un id inexistente). Imagen rota → queda visible `background-color: var(--clr-surface-container-low)` de `.modal-media`; `object-fit: contain` evita el estiramiento. `medidas` con número+unidad usa `&nbsp;` entre ambos (ej. `12&nbsp;cm x 3&nbsp;cm`).

**Contrato de `js/detalle.js`**:

```js
function abrirModal(id) { /* busca en `productos`, rellena el dialog, dialog.showModal() */ }
function cerrarModal() { /* dispara la animación de salida */ }
```

**Comportamiento**:
- `abrirModal(id)` busca el producto en el array global `productos` (declarado en `js/main.js`) por `id`, rellena `.modal-categoria`/`.modal-titulo`/`.modal-precio`/`.modal-imagen` siempre, y construye condicionalmente `.modal-descripcion`/`.modal-fichas` según la tabla de arriba; setea `data-id` en `.modal-agregar`; llama `dialog.showModal()`; fija `document.body.style.overflow = 'hidden'`.
- El trigger `.producto-ver-mas` se cablea por delegación de evento en `#contenedor-productos` (no un `forEach` re-bindeado), igual que se especificó en el cambio de `main.js`.
- `cerrarModal()` agrega la clase `.cerrando` al `<dialog>`; el handler de `animationend` sobre `.modal-panel` llama a `dialog.close()`. El botón `.modal-cerrar`, un click en el propio `<dialog>` (`e.target === dialog`) y el evento nativo `cancel` (tecla ESC, con `e.preventDefault()` para dejar correr la animación) llaman a `cerrarModal()`.
- El evento `close` nativo del `<dialog>` restaura `body.style.overflow` y quita `.cerrando`. El retorno de foco al trigger que abrió el modal lo hace el navegador nativamente (parte de `showModal()`).
- El botón `.modal-agregar` invoca `agregarAlCarrito` (la misma función de `js/main.js`, ver cambio del punto 2) pasándole el evento; el toast Toastify de esa llamada se monta con la opción `selector: 'modal-producto'` cuando el trigger está dentro del `<dialog>` (para no quedar detrás del `::backdrop` en el top layer), y sin `selector` cuando es el botón de la card — `agregarAlCarrito` decide esto comprobando si `e.currentTarget.closest('#modal-producto')` es verdadero. Tras agregar, el CTA pasa a estado `.confirmado` (ícono `check_circle`, texto "Agregado") 1.6s y vuelve a su estado normal. El modal permanece abierto tras agregar.
- No hay estado `loading` ni `error`: el modal se llena desde el array `productos` ya cargado en memoria por `fetch` al inicio de `main.js`, sin red adicional.

**Accesibilidad**: `role="dialog"`/`aria-modal="true"` son implícitos de `showModal()` (no se declaran a mano). Foco inicial en `.modal-cerrar` vía `autofocus` (deliberadamente no en "Agregar al carrito", para evitar un Enter accidental que agregue el producto). Focus trap, inertización del fondo, ESC y retorno de foco: nativos del `<dialog>`, sin trap manual. Todos los targets ≥44×44px.

#### 4. Service Worker — agregar `js/detalle.js` al precache

**Archivo**: `js/sw.js` (modificar, `urlsToCache` en `js/sw.js:4-12`)
**Cambios**: agregar `'./js/detalle.js'` a la lista.

**Comportamiento**: sin este cambio, el sitio funcionaría online pero `js/detalle.js` no se serviría desde caché offline (queda desactualizado o ausente si el Service Worker previo sigue activo), rompiendo el botón de detalle sin conexión aunque el resto del shell cargue.

### Criterios de éxito:

#### Verificación automatizada:

- [x] `productos.json` sigue siendo JSON válido tras el cambio de shape: `node -e "JSON.parse(require('fs').readFileSync('js/productos.json'))"`.
- [x] No hay errores de sintaxis en los archivos JS nuevos/modificados: `node --check js/detalle.js` y `node --check js/main.js`.
- [x] (No aplica typecheck/lint/test automatizado — el repo no tiene esas herramientas configuradas, ver `CLAUDE.md`.)
- [x] Compatibilidad GitHub Pages (D11): verificado sin rutas absolutas (`grep src="/|href="/` sin matches) y `js/detalle.js` en disco coincide en mayúsculas/minúsculas exactas con la referencia en `index.html`.

#### Verificación manual:

- [ ] Con `npx serve .`, click en "Ver más información" en un producto de cada una de las 7 categorías (incluida "Todos") abre el modal con los datos correctos de ESE producto (no otro).
- [ ] Con `productos.json` sin `descripcion`/`medidas`/`recomendacionesSalud` (estado real hasta la Fase 4), el modal abre igual, sin huecos ni bloques vacíos, mostrando solo imagen/categoría/título/precio.
- [ ] El modal se cierra con: click en la X, tecla ESC, y click fuera del panel (en el scrim) — los 3 métodos.
- [ ] "Agregar al carrito" desde el modal actualiza el número del carrito (`#numerito`) y `localStorage.productos-en-carrito`, muestra el toast "Producto agregado" (visible por encima del scrim, no oculto detrás) y el CTA pasa brevemente a "Agregado" antes de volver.
- [ ] El carrito (`carrito.html`) refleja correctamente los productos agregados desde el modal, sumando cantidad si ya estaban.
- [ ] En viewport ≤600px, el modal se muestra como bottom sheet (no centrado) y el CTA queda alcanzable sin recortarse por la barra del navegador.
- [ ] Navegación por teclado: Tab dentro del modal no se escapa hacia el catálogo de fondo (focus trap); al cerrar, el foco vuelve al botón "Ver más información" que abrió el modal.
- [ ] `Ver más información` y `Agregar` tienen anillo de foco visible al navegar con Tab (antes no tenían ninguno).
- [ ] Sin conexión (tras un primer load online con el Service Worker activo), recargar la página y abrir el modal sigue funcionando.
- [ ] Sin regresiones: el filtro de categorías, "Agregar" directo desde la card, y el flujo de carrito/WhatsApp existentes siguen funcionando igual que antes de esta fase.

---

## Phase 3: Investigación y redacción de contenido (descripción, medidas, cuidado y uso)

### Overview

Producir, para los 76 productos, un borrador de `descripcion` (todos), `medidas` (donde aplique) y `recomendacionesSalud`/"Cuidado y uso" (donde aplique según D4), investigado por categoría/tipo de producto — no hay ficha técnica de proveedor, solo foto + título. El entregable es una tabla de revisión, no una escritura directa a `productos.json` (eso es la Fase 4).

### Dependencias con fases previas

No depende funcionalmente de la Fase 2 (la UI ya tolera la ausencia de estos campos), pero sí asume los ids ya únicos de la Fase 1 para poder referenciar cada fila de la tabla sin ambigüedad.

### Cambios requeridos:

#### 1. Tabla de propuesta de contenido

**Archivo**: `docs/research/2026-08-11-contenido-productos-propuesta.md` (nuevo)

**Comportamiento**: documento con una tabla de 76 filas, agrupada por categoría (`cosmeticos`, `Juegos`, `Juguetes`, `Bondage`, `Lubricantes`, `Sachet`, `Promociones`), con columnas `id | título | descripción propuesta | medidas propuestas (o "—") | cuidado y uso propuesto (o "—")`. Metodología a seguir por columna:

- **Descripción**: redactada a partir del título, la categoría y una inspección de la imagen del producto (`img/<categoria>/...`), en tono de copy de retail (no clínico), 200–450 caracteres por producto (guía del design review para que quepa en `max-width: 58ch` del modal sin forzar scroll largo en desktop).
- **Medidas**: investigadas por tipo de producto genérico comparable (no por SKU exacto — la mayoría son productos de dropshipping sin marca rastreable), con el texto libre indicando cuando el valor es una aproximación de mercado y no una especificación de fábrica confirmada (ej. "Aprox. 12 cm x 3 cm de diámetro"). Se omite la fila/columna para productos donde no aplica un valor medible relevante (ej. un juego de cartas no necesita medidas de la carta).
- **Cuidado y uso**: aplica por categoría según D4 (Lubricantes, Sachet, Juguetes, Cosméticos sí; Juegos y Bondage no invasivo no, salvo excepción puntual justificada en la tabla). Contenido de higiene/seguridad de producto (ej. compatibilidad de lubricantes con látex, prueba de alergia cutánea antes del primer uso en cosméticos/perfumes con feromonas, limpieza post-uso de juguetes, no ingerir salvo que el producto sea comestible-safe) — no una consulta médica.

### Criterios de éxito:

#### Verificación automatizada:

- No aplica (entregable es un documento de contenido, no código).

#### Verificación manual:

- [x] La tabla cubre los 76 productos de `productos.json` sin omisiones, agrupados por categoría.
- [x] Cada fila con "Cuidado y uso" corresponde a una categoría marcada como aplicable en D4, o trae una justificación explícita si es una excepción puntual.
- [ ] El usuario recibió la tabla completa y dio su aprobación (total o con ediciones puntuales) antes de que arranque la Fase 4 — sin esta aprobación, la Fase 4 no comienza.

---

## Phase 4: Aplicar contenido aprobado a `productos.json`

### Overview

Escribir a `productos.json` el contenido de la tabla de la Fase 3, ya aprobado/editado por el usuario.

### Dependencias con fases previas

Depende de la aprobación explícita de la tabla de la Fase 3. Depende de la Fase 2 solo en cuanto a que el modal ya sabe renderizar estos campos — esta fase no toca `js/` ni `css/`, solo datos.

### Cambios requeridos:

#### 1. `productos.json` — contenido aprobado

**Archivo**: `js/productos.json` (modificar)
**Cambios**: agregar `descripcion` a los 76 productos, y `medidas`/`recomendacionesSalud` a los que correspondan según la tabla aprobada de la Fase 3. Campos no aplicables se omiten (no se escribe `""` ni `null`), consistente con D7.

**Comportamiento**: sin cambios de código — el modal (Fase 2) ya sabe leer y renderizar (o graciosamente omitir) estos campos.

### Criterios de éxito:

#### Verificación automatizada:

- [x] `productos.json` sigue siendo JSON válido: `node -e "JSON.parse(require('fs').readFileSync('js/productos.json'))"`.
- [x] Todos los productos tienen `descripcion` no vacía: `node -e "const p=JSON.parse(require('fs').readFileSync('js/productos.json')); const f=p.filter(x=>!x.descripcion); if(f.length) throw new Error('sin descripcion: '+f.map(x=>x.id))"`.

#### Verificación manual:

- [ ] Abrir el modal de al menos 2 productos por categoría y confirmar que descripción/medidas/cuidado y uso coinciden con lo aprobado en la tabla de la Fase 3.
- [ ] Confirmar visualmente que ningún modal queda con un bloque vacío o mal espaciado (regla de la Fase 2: campo ausente = nodo no emitido).
- [ ] Un producto con los 3 campos, uno con solo 2, y uno con solo `descripcion` — verificar que los 3 casos se ven correctos en el modal (sin huecos raros).

---

## Phase 5: Investigación y aplicación de precio de mercado en Bogotá

### Overview

Investigar, por tipo de producto (no por SKU exacto), un precio promedio de venta en Bogotá/Colombia, dejar registro en una tabla, y **aplicarlo directo** a `precio` en `productos.json` (D2, revisada) — sin esperar aprobación fila por fila. El registro queda disponible para que el usuario corrija manualmente cualquier precio puntual que no le convenza después de verlo en vivo.

### Dependencias con fases previas

Ninguna dependencia funcional con las fases anteriores — puede ejecutarse en paralelo a las Fases 2-4 si se prefiere, aunque el plan la secuencia después por orden de lectura.

### Cambios requeridos:

#### 1. Tabla de registro de precios (traza, no gate de aprobación)

**Archivo**: `docs/research/2026-08-11-precios-bogota-propuesta.md` (nuevo)

**Comportamiento**: documento con una tabla de 76 filas: `id | título | categoría | precio anterior (COP) | precio aplicado (COP) | diferencia (%) | fuentes/rango observado`. Metodología: búsqueda por tipo de producto genérico comparable en el mercado colombiano (marketplaces y tiendas online de Bogotá del rubro), calculando un promedio o punto medio representativo del rango de precios encontrado — explícitamente no un precio exacto de ESE SKU (la mayoría son productos de dropshipping sin marca rastreable con listado propio). Cuando no se encuentre suficiente evidencia de mercado confiable para un tipo de producto, la fila lo indica explícitamente ("sin evidencia suficiente") y ese producto **conserva su precio actual sin cambios** — no se inventa un número solo para completar la tabla.

#### 2. `productos.json` — precios actualizados

**Archivo**: `js/productos.json` (modificar)
**Cambios**: actualizar el campo `precio` (número entero, COP) de cada producto con el valor "precio aplicado" de la tabla del punto 1, apenas queda calculado — sin paso de revisión intermedio.

**Comportamiento**: sin cambios de código — `main.js`/`carrito.js` ya formatean y suman `precio` genéricamente.

### Criterios de éxito:

#### Verificación automatizada:

- [ ] `productos.json` sigue siendo JSON válido: `node -e "JSON.parse(require('fs').readFileSync('js/productos.json'))"`.
- [ ] Todos los `precio` son números enteros positivos: `node -e "const p=JSON.parse(require('fs').readFileSync('js/productos.json')); const f=p.filter(x=>!Number.isInteger(x.precio)||x.precio<=0); if(f.length) throw new Error('precio invalido: '+f.map(x=>x.id))"`.

#### Verificación manual:

- [ ] La tabla de registro cubre los 76 productos sin omisiones, y cada precio aplicado trae su rango/fuente o la nota explícita "sin evidencia suficiente" (para esos, el precio no cambió).
- [ ] Los precios mostrados en el catálogo y en el modal coinciden con la tabla de registro.
- [ ] Agregar 2-3 productos al carrito y confirmar que el total (`#total` en `carrito.html`) y el mensaje de WhatsApp generado (`comprarCarrito`, `js/carrito.js:166-194`) reflejan los precios nuevos correctamente.

---

## Estrategia de testing

El repo no tiene framework de test configurado (ver `CLAUDE.md`), así que el mix real de esta fase es **~80% verificación manual, ~20% automatizada** — el 20% son las validaciones `node -e`/`node --check` de shape/sintaxis en cada fase (id únicos, JSON válido, `descripcion` no vacía, `precio` entero positivo), que es todo lo que el entorno actual permite automatizar sin agregar tooling nuevo. El resto (comportamiento del modal, accesibilidad, responsive, offline, compatibilidad GitHub Pages) se verifica a mano en navegador, siguiendo los pasos de cada fase más los generales de acá abajo.

### Tests unitarios:

No aplica — no se agrega framework de test en este plan (ver arriba). La verificación automatizada de cada fase se limita a validaciones de shape/sintaxis vía `node -e`/`node --check`, ya listadas en los criterios de éxito de cada fase.

### Pasos de testing manual:

1. Servir el sitio con `npx serve .` (obligatorio para que `fetch` y el Service Worker funcionen — `file://` falla en algunos navegadores).
2. Recorrer las 7 categorías del menú lateral, abriendo el modal de al menos un producto por categoría.
3. Verificar los 3 métodos de cierre del modal (X, ESC, click fuera).
4. Agregar al carrito desde el modal y desde la card directamente, en distintos productos, y confirmar que el carrito (`carrito.html`) y el número (`#numerito`) quedan consistentes en ambos casos.
5. Probar en viewport mobile (≤600px) el comportamiento de bottom sheet y que el CTA no quede recortado.
6. Probar la categoría "PROMOCIONES!" después de la Fase 1, agregando al carrito tanto la copia promocional como el producto original de su categoría real, confirmando que quedan como líneas separadas.
7. Simular offline (DevTools → Network → Offline) tras un primer load, recargar, y confirmar que el catálogo y el modal siguen funcionando desde caché.
8. **Compatibilidad GitHub Pages (D11)**: confirmar que ningún archivo nuevo usa rutas absolutas (`grep`/búsqueda de `src="/` o `href="/` sin el `.` relativo), y que los nombres de archivo nuevos (`js/detalle.js`, cualquier imagen nueva si aplicara) coinciden en mayúsculas/minúsculas exactas entre el nombre en disco y cada referencia en el código — un mismatch de casing no falla en Windows local pero sí en el filesystem case-sensitive de GitHub Pages. Si el repositorio se publica como *project page* (`usuario.github.io/CatalogoStore/`), confirmar igual que todo sigue resolviendo bien porque las rutas ya son relativas al documento, no absolutas al dominio.

### Edge cases a testear manualmente:

- Producto sin `medidas` ni `recomendacionesSalud` (solo `descripcion`) — el modal no debe dejar huecos.
- Título de producto largo (ej. "Vibrador manejo app larga distancia") — no debe truncarse dentro del modal, aunque sí en la card.
- Descripción larga cercana al límite de 450 caracteres — no debe forzar scroll horizontal ni desbordar el panel en desktop.
- Doble click rápido en "Agregar al carrito" dentro del modal — la cantidad debe incrementar correctamente, no duplicar por evento fantasma.
- Un producto cuyo precio quedó "sin evidencia suficiente" en la Fase 5 — confirmar que conserva el precio anterior y no aparece como `undefined`/`NaN` en ningún lado.

## Consideraciones de performance

- El modal reutiliza el `src` de imagen que la card ya cargó — el navegador sirve desde caché de imagen/Service Worker, sin request adicional.
- `js/detalle.js` es un archivo nuevo pequeño (solo orquestación del `<dialog>`), agregado explícitamente a `urlsToCache` en `js/sw.js` para no quedar fuera del precache offline (ver Fase 2, punto 4).
- Las animaciones del modal solo tocan `opacity`/`transform` (compositor-friendly, sin repintado de layout), con `prefers-reduced-motion` cubierto reduciendo la duración a `.01ms` en vez de desactivar la animación (evita que `animationend` nunca dispare y el modal quede abierto).
- Sin llamadas de red nuevas: el modal lee del array `productos` ya obtenido por el único `fetch` existente en `js/main.js:3-8`.

## Referencias

- Research doc de diseño (UX Spec completo + alternativas descartadas): `docs/research/detalle-producto-y-precios-bogota-uiux.md`
- Modelo de datos actual: `js/productos.json:1-765`
- Renderizado de cards: `js/main.js:23-44`
- Lógica de carrito: `js/carrito.js`
- Precedente de overlay/toggle de clase: `<aside>` mobile, `css/main.css:743-761`, `js/menu.js`
- Precedente de confirm dialog: SweetAlert2 en `vaciarCarrito`, `js/carrito.js:140-156`
- Precedente de tinte de marca: `.estado-icono-exito`, `css/main.css:442-449`
