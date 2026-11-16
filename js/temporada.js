// Controla qué diseño de temporada se muestra en el sitio.
// "auto"      -> octubre = Halloween; del 15 de noviembre al 6 de enero = Navidad; el resto del año, diseño normal.
// "halloween" -> fuerza el diseño de Halloween sin importar la fecha.
// "navidad"   -> fuerza el diseño de Navidad sin importar la fecha.
// "normal"    -> fuerza el diseño normal sin importar la fecha.
const TEMPORADA_FORZADA = "auto";

// Estilo visual de la Navidad: "burdeos" | "aguinaldo" | "neon".
// Cada uno es un bloque html.navidad-<estilo> en css/main.css.
const ESTILO_NAVIDAD = "aguinaldo";

// Textos y emoji de cada temporada (badge en las tarjetas, botón Agregar, hero).
const TEMPORADAS = {
    halloween: {
        emoji: "🎃",
        badge: "🎃 Halloween",
        titular: "Edición especial de Halloween 🎃",
        subtitulo: "Disfraces y sorpresas de temporada, con envío discreto y atención directa por WhatsApp.",
    },
    navidad: {
        emoji: "🎁",
        badge: "🎁 Navidad",
        titular: "Regalos que no van debajo del árbol 🎁",
        subtitulo: "Kits de Navidad para parejas, listos para regalar. Empaque y envío discretos, atención directa por WhatsApp.",
    },
};

function temporadaActiva() {
    if (TEMPORADA_FORZADA !== "auto") return TEMPORADA_FORZADA;
    const hoy = new Date();
    const mes = hoy.getMonth(); // 0 = enero ... 9 = octubre, 10 = noviembre, 11 = diciembre
    const dia = hoy.getDate();
    if (mes === 9) return "halloween";
    if ((mes === 10 && dia >= 15) || mes === 11 || (mes === 0 && dia <= 6)) return "navidad";
    return "normal";
}

function datosTemporada() {
    return TEMPORADAS[temporadaActiva()] || null;
}

// Texto del botón Agregar según la temporada (ej. "Agregar 🎁").
function textoBotonAgregar() {
    const datos = datosTemporada();
    return datos ? `Agregar ${datos.emoji}` : "Agregar";
}

// Convención: agregar el sufijo ".<temporada>" al id del producto en productos.json
// (ej: "promociones-01.navidad") para que se destaque mientras el tema esté activo.
function esProductoDeTemporada(producto, temporada) {
    return producto.id.toLowerCase().endsWith("." + temporada);
}

// Reordena dejando primero los productos etiquetados para la temporada activa.
// Si la temporada activa es "normal", no reordena nada.
function ordenarPorTemporada(lista) {
    const temporada = temporadaActiva();
    if (temporada === "normal") return lista;
    return [...lista].sort((a, b) => Number(esProductoDeTemporada(b, temporada)) - Number(esProductoDeTemporada(a, temporada)));
}

(function aplicarClaseTemporada() {
    const temporada = temporadaActiva();
    if (temporada === "normal") return;
    document.documentElement.classList.add("tema-" + temporada);
    if (temporada === "navidad") document.documentElement.classList.add("navidad-" + ESTILO_NAVIDAD);
})();

document.addEventListener("DOMContentLoaded", () => {
    const temporada = temporadaActiva();
    const datos = datosTemporada();
    if (!datos) return;

    document.title = datos.emoji + " " + document.title;

    const heroHeadline = document.querySelector("#hero-headline");
    const heroSubcopy = document.querySelector("#hero-subcopy");
    if (heroHeadline) heroHeadline.innerText = datos.titular;
    if (heroSubcopy) heroSubcopy.innerText = datos.subtitulo;

    if (temporada === "halloween") mostrarAnimacionBienvenida("murcielago-halloween", ["🦇"], 3);
    if (temporada === "navidad") mostrarNieve();
});

// Un par de murciélagos cruzan la pantalla al cargar la página, como bienvenida.
// Puramente decorativo: no bloquea clics y se autodestruye al terminar la animación.
function mostrarAnimacionBienvenida(clase, emojis, cantidad) {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const duracionMs = 3200;
    for (let i = 0; i < cantidad; i++) {
        const retrasoMs = i * 400;
        const el = document.createElement("span");
        el.className = clase;
        el.textContent = emojis[i % emojis.length];
        el.style.top = `${10 + Math.random() * 50}%`;
        el.style.animationDelay = `${retrasoMs / 1000}s`;
        el.style.fontSize = `${3 + Math.random() * 1.5}rem`;
        document.body.appendChild(el);
        // No depender solo de "animationend" (puede no dispararse si la pestaña
        // no está en foco/visible): un setTimeout como respaldo garantiza la limpieza.
        el.addEventListener("animationend", () => el.remove());
        setTimeout(() => el.remove(), retrasoMs + duracionMs + 200);
    }
}

// Unos copos caen suavemente al cargar la página (una sola vez, ~6 s) y desaparecen.
// Decorativo: no bloquea clics y respeta "reducir movimiento".
function mostrarNieve() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const cantidad = window.innerWidth < 600 ? 14 : 24;
    for (let i = 0; i < cantidad; i++) {
        const copo = document.createElement("span");
        copo.className = "copo-navidad";
        copo.textContent = "❄";
        const duracionS = 4 + Math.random() * 3;
        const retrasoS = Math.random() * 1.8;
        copo.style.left = `${Math.random() * 100}vw`;
        copo.style.fontSize = `${0.6 + Math.random() * 0.9}rem`;
        copo.style.animationDuration = `${duracionS}s`;
        copo.style.animationDelay = `${retrasoS}s`;
        document.body.appendChild(copo);
        copo.addEventListener("animationend", () => copo.remove());
        setTimeout(() => copo.remove(), (duracionS + retrasoS) * 1000 + 300);
    }
}
