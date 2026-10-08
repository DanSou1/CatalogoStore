function toggleCartDrawer(mostrar) {
    const drawer = document.querySelector("#carrito-drawer");
    const backdrop = document.querySelector("#carrito-drawer-backdrop");
    drawer.classList.toggle("translate-x-full", !mostrar);
    backdrop.classList.toggle("disabled", !mostrar);
}

function renderDrawer() {
    const productosEnCarrito = leerCarrito();
    const lista = document.querySelector("#carrito-drawer-productos");
    const vacio = document.querySelector("#carrito-drawer-vacio");
    const resumen = document.querySelector("#carrito-drawer-resumen");

    lista.innerHTML = "";

    if (!productosEnCarrito.length) {
        vacio.classList.remove("disabled");
        resumen.classList.add("disabled");
        return;
    }

    vacio.classList.add("disabled");
    resumen.classList.remove("disabled");

    productosEnCarrito.forEach(producto => {
        const div = document.createElement("div");
        div.className = "flex gap-3 bg-surface-container-low p-3 rounded-xl items-center";
        div.innerHTML = `
            <img class="w-14 h-14 object-cover rounded-lg shrink-0" src="${producto.imagen}" alt="${producto.titulo}">
            <div class="flex-1 min-w-0">
                <p class="font-bold text-xs text-charcoal truncate">${producto.titulo}</p>
                <div class="flex items-center justify-between mt-1">
                    <div class="flex items-center gap-1 bg-surface rounded-full px-1">
                        <button class="w-6 h-6 text-xs" data-accion="restar" data-id="${producto.id}" aria-label="Restar">-</button>
                        <span class="text-xs font-bold px-1">${producto.cantidad}</span>
                        <button class="w-6 h-6 text-xs" data-accion="sumar" data-id="${producto.id}" aria-label="Sumar">+</button>
                    </div>
                    <span class="font-bold text-xs text-plum">$${producto.precio * producto.cantidad}</span>
                </div>
            </div>
            <button class="text-on-surface-variant hover:text-error" data-accion="eliminar" data-id="${producto.id}" aria-label="Eliminar">
                <span class="material-symbols-outlined text-base">delete</span>
            </button>
        `;
        lista.append(div);
    });

    document.querySelector("#carrito-drawer-total").innerText = `$${calcularTotalPrecio(productosEnCarrito)}`;
    lista.querySelectorAll("[data-accion]").forEach(boton => boton.addEventListener("click", manejarAccionDrawer));
}

function manejarAccionDrawer(e) {
    const accion = e.currentTarget.dataset.accion;
    const id = e.currentTarget.dataset.id;
    const productosEnCarrito = leerCarrito();

    if (accion === "sumar") incrementarProducto(productosEnCarrito, id);
    if (accion === "restar") decrementarProducto(productosEnCarrito, id);
    if (accion === "eliminar") quitarProducto(productosEnCarrito, id);

    actualizarNumerito();
    document.dispatchEvent(new CustomEvent("carrito:actualizado"));
}

document.querySelector("#abrir-carrito-flotante")?.addEventListener("click", () => toggleCartDrawer(true));
document.querySelector("#abrir-carrito-icono")?.addEventListener("click", () => toggleCartDrawer(true));
document.querySelector("#cerrar-carrito-drawer")?.addEventListener("click", () => toggleCartDrawer(false));
document.querySelector("#carrito-drawer-backdrop")?.addEventListener("click", () => toggleCartDrawer(false));

document.addEventListener("carrito:actualizado", () => {
    renderDrawer();
    toggleCartDrawer(true);
});

renderDrawer();
