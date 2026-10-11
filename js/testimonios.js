// ADVERTENCIA: estas reseñas son TEMPORALMENTE FICTICIAS mientras se consiguen
// clientes y calificaciones reales. Para reemplazarlas, edita SOLO
// ./js/testimonios.json — no hace falta tocar este archivo ni el HTML.
fetch("./js/testimonios.json")
    .then(r => r.json())
    .then(renderTestimonios)
    .catch(err => console.error("No se pudieron cargar los testimonios:", err));

function renderTestimonios(testimonios) {
    const contenedor = document.querySelector("#contenedor-testimonios");
    if (!contenedor) return;

    contenedor.innerHTML = "";

    testimonios.forEach(t => {
        const estrellas = "★".repeat(t.calificacion) + "☆".repeat(5 - t.calificacion);
        const div = document.createElement("div");
        div.className = "bg-surface rounded-xl shadow-card p-5 flex flex-col gap-3";
        div.innerHTML = `
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-plum text-surface flex items-center justify-center font-bold text-sm">${iniciales(t.nombre)}</div>
                <div>
                    <p class="font-bold text-sm text-charcoal">${t.nombre}</p>
                    <p class="text-xs text-on-surface-variant">${t.fecha}</p>
                </div>
            </div>
            <p class="text-amber-500 text-sm" aria-label="${t.calificacion} de 5 estrellas">${estrellas}</p>
            <p class="text-sm text-on-surface-variant leading-relaxed">${t.texto}</p>
        `;
        contenedor.append(div);
    });
}

function iniciales(nombre) {
    return nombre.split(" ").map(p => p[0]).slice(0, 2).join("").toUpperCase();
}
