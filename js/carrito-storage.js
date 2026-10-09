const CARRITO_KEY = "productos-en-carrito";

function leerCarrito() {
    const raw = localStorage.getItem(CARRITO_KEY);
    return raw ? JSON.parse(raw) : [];
}

function guardarCarrito(productosEnCarrito) {
    localStorage.setItem(CARRITO_KEY, JSON.stringify(productosEnCarrito));
}

function agregarProductoAlCarrito(productosEnCarrito, producto) {
    const existente = productosEnCarrito.find(p => p.id === producto.id);
    if (existente) {
        existente.cantidad++;
    } else {
        producto.cantidad = 1;
        productosEnCarrito.push(producto);
    }
    guardarCarrito(productosEnCarrito);
    return productosEnCarrito;
}

function incrementarProducto(productosEnCarrito, id) {
    const index = productosEnCarrito.findIndex(p => p.id === id);
    if (index === -1) return productosEnCarrito;
    productosEnCarrito[index].cantidad++;
    guardarCarrito(productosEnCarrito);
    return productosEnCarrito;
}

function decrementarProducto(productosEnCarrito, id) {
    const index = productosEnCarrito.findIndex(p => p.id === id);
    if (index === -1) return productosEnCarrito;
    if (productosEnCarrito[index].cantidad > 1) {
        productosEnCarrito[index].cantidad--;
    } else {
        productosEnCarrito.splice(index, 1);
    }
    guardarCarrito(productosEnCarrito);
    return productosEnCarrito;
}

function quitarProducto(productosEnCarrito, id) {
    const index = productosEnCarrito.findIndex(p => p.id === id);
    if (index !== -1) productosEnCarrito.splice(index, 1);
    guardarCarrito(productosEnCarrito);
    return productosEnCarrito;
}

function vaciarArregloCarrito(productosEnCarrito) {
    productosEnCarrito.length = 0;
    guardarCarrito(productosEnCarrito);
    return productosEnCarrito;
}

function calcularCantidadTotal(productosEnCarrito) {
    return productosEnCarrito.reduce((acc, p) => acc + p.cantidad, 0);
}

function calcularTotalPrecio(productosEnCarrito) {
    return productosEnCarrito.reduce((acc, p) => acc + p.precio * p.cantidad, 0);
}

// Formatea un número a pesos colombianos con separador de miles (ej. 62000 -> "62.000").
// Solo para mostrar: nunca usar el resultado en cálculos, siempre el número crudo.
function formatearPrecio(valor) {
    return Math.round(valor).toLocaleString("es-CO");
}
