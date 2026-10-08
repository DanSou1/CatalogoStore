let productosEnCarrito = leerCarrito();

const contenedorCarritoVacio = document.querySelector("#carrito-vacio");
const contenedorCarritoGrid = document.querySelector("#carrito-grid");
const contenedorCarritoProductos = document.querySelector("#carrito-productos");
const contenedorCarritoComprado = document.querySelector("#carrito-comprado");
const botonVaciar = document.querySelector("#carrito-acciones-vaciar");
const contenedorTotal = document.querySelector("#total");
const botonComprar = document.querySelector("#carrito-acciones-comprar");


function cargarProductosCarrito() {
    if (productosEnCarrito && productosEnCarrito.length > 0) {

        contenedorCarritoVacio.classList.add("disabled");
        contenedorCarritoGrid.classList.remove("disabled");
        contenedorCarritoComprado.classList.add("disabled");

        contenedorCarritoProductos.innerHTML = "";

        productosEnCarrito.forEach(producto => {

            const div = document.createElement("div");
            div.classList.add("carrito-producto");
            div.innerHTML = `
                <div class="carrito-producto-imagen-wrapper">
                    <img class="carrito-producto-imagen" src="${producto.imagen}" alt="${producto.titulo}">
                </div>
                <div class="carrito-producto-info">
                    <div class="carrito-producto-encabezado">
                        <h3 class="carrito-producto-titulo">${producto.titulo}</h3>
                        <button class="carrito-producto-eliminar" id="${producto.id}" aria-label="Eliminar">
                            <span class="material-symbols-outlined">delete</span>
                        </button>
                    </div>
                    <div class="carrito-producto-pie">
                        <div class="carrito-producto-cantidad">
                            <button class="carrito-producto-restar" data-id="${producto.id}" aria-label="Restar"><span class="material-symbols-outlined">remove</span></button>
                            <span class="carrito-producto-cantidad-numero">${producto.cantidad}</span>
                            <button class="carrito-producto-sumar" data-id="${producto.id}" aria-label="Sumar"><span class="material-symbols-outlined">add</span></button>
                        </div>
                        <p class="carrito-producto-precio">$${producto.precio * producto.cantidad}</p>
                    </div>
                </div>
            `;

            contenedorCarritoProductos.append(div);
        })

    actualizarBotonesEliminar();
    actualizarBotonesCantidad();
    actualizarTotal();

    } else {
        contenedorCarritoVacio.classList.remove("disabled");
        contenedorCarritoGrid.classList.add("disabled");
        contenedorCarritoComprado.classList.add("disabled");
    }

}

cargarProductosCarrito();

function actualizarBotonesEliminar() {
    document.querySelectorAll(".carrito-producto-eliminar").forEach(boton => {
        boton.addEventListener("click", eliminarDelCarrito);
    });
}

function actualizarBotonesCantidad() {
    document.querySelectorAll(".carrito-producto-restar").forEach(boton => {
        boton.addEventListener("click", restarCantidad);
    });
    document.querySelectorAll(".carrito-producto-sumar").forEach(boton => {
        boton.addEventListener("click", sumarCantidad);
    });
}

function eliminarDelCarrito(e) {
    Toastify({
        text: "Producto eliminado",
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
    quitarProducto(productosEnCarrito, idBoton);
    guardarYActualizar();
}

function restarCantidad(e) {
    decrementarProducto(productosEnCarrito, e.currentTarget.dataset.id);
    guardarYActualizar();
}

function sumarCantidad(e) {
    incrementarProducto(productosEnCarrito, e.currentTarget.dataset.id);
    guardarYActualizar();
}

function guardarYActualizar() {
    cargarProductosCarrito();
    document.dispatchEvent(new CustomEvent("carrito:actualizado"));
}

botonVaciar.addEventListener("click", vaciarCarrito);
function vaciarCarrito() {

    Swal.fire({
        title: '¿Estás seguro?',
        icon: 'question',
        html: `Se van a borrar ${productosEnCarrito.reduce((acc, producto) => acc + producto.cantidad, 0)} productos.`,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
        confirmButtonColor: '#832062',
        cancelButtonColor: '#1B1A1A'
    }).then((result) => {
        if (result.isConfirmed) {
            vaciarArregloCarrito(productosEnCarrito);
            guardarYActualizar();
        }
    })
}


function actualizarTotal() {
    total.innerText = `$${calcularTotalPrecio(productosEnCarrito)}`;
}

botonComprar.addEventListener("click", comprarCarrito);

function comprarCarrito() {
    if (productosEnCarrito.length === 0) {
        alert("El carrito está vacío.");
        return;
    }

    // Crear un mensaje con los productos
    let mensaje = "¡Hola! Estos son los productos de mi carrito:\n\n";
    productosEnCarrito.forEach(producto => {
        mensaje += `- ${producto.titulo} x${producto.cantidad}: $${producto.precio * producto.cantidad}\n`;
    });
    mensaje += `\nTotal: $${productosEnCarrito.reduce((acc, producto) => acc + (producto.precio * producto.cantidad), 0)}`;

    // Convertir el mensaje a formato URL
    const mensajeCodificado = encodeURIComponent(mensaje);
    const numeroWhatsApp = "573150338545";
    const urlWhatsApp = `https://wa.me/${numeroWhatsApp}?text=${mensajeCodificado}`;

    // Abrir WhatsApp
    window.open(urlWhatsApp, "_blank");

    // Vaciar el carrito
    vaciarArregloCarrito(productosEnCarrito);

    contenedorCarritoVacio.classList.add("disabled");
    contenedorCarritoGrid.classList.add("disabled");
    contenedorCarritoComprado.classList.remove("disabled");
}
