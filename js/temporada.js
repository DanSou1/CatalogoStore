// Controla qué diseño de temporada se muestra en el sitio.
// "auto"      -> octubre activa Halloween automáticamente, el resto del año es el diseño normal.
// "halloween" -> fuerza el diseño de Halloween sin importar la fecha.
// "normal"    -> fuerza el diseño normal sin importar la fecha.
const TEMPORADA_FORZADA = "auto";

function temporadaActiva() {
    if (TEMPORADA_FORZADA === "halloween") return "halloween";
    if (TEMPORADA_FORZADA === "normal") return "normal";
    const mes = new Date().getMonth(); // 0 = enero ... 9 = octubre
    return mes === 9 ? "halloween" : "normal";
}

// Convención: agregar el sufijo ".halloween" al id del producto en productos.json
// (ej: "disfraz-gata.halloween") para que se destaque mientras el tema esté activo.
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

if (temporadaActiva() === "halloween") {
    document.documentElement.classList.add("tema-halloween");
}

document.addEventListener("DOMContentLoaded", () => {
    if (temporadaActiva() !== "halloween") return;

    document.title = "🎃 " + document.title;

    const heroHeadline = document.querySelector("#hero-headline");
    const heroSubcopy = document.querySelector("#hero-subcopy");
    if (heroHeadline) heroHeadline.innerText = "Edición especial de Halloween 🎃";
    if (heroSubcopy) heroSubcopy.innerText = "Disfraces y sorpresas de temporada, con envío discreto y atención directa por WhatsApp.";
});
