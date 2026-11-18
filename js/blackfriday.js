// Black Friday XperienceLove — se activa y se apaga SOLO por fecha (como temporada.js).
// Fuera de las fechas, la tienda muestra los precios normales de productos.json.
//
// "auto"     -> activo solo entre INICIO y FIN (hora Bogotá).
// "activo"   -> fuerza la promo encendida (solo para vistas previas; NO publicar así).
// "apagado"  -> fuerza la promo apagada.
const BLACK_FRIDAY_FORZADO = "auto";

const BLACK_FRIDAY = {
    inicio: new Date("2026-11-27T00:00:00-05:00"),
    fin: new Date("2026-11-30T23:59:59-05:00"),
    textoCierre: "lunes 30 de noviembre a las 11:59 p. m.",
    // Regalo para toda compra hecha en la página durante la promo.
    // EDITA ESTE TEXTO cuando Daniel defina el regalo (sale en el carrito y en el correo del pedido).
    regalo: "Un sachet lubricante de regalo",
    // Precio de promoción por id de producto (15 % sobre el precio de hoy en productos.json).
    // El precio normal SIEMPRE se toma de productos.json; nunca se infla.
    precios: {
        "cosmeticos-10": 33900, // Feromonas sin olor para hombre  ($39.900)
        "bondage-10": 107100,   // Sling arnés de posiciones       ($126.000)
        "juego-15": 57700,      // Jenga Picante                   ($67.900)
        "lubricante-17": 33100, // Lubricante lychee sensación caliente ($38.900)
    },
};

function blackFridayActivo(fecha = new Date()) {
    if (BLACK_FRIDAY_FORZADO === "activo") return true;
    if (BLACK_FRIDAY_FORZADO === "apagado") return false;
    return fecha >= BLACK_FRIDAY.inicio && fecha <= BLACK_FRIDAY.fin;
}

function esProductoBlackFriday(producto) {
    return Object.prototype.hasOwnProperty.call(BLACK_FRIDAY.precios, producto.id);
}

// Ajusta el precio de UN producto (catálogo o carrito) según la fecha.
// Guarda el precio normal en `precioBase` para poder volver a él cuando termine la promo.
function ajustarPrecioBlackFriday(producto) {
    if (!esProductoBlackFriday(producto)) return producto;
    const base = producto.precioBase ?? (producto.precioAnterior > producto.precio ? producto.precioAnterior : producto.precio);
    const promo = BLACK_FRIDAY.precios[producto.id];
    producto.precioBase = base;
    if (blackFridayActivo() && promo < base) {
        producto.precio = promo;
        producto.precioAnterior = base;
    } else {
        producto.precio = base;
        delete producto.precioAnterior;
    }
    return producto;
}

// Para la lista de productos.json: aplica precios según la fecha.
function aplicarBlackFriday(lista) {
    lista.forEach(ajustarPrecioBlackFriday);
    return lista;
}

// Mientras dure la promo, sus productos van de primeros (antes que los kits de temporada).
function ordenarBlackFriday(lista) {
    if (!blackFridayActivo()) return lista;
    return [...lista].sort((a, b) => Number(esProductoBlackFriday(b)) - Number(esProductoBlackFriday(a)));
}

(function marcarBlackFriday() {
    if (blackFridayActivo()) document.documentElement.classList.add("promo-blackfriday");
})();

// Textos del inicio (corre después de temporada.js, así que reemplaza el titular de Navidad mientras dure la promo).
document.addEventListener("DOMContentLoaded", () => {
    if (!blackFridayActivo()) return;

    const heroHeadline = document.querySelector("#hero-headline");
    const heroSubcopy = document.querySelector("#hero-subcopy");
    if (heroHeadline) heroHeadline.innerText = "Black Friday: 15 % en 4 favoritos 🖤";
    if (heroSubcopy) heroSubcopy.innerText = `Hasta el ${BLACK_FRIDAY.textoCierre} Además, toda compra por la página lleva ${BLACK_FRIDAY.regalo.toLowerCase()}.`;

    const barraTexto = document.querySelector("#barra-promo-texto");
    if (barraTexto) barraTexto.innerText = `Black Friday: 15 % + ${BLACK_FRIDAY.regalo.toLowerCase()} · termina en`;

    const regaloCarrito = document.querySelector("#datos-envio-regalo");
    const regaloTexto = document.querySelector("#datos-envio-regalo-texto");
    if (regaloCarrito && regaloTexto) {
        regaloTexto.innerText = BLACK_FRIDAY.regalo;
        regaloCarrito.classList.remove("disabled");
    }
});
