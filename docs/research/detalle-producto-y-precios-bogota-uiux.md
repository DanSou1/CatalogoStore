---
date: 2026-08-11
git_commit: ff0eb133a1a3cb0d4a7a608957d2285a137c8735
branch: main
topic: "UI/UX review — botón 'Ver más información' en la card de producto + modal de detalle de producto"
tags: [research, uiux, design-review, catalogo, modal, accesibilidad, vanilla-js]
status: complete
last_updated: 2026-08-11
plan: docs/plans/2026-08-11-detalle-producto-y-precios-bogota.md
---

# Research UI/UX: Detalle de producto (modal) + trigger en la card

**Fecha**: 2026-08-11
**Git Commit**: ff0eb133a1a3cb0d4a7a608957d2285a137c8735
**Rama**: main
**Plan compañero**: `docs/plans/2026-08-11-detalle-producto-y-precios-bogota.md`

## Contexto

Documento compañero del review de UI/UX ejecutado sobre la Fase 2 del plan (UI: botón "Ver más información" + modal de detalle con "Agregar al carrito"). El review cubrió dos componentes: la card de producto existente (modo híbrido — se audita el delta y se diseña lo que se agrega) y el modal de detalle (modo diseño — superficie nueva).

Este documento **no duplica** el UX Spec que quedó inline en el plan. Preserva lo que no entró: las alternativas descartadas con su rationale, los hallazgos crudos del codebase relevados durante el review, las heurísticas evaluadas que no se aplicaron y los pendientes detectados fuera de alcance. El plan es suficiente para implementar sin abrir este archivo.

**Stack del review**: sitio estático vanilla HTML/CSS/JS, sin build ni framework ni package manager. Iconografía Material Symbols vía CDN, toasts con Toastify, diálogos de confirmación con SweetAlert2.

## Decisiones UX globales

Aprobadas por el usuario antes del loop por componente. Copiadas acá como referencia; el rationale extendido es propio de este documento.

1. **Sin paleta nueva** — el modal reusa las variables ya definidas en `css/main.css:1-40` (`--clr-*`, `--radius-*`, `--shadow-*`). *Rationale extendido*: el proyecto ya tiene un sistema de tokens coherente y completo (paleta plum/charcoal, cinco escalones de radio, dos sombras). Cualquier valor nuevo introducido para una sola superficie se convierte en deuda inmediata en un proyecto sin build ni linter que la detecte.
2. **Tres vías de cierre** — botón X, tecla ESC, click fuera del panel. *Rationale extendido*: es el contrato de cierre que el usuario ya conoce del `<aside>` mobile (click fuera) y de SweetAlert2 (ESC), ambos presentes hoy en el sitio. No se inventa un contrato nuevo.
3. **Toast reusado, no clonado** — el toast "Producto agregado" del CTA del modal usa exactamente el mismo estilo Toastify de la card: gradiente `#832062 → #1B1A1A`, `border-radius: 2rem`, `text-transform: uppercase`, `font-size: .75rem` (`js/main.js:87-105`). *Rationale extendido*: el usuario debe leer "agregué al carrito" como un único evento del sistema, no como dos features distintas según desde dónde lo dispare.

## Componente 1 — Card de producto (modo híbrido)

### Opciones consideradas

**Opción A — acción de texto apilada bajo el precio** (elegida). Ícono `info` de 16px + etiqueta "Ver más información", sin cromo de botón, con subrayado sutil, en blanco al 88% sobre el fondo plum de la card. Se activa vía `data-id` + delegación de evento en `#contenedor-productos`.

**Opción B — fila de dos acciones con trigger circular ícono-only** (descartada). "Agregar" y un botón circular con ícono `info` compartiendo una fila horizontal al pie de la card.

### Rationale de descarte de la Opción B

Tres razones concretas, en orden de peso:

1. **El brief pedía una etiqueta legible.** Un trigger ícono-only deja el significado únicamente en el `aria-label`, lo que lo vuelve adivinable para el usuario vidente. En un catálogo donde el contenido enriquecido (medidas, cuidado y uso) es justamente el valor que se está agregando, esconder la puerta de entrada detrás de un glifo contradice el objetivo de la fase.
2. **No hay ancho real disponible.** En el grid mobile de 2 columnas a 375px de viewport, el ancho de contenido medido por card es de ~131px. La etiqueta "Agregar" en uppercase con `letter-spacing: .05em` (`css/main.css:383-396`) ya consume casi todo ese ancho. Un trigger circular en la misma fila no tiene margen de layout — se resolvería recortando el CTA principal.
3. **Diluye la jerarquía de conversión.** Dos controles de peso visual comparable en la misma fila comunican que hay dos acciones equivalentes. "Agregar" es el único CTA de conversión de la card; "Ver más información" es una acción exploratoria secundaria. Apilarla como acción de texto sin cromo preserva esa diferencia sin necesidad de un tratamiento defensivo.

### Hallazgos de código que motivaron ajustes

- **Colisión de identificador.** Hoy el id del producto viaja como atributo HTML `id` en el botón de agregar (`js/main.js:36`), y `agregarAlCarrito` lo lee vía `e.currentTarget.id` (`js/main.js:107`). Un segundo control dentro de la misma card no puede reusar `id` sin duplicar identificadores en el documento. Decisión: el trigger nuevo usa `data-id`, y `agregarAlCarrito` pasa a leer `dataset.id || id` — retrocompatible, sin tocar el markup existente del botón "Agregar" en la misma fase.
- **Cero reglas de foco visible en el proyecto.** Una búsqueda de `:focus` y `:focus-visible` sobre `css/main.css` completo devuelve cero coincidencias. El sitio depende enteramente del anillo por defecto del navegador, que sobre el fondo plum saturado de la card tiene contraste marginal. Decisión: se agregan reglas `:focus-visible` explícitas a **ambos** botones de la card (el nuevo y el existente), no solo al nuevo — el delta de la fase toca esa fila y dejar la mitad sin foco visible produce una inconsistencia peor que la ausencia total.

### Alternativas de wiring evaluadas

Se evaluó mantener el patrón actual de re-attach de listeners (`actualizarBotonesAgregar()`, `js/main.js:66-72`, que re-consulta el DOM y vuelve a suscribir en cada render) también para el trigger nuevo. Se descartó a favor de delegación en `#contenedor-productos`: el patrón de re-attach ya acumula suscripciones sobre nodos recreados en cada cambio de categoría, y replicarlo duplicaría ese costo. La delegación no requiere refactorizar el patrón existente — convive con él.

## Componente 2 — Modal de detalle (modo diseño)

### Arquitectura: `<dialog>` nativo vs. `div` + clase

**Elegida**: `<dialog>` nativo con `showModal()`.

**Descartada**: calcar el patrón del `<aside>` mobile existente — un `div` con clase toggleada y `box-shadow: 0 0 0 100vmax rgba(0,0,0,.75)` como scrim (`css/main.css:750`).

Rationale de descarte:

1. **El scrim por `box-shadow` no escala a un panel centrado.** Esa técnica ancla el oscurecimiento al box del propio elemento. Funciona para un panel lateral anclado al borde que ocupa el alto completo; se rompe con un panel centrado que hace scroll interno, porque la sombra sigue al box y no cubre el viewport de forma estable.
2. **Reimplementar la mecánica de modal a mano se rompe en silencio.** Focus trap, ESC, inertización del contenido de fondo y retorno de foco al trigger son cuatro comportamientos que, cuando fallan, no producen ningún error visible — solo usuarios de teclado y lector de pantalla atrapados o perdidos. En un proyecto sin tests, ese tipo de regresión no se detecta.
3. **`<dialog>` entrega los cuatro gratis vía la plataforma.** No hay biblioteca que agregar a un sitio que ya carga tres CDNs.

**Trade-off aceptado y resuelto**: `<dialog>` abierto con `showModal()` se pinta en el *top layer* del navegador, por encima de cualquier `z-index` del documento. Un toast de Toastify montado en `body` (comportamiento por defecto) quedaría detrás del scrim y sería invisible. Resolución: el toast disparado desde el CTA del modal se monta dentro del propio `<dialog>` usando la opción `selector` de Toastify. Se evaluó como alternativa cerrar el modal antes de disparar el toast — descartado porque elimina el escenario de "agregar varias unidades sin salir del detalle" y hace que la acción se sienta como un submit que expulsa al usuario.

### Dirección visual del bloque de recomendaciones

**Opción A — callout teñido de marca** (elegida): fondo `rgba(131,32,98,.06)`, `border-left: 3px solid var(--clr-plum)`, ícono `health_and_safety`, título "Cuidado y uso".

**Opción B — callout neutro gris** (descartada): fondo `--clr-surface-container-low` (`#f3f3f3`, `css/main.css:13`), sin borde de color. Descartada por dos motivos: (a) se aplanaba contra el resto del contenido del modal, perdiendo el énfasis que el brief pedía explícitamente para este bloque — el mismo gris ya se usa como fondo de superficie neutra en la página del carrito (`css/main.css:350`, `css/main.css:517`), así que no lee como bloque destacado; (b) el ícono neutro candidato para ese tratamiento (`spa`) ya está tomado semánticamente por la categoría "Cosméticos" en el nav lateral (`index.html:48`), y reusarlo con otro significado en la misma sesión de navegación produce ambigüedad.

**Opción C — tratamiento de advertencia en rojo** (descartada de plano, no llegó a presentarse como opción formal): usar `--clr-error` (`#ba1a1a`, `css/main.css:22`) o su variante oscura. Dos razones: ese color está reservado en el proyecto para acciones destructivas — es el hover del botón de eliminar del carrito (`css/main.css:563-565`) —, y un callout rojo se lee como advertencia médica formal o como error del sistema, no como nota de cuidado de producto. No es el tono correcto para retail.

### Copy

El campo interno del JSON se llama `recomendacionesSalud`, pero la etiqueta de UI es **"Cuidado y uso"**. La decisión es deliberada: "salud" arrastra un registro clínico que no corresponde al contexto (un catálogo de productos íntimos), sube innecesariamente la temperatura emocional del bloque y sugiere una autoridad médica que el sitio no tiene. "Cuidado y uso" comunica lo mismo en registro de producto. El nombre del campo interno no se cambia en esta fase para no tocar el contrato de `productos.json` fuera de las fases que ya lo modifican.

### Layout

Split 42/58 (imagen 4:5 con `object-fit: contain` | contenido) centrado en desktop, `max-width: min(880px, ...)`. Bottom-sheet full-width en mobile con handle visual y `border-radius` solo en las esquinas superiores.

El breakpoint mobile es `≤600px` — el mismo que ya usa el `<aside>` (`css/main.css:735`). Se evaluó introducir un breakpoint propio más alto para el modal, dado que un split de dos columnas se comprime antes que un nav lateral. Se descartó: agregar un segundo breakpoint a una hoja de estilos que hoy tiene uno solo obliga a razonar sobre dos puntos de quiebre en cada cambio futuro, y la ganancia era marginal frente a resolver la compresión con el propio split.

### Reglas de campos opcionales

`medidas` y `recomendacionesSalud` pueden faltar. La regla de composición elegida: el separador (`border-top`) vive en el wrapper `.modal-fichas`, **no** en un `<hr>` suelto entre bloques. Consecuencia: si ningún campo opcional existe, el wrapper entero no se emite y no queda ni regla huérfana ni hueco vertical en el layout. Se descartó la alternativa de emitir los bloques con un `<hr>` entre ellos y ocultarlos con CSS (`:empty`, `:last-child`), porque exige que el markup emita nodos vacíos y hace el CSS dependiente del orden exacto de los hijos.

Mismo criterio para `descripcion` ausente: no se emite el `<p>`, **y** se remueve el atributo `aria-describedby` del `<dialog>` en vez de dejarlo apuntando a un id inexistente — un `aria-describedby` colgado es peor que no tenerlo, porque el lector de pantalla anuncia el diálogo sin descripción y sin señal de que faltó algo.

### Accesibilidad

- **`role="dialog"` y `aria-modal="true"` no se declaran a mano.** Ambos son implícitos de un `<dialog>` abierto con `showModal()`. Declararlos explícitamente es redundante según ARIA APG y crea el riesgo de que queden desincronizados si en el futuro alguien cambia `showModal()` por `show()`.
- **Foco inicial en el botón de cerrar**, no en "Agregar al carrito". Rationale: si el foco inicial cae sobre el CTA, un Enter reflejo del usuario (habitual justo después de abrir algo con Enter) agrega el producto al carrito sin intención. El botón de cerrar es la acción segura por defecto.
- **Retorno de foco al trigger**: delegado íntegramente al navegador vía el comportamiento nativo de `<dialog>`. No se implementa a mano.
- **Hallazgo de sistema que aplica a todo el modal**: `--clr-outline` (`#7d7577`, `css/main.css:18`) da 4.48:1 sobre blanco. Pasa el mínimo de 3:1 exigido para bordes e íconos, pero **falla** el 4.5:1 de texto normal. Hoy se usa como color de texto en al menos dos lugares del sitio (`css/main.css:439`, `css/main.css:552`). Regla adoptada para el modal: todo texto secundario usa `--clr-on-surface-variant` (`#4c4547`, 8.9:1 sobre blanco, `css/main.css:17`), nunca `--clr-outline`. Los usos preexistentes fuera del modal quedan fuera de alcance de esta fase (ver pendientes).

### Animación

Solo `opacity` y `transform` — las dos propiedades que el compositor puede animar sin recalcular layout ni repintar.

Dos detalles de implementación que surgieron del review y que no son obvios:

- **`@keyframes` separados para entrada y salida.** El cierre de un `<dialog>` no es un toggle de clase: hay que esperar el evento `animationend` antes de llamar a `close()`, porque `close()` remueve el elemento del top layer de inmediato y la animación de salida nunca se vería.
- **`prefers-reduced-motion` se cubre con `animation-duration: .01ms`, no con `animation: none`.** Con `animation: none` el evento `animationend` **nunca se dispara**, el handler de cierre nunca corre y el modal queda abierto para siempre para todo usuario con motion reducido activado. Es una falla total de la funcionalidad disfrazada de mejora de accesibilidad.

## Heurísticas evaluadas y no aplicadas

- **Deep-link / historial del modal** (abrir el detalle vía URL, cerrar con el botón atrás del navegador). Aporta valor real de compartibilidad en un catálogo, pero exige introducir routing en un sitio de dos páginas sin router y sin build. Fuera de alcance de esta fase; queda registrado como candidato futuro.
- **Skeleton / estado de carga en el modal.** Descartado: los datos del producto ya están en memoria (`productos`, cargado una sola vez en `js/main.js:1-8`) al momento de abrir el modal. No hay latencia que cubrir; un skeleton sería teatro.
- **Galería multi-imagen en el modal.** El esquema actual de `productos.json` tiene un único campo `imagen`. Diseñar un carrusel para un array que no existe agrega complejidad especulativa.
- **Botón "Ver más información" también en la página del carrito.** `carrito.js` no re-consulta `productos.json` y trabaja sobre el snapshot en `localStorage`, que no contiene los campos nuevos. Aplicarlo ahí exigiría cambiar el modelo de datos del carrito. Fuera de alcance.

## Pendientes detectados fuera de alcance

Encontrados durante el review, no implementados en esta fase. Prioridad baja/media.

| Hallazgo | Ubicación | Prioridad | Nota |
| --- | --- | --- | --- |
| Precio sin separador de miles (`$42500` en vez de `$42.500`) | `js/main.js:35` | Media | Afecta legibilidad de precios en COP. El modal hereda el mismo formato para no divergir de la card; corregir ambos a la vez cuando se aborde. |
| `alt="${producto.titulo}"` sin escapar | `js/main.js:32` | Baja | Rompe el atributo si un título contiene comillas dobles. Ninguno lo hace hoy. |
| Imágenes sin `loading="lazy"` | `js/main.js:32` | Baja | El grid renderiza el catálogo completo en el filtro "Todos los productos". |
| `--clr-outline` usado como color de texto (4.48:1, falla 4.5:1) | `css/main.css:439`, `css/main.css:552` | Media | La regla ya se aplica al modal; los usos preexistentes quedan pendientes. |
| Ausencia total de reglas `:focus-visible` en el sitio | `css/main.css` (global) | Media | Esta fase las agrega solo a los dos botones de la card. Nav lateral, botones de categoría y controles del carrito siguen sin cobertura. |

## Referencias de código

- `js/main.js:31-38` — template de la card de producto; punto de inserción del trigger nuevo.
- `js/main.js:36` — botón "Agregar" con el id del producto como atributo HTML `id`.
- `js/main.js:66-72` — `actualizarBotonesAgregar()`, patrón de re-attach de listeners tras cada render.
- `js/main.js:85-121` — `agregarAlCarrito`, incluye la configuración Toastify que el modal reusa (`:87-105`) y la lectura del id (`:107`).
- `css/main.css:1-40` — bloque de custom properties: paleta, radios, sombras, espaciados.
- `css/main.css:383-400` — `.producto-agregar`, el CTA existente de la card.
- `css/main.css:548-565` — `.carrito-producto-eliminar`, único consumidor de `--clr-error`.
- `css/main.css:735` — apertura del media query mobile (`max-width: 600px`), breakpoint compartido con el modal.
- `css/main.css:750` — scrim del `<aside>` vía `box-shadow: 0 0 0 100vmax`, patrón evaluado y descartado.
- `index.html:45-66` — botones de categoría del nav lateral, fuente de los íconos Material Symbols ya en uso.

## Referencias externas

- ARIA Authoring Practices Guide — Dialog (Modal) Pattern: <https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/>
- MDN — `<dialog>` y el top layer: <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog>
- WCAG 2.2 SC 1.4.3 Contrast (Minimum): <https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html>
- WCAG 2.2 SC 1.4.11 Non-text Contrast: <https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html>
- Toastify — opción `selector` para montar el toast en un contenedor propio: <https://github.com/apvarun/toastify-js>

## Preguntas abiertas

- El deep-link del modal (compartir la URL de un producto por WhatsApp) tiene sinergia directa con el modelo de negocio del sitio, que ya es WhatsApp-first. Vale evaluarlo como fase propia una vez que el contenido enriquecido exista.
- Si en el futuro se agrega galería multi-imagen, el split 42/58 del modal es el lugar natural, pero requiere decidir antes el esquema (`imagen` string vs. `imagenes` array) y su compatibilidad con el snapshot del carrito en `localStorage`.
