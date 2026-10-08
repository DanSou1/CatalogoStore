let productos = [];

fetch("./js/productos.json")
    .then(response => response.json())
    .then(data => {
        productos = data;
        cargarProductos(productos);
        renderCarruselPromociones(productos);
    })


const contenedorProductos = document.querySelector("#contenedor-productos");
const botonesCategorias = document.querySelectorAll(".boton-categoria");
const tituloPrincipal = document.querySelector("#titulo-principal");
let botonesAgregar = document.querySelectorAll(".producto-agregar");
const numeritos = document.querySelectorAll(".numerito");


botonesCategorias.forEach(boton => boton.addEventListener("click", () => {
    aside.classList.remove("aside-visible");
}))


function cargarProductos(productosElegidos) {

    contenedorProductos.innerHTML = "";

    const temporada = temporadaActiva();
    const textoAgregar = temporada === "halloween" ? "Agregar 🎃" : "Agregar";

    ordenarPorTemporada(productosElegidos).forEach(producto => {

        const div = document.createElement("div");
        div.classList.add("producto");

        const tieneDescuento = producto.precioAnterior && producto.precioAnterior > producto.precio;
        const descuentoPct = tieneDescuento ? Math.round((1 - producto.precio / producto.precioAnterior) * 100) : 0;
        const agotado = producto.stock === 0;
        const esDeTemporada = temporada === "halloween" && esProductoDeTemporada(producto, "halloween");

        div.innerHTML = `
            <div class="producto-imagen-wrapper">
                ${tieneDescuento ? `<span class="producto-badge-descuento">-${descuentoPct}%</span>` : ""}
                ${esDeTemporada ? `<span class="producto-badge-halloween">🎃 Halloween</span>` : ""}
                <img class="producto-imagen" src="${producto.imagen}" alt="${producto.titulo}">
            </div>
            <div class="producto-detalles">
                <h3 class="producto-titulo">${producto.titulo}</h3>
                ${producto.stock !== undefined && producto.stock <= 5
                    ? `<p class="producto-stock ${agotado ? "producto-stock-agotado" : ""}">${agotado ? "Agotado" : "Solo quedan " + producto.stock}</p>`
                    : ""}
                <div class="producto-precios">
                    ${tieneDescuento ? `<span class="producto-precio-anterior">$${producto.precioAnterior}</span>` : ""}
                    <p class="producto-precio">$${producto.precio}</p>
                </div>
                <button class="producto-agregar" id="${producto.id}" ${agotado ? "disabled" : ""}>${textoAgregar}</button>
            </div>
        `;

        contenedorProductos.append(div);
    })

    actualizarBotonesAgregar();
}


botonesCategorias.forEach(boton => {
    boton.addEventListener("click", (e) => {

        botonesCategorias.forEach(boton => boton.classList.remove("active"));
        e.currentTarget.classList.add("active");

        if (e.currentTarget.id != "todos") {
            const productoCategoria = productos.find(producto => producto.categoria.id === e.currentTarget.id);
            tituloPrincipal.innerText = productoCategoria.categoria.nombre;
            const productosBoton = productos.filter(producto => producto.categoria.id === e.currentTarget.id);
            cargarProductos(productosBoton);
        } else {
            tituloPrincipal.innerText = "Todos los productos";
            cargarProductos(productos);
        }

    })
});

function actualizarBotonesAgregar() {
    botonesAgregar = document.querySelectorAll(".producto-agregar");

    botonesAgregar.forEach(boton => {
        boton.addEventListener("click", agregarAlCarrito);
    });
}

let productosEnCarrito = leerCarrito();
actualizarNumerito();

function agregarAlCarrito(e) {

    Toastify({
        text: "Producto agregado",
        duration: 3000,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "right", // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
          background: "linear-gradient(to right, #832062, #1B1A1A)",
          borderRadius: "2rem",
          textTransform: "uppercase",
          fontSize: ".75rem"
        },
        offset: {
            x: '1.5rem', // horizontal axis - can be a number or a string indicating unity. eg: '2em'
            y: '5.5rem' // vertical axis - clears the floating cart button in the top-right corner
          },
        onClick: function(){} // Callback after click
      }).showToast();

    const idBoton = e.currentTarget.id;
    const productoAgregado = productos.find(producto => producto.id === idBoton);

    agregarProductoAlCarrito(productosEnCarrito, productoAgregado);

    actualizarNumerito();
    document.dispatchEvent(new CustomEvent("carrito:actualizado"));
}

function actualizarNumerito() {
    const cantidad = calcularCantidadTotal(leerCarrito());
    numeritos.forEach(numerito => numerito.innerText = cantidad);
}

let carruselProductos = [];
let carruselIndex = 0;
let carruselInterval = null;

function renderCarruselPromociones(productos) {
    const heroSection = document.querySelector("#hero-destacado");
    const dotsContenedor = document.querySelector("#hero-carrusel-dots");
    if (!heroSection || !dotsContenedor) return;

    carruselProductos = ordenarPorTemporada(productos.filter(p => p.categoria.id === "Promociones"));

    if (!carruselProductos.length) {
        heroSection.classList.add("disabled");
        return;
    }

    heroSection.classList.remove("disabled");

    dotsContenedor.innerHTML = "";
    carruselProductos.forEach((_, index) => {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = "hero-carrusel-dot";
        dot.setAttribute("aria-label", `Ver promoción ${index + 1}`);
        dot.addEventListener("click", () => mostrarSlideCarrusel(index));
        dotsContenedor.append(dot);
    });

    mostrarSlideCarrusel(0);

    if (carruselProductos.length > 1) {
        heroSection.addEventListener("mouseenter", () => clearInterval(carruselInterval));
        heroSection.addEventListener("mouseleave", iniciarAutoRotacionCarrusel);
    }
    iniciarAutoRotacionCarrusel();
}

function iniciarAutoRotacionCarrusel() {
    clearInterval(carruselInterval);
    if (carruselProductos.length <= 1) return;
    carruselInterval = setInterval(() => {
        mostrarSlideCarrusel((carruselIndex + 1) % carruselProductos.length);
    }, 4500);
}

function mostrarSlideCarrusel(index) {
    const producto = carruselProductos[index];
    if (!producto) return;
    carruselIndex = index;

    const heroImagen = document.querySelector("#hero-producto-imagen");
    const heroTitulo = document.querySelector("#hero-producto-titulo");
    const heroPrecio = document.querySelector("#hero-producto-precio");
    const heroPrecioAnterior = document.querySelector("#hero-producto-precio-anterior");
    const heroBoton = document.querySelector('[data-rol="hero-agregar"]');
    if (!heroImagen || !heroTitulo || !heroPrecio || !heroBoton) return;

    heroImagen.src = producto.imagen;
    heroImagen.alt = producto.titulo;
    heroTitulo.innerText = producto.titulo;
    heroPrecio.innerText = `$${producto.precio}`;

    if (producto.precioAnterior && producto.precioAnterior > producto.precio) {
        heroPrecioAnterior.innerText = `$${producto.precioAnterior}`;
        heroPrecioAnterior.classList.remove("disabled");
    } else {
        heroPrecioAnterior.classList.add("disabled");
    }

    heroBoton.id = producto.id;
    heroBoton.innerText = temporadaActiva() === "halloween" ? "Agregar 🎃" : "Agregar";
    actualizarBotonesAgregar();

    document.querySelectorAll(".hero-carrusel-dot").forEach((dot, i) => {
        dot.classList.toggle("active", i === index);
    });
}
