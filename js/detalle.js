const modalProducto = document.querySelector("#modal-producto");
const modalImagen = modalProducto.querySelector(".modal-imagen");
const modalCategoria = modalProducto.querySelector(".modal-categoria");
const modalTitulo = modalProducto.querySelector(".modal-titulo");
const modalPrecio = modalProducto.querySelector(".modal-precio");
const modalDescripcion = modalProducto.querySelector(".modal-descripcion");
const modalFichas = modalProducto.querySelector(".modal-fichas");
const modalFicha = modalProducto.querySelector(".modal-ficha");
const modalFichaValor = modalFicha.querySelector("dd");
const modalNota = modalProducto.querySelector(".modal-nota");
const modalNotaTexto = modalNota.querySelector(".modal-nota-texto");
const modalCerrar = modalProducto.querySelector(".modal-cerrar");
const modalAgregar = modalProducto.querySelector(".modal-agregar");
const modalAgregarIcono = modalAgregar.querySelector(".material-symbols-outlined");
const modalAgregarTexto = modalAgregar.querySelector(".modal-agregar-texto");

// Número de WhatsApp de la tienda (código de país + número, sin "+" ni espacios).
const NUMERO_WHATSAPP_ASESOR = "573004675206";
const modalWhatsapp = modalProducto.querySelector(".modal-whatsapp");

// Enlace directo a un producto: https://dansou1.github.io/CatalogoStore/?p=<id del producto>
// Enlace directo a una categoría: https://dansou1.github.io/CatalogoStore/?c=<id de la categoría> (ej. ?c=Promociones)
function enlaceProducto(id) {
    return `${location.origin}${location.pathname}?p=${encodeURIComponent(id)}`;
}

function abrirDesdeEnlace() {
    const params = new URLSearchParams(location.search);
    const categoria = params.get("c");
    if (categoria) {
        const boton = document.getElementById(categoria);
        if (boton && boton.classList.contains("boton-categoria")) boton.click();
    }
    const id = params.get("p");
    if (id && productos.some(p => p.id === id)) {
        abrirModal(id);
    } else if (id) {
        history.replaceState(null, "", location.pathname);
    }
}

function enlaceWhatsappProducto(producto) {
    const mensaje = `Hola XperienceLove 👋 Quiero más información sobre: ${producto.titulo} ($${formatearPrecio(producto.precio)})\n${enlaceProducto(producto.id)}`;
    return `https://wa.me/${NUMERO_WHATSAPP_ASESOR}?text=${encodeURIComponent(mensaje)}`;
}

function abrirModal(id) {
    const producto = productos.find(p => p.id === id);
    if (!producto) return;

    modalImagen.src = producto.imagen;
    modalImagen.alt = "";
    modalCategoria.textContent = producto.categoria.nombre;
    modalTitulo.textContent = producto.titulo;
    modalPrecio.textContent = `$${formatearPrecio(producto.precio)}`;

    if (producto.descripcion) {
        modalDescripcion.textContent = producto.descripcion;
        modalDescripcion.hidden = false;
        modalProducto.setAttribute("aria-describedby", "modal-producto-descripcion");
    } else {
        modalDescripcion.textContent = "";
        modalDescripcion.hidden = true;
        modalProducto.removeAttribute("aria-describedby");
    }

    if (producto.medidas) {
        modalFichaValor.textContent = producto.medidas;
        modalFicha.hidden = false;
    } else {
        modalFichaValor.textContent = "";
        modalFicha.hidden = true;
    }

    if (producto.recomendacionesSalud) {
        modalNotaTexto.textContent = producto.recomendacionesSalud;
        modalNota.hidden = false;
    } else {
        modalNotaTexto.textContent = "";
        modalNota.hidden = true;
    }

    modalFichas.hidden = !producto.medidas && !producto.recomendacionesSalud;

    modalAgregar.dataset.id = producto.id;
    if (modalWhatsapp) {
        modalWhatsapp.href = enlaceWhatsappProducto(producto);
        modalWhatsapp.setAttribute("aria-label", `Hablar con un asesor por WhatsApp sobre ${producto.titulo}`);
    }
    modalAgregar.classList.remove("confirmado");
    modalAgregarIcono.textContent = "add_shopping_cart";
    modalAgregarTexto.textContent = "Agregar al carrito";

    history.replaceState(null, "", `?p=${encodeURIComponent(producto.id)}`);
    modalProducto.showModal();
    document.body.style.overflow = "hidden";
}

function cerrarModal() {
    modalProducto.classList.add("cerrando");
}

modalProducto.addEventListener("animationend", (e) => {
    if (e.target === modalProducto.querySelector(".modal-panel") && modalProducto.classList.contains("cerrando")) {
        modalProducto.close();
    }
});

modalProducto.addEventListener("close", () => {
    if (new URLSearchParams(location.search).has("p")) {
        history.replaceState(null, "", location.pathname);
    }
    document.body.style.overflow = "";
    modalProducto.classList.remove("cerrando");
});

modalProducto.addEventListener("cancel", (e) => {
    e.preventDefault();
    cerrarModal();
});

modalCerrar.addEventListener("click", cerrarModal);

modalProducto.addEventListener("click", (e) => {
    if (e.target === modalProducto) {
        cerrarModal();
    }
});

modalAgregar.addEventListener("click", (e) => {
    agregarAlCarrito(e);

    modalAgregar.classList.add("confirmado");
    modalAgregarIcono.textContent = "check_circle";
    modalAgregarTexto.textContent = "Agregado";

    setTimeout(() => {
        modalAgregar.classList.remove("confirmado");
        modalAgregarIcono.textContent = "add_shopping_cart";
        modalAgregarTexto.textContent = "Agregar al carrito";
    }, 1600);
});
