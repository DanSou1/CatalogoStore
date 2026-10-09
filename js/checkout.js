// Checkout: formulario de datos de envío + flete + pago con Wompi.
// Depende de los globals de carrito.js (productosEnCarrito, contenedorCarritoVacio,
// contenedorCarritoGrid, contenedorCarritoComprado) y de carrito-storage.js
// (calcularTotalPrecio, formatearPrecio, vaciarArregloCarrito).

const NUMERO_WHATSAPP = "573150338545";
const FLETE_BOGOTA = 10000;
const FLETE_OTRA_CIUDAD = 15000;

const contenedorDatosEnvio = document.querySelector("#carrito-datos-envio");
const contenedorErrorPago = document.querySelector("#carrito-error-pago");
const formDatosEnvio = document.querySelector("#form-datos-envio");
const campoDocumento = document.querySelector("#campo-documento");
const inputDocumento = document.querySelector("#envio-documento");
const selectCiudad = document.querySelector("#envio-ciudad");
const botonVolverDatosEnvio = document.querySelector("#datos-envio-volver");
const botonReintentarPago = document.querySelector("#error-pago-reintentar");
const botonComprarAhora = document.querySelector("#carrito-acciones-comprar");

function obtenerFlete() {
    return selectCiudad.value === "bogota" ? FLETE_BOGOTA : FLETE_OTRA_CIUDAD;
}

function obtenerCiudadLegible() {
    return selectCiudad.value === "bogota" ? "Bogotá D.C." : "Otra ciudad";
}

function actualizarCampoDocumento() {
    const fueraDeBogota = selectCiudad.value !== "bogota";
    campoDocumento.classList.toggle("disabled", !fueraDeBogota);
    inputDocumento.required = fueraDeBogota;
    if (!fueraDeBogota) inputDocumento.value = "";
}

function actualizarResumenEnvio() {
    const subtotal = calcularTotalPrecio(productosEnCarrito);
    const flete = obtenerFlete();
    document.querySelector("#datos-envio-subtotal").innerText = `$${formatearPrecio(subtotal)}`;
    document.querySelector("#datos-envio-flete").innerText = `$${formatearPrecio(flete)}`;
    document.querySelector("#datos-envio-flete-nota").innerText = ` (${obtenerCiudadLegible()})`;
    document.querySelector("#datos-envio-total").innerText = `$${formatearPrecio(subtotal + flete)}`;
}

selectCiudad.addEventListener("change", () => {
    actualizarCampoDocumento();
    actualizarResumenEnvio();
});

botonComprarAhora.addEventListener("click", () => {
    actualizarCampoDocumento();
    actualizarResumenEnvio();
    contenedorCarritoGrid.classList.add("disabled");
    contenedorDatosEnvio.classList.remove("disabled");
    contenedorDatosEnvio.scrollIntoView({ behavior: "smooth", block: "start" });
});

botonVolverDatosEnvio.addEventListener("click", () => {
    contenedorDatosEnvio.classList.add("disabled");
    contenedorCarritoGrid.classList.remove("disabled");
});

botonReintentarPago.addEventListener("click", () => {
    contenedorErrorPago.classList.add("disabled");
    contenedorDatosEnvio.classList.remove("disabled");
});

formDatosEnvio.addEventListener("submit", (e) => {
    e.preventDefault();
    iniciarPago();
});

// Mientras no se configuren WOMPI_PUBLIC_KEY / WOMPI_SIGNATURE_ENDPOINT en
// js/wompi-config.js (ver ese archivo), el checkout sigue funcionando: el
// pedido se registra igual por WhatsApp, solo que marcado como pendiente de
// coordinar el pago, en vez de abrir el widget de Wompi. Así el sitio nunca
// queda roto mientras Daniel completa su cuenta de Wompi y despliega el
// servidor de firma (ver server/wompi-signature.js).
function wompiEstaConfigurado() {
    return typeof WOMPI_PUBLIC_KEY === "string" && !WOMPI_PUBLIC_KEY.startsWith("TU_")
        && typeof WOMPI_SIGNATURE_ENDPOINT === "string" && !WOMPI_SIGNATURE_ENDPOINT.startsWith("TU_");
}

function leerDatosEnvioFormulario() {
    return {
        nombre: document.querySelector("#envio-nombre").value.trim(),
        contacto: document.querySelector("#envio-contacto").value.trim(),
        ciudad: obtenerCiudadLegible(),
        direccion: document.querySelector("#envio-direccion").value.trim(),
        documento: inputDocumento.value.trim(),
    };
}

async function iniciarPago() {
    if (!formDatosEnvio.reportValidity()) return;

    const datosEnvio = leerDatosEnvioFormulario();
    const subtotal = calcularTotalPrecio(productosEnCarrito);
    const flete = obtenerFlete();
    const total = subtotal + flete;
    const referencia = `EL-${Date.now()}`;

    if (!wompiEstaConfigurado()) {
        finalizarPedidoPorWhatsApp({ referencia, subtotal, flete, total, datosEnvio, estado: "PENDIENTE_CONFIGURACION" });
        return;
    }

    const botonContinuar = document.querySelector("#datos-envio-continuar");
    const textoOriginalBoton = botonContinuar.innerHTML;
    botonContinuar.disabled = true;
    botonContinuar.innerText = "Abriendo pago...";

    try {
        // IMPORTANTE: al configurar la cuenta real de Wompi, confirma en su
        // dashboard el nombre exacto del campo de firma en el constructor de
        // WidgetCheckout (la documentación lo muestra distinto según la
        // sección) — aquí se asume `signature: { integrity: "..." }`,
        // siguiendo el mismo patrón anidado que customerData/shippingAddress.
        const firma = await obtenerFirma(referencia, Math.round(total * 100), "COP");

        const checkout = new WidgetCheckout({
            currency: "COP",
            amountInCents: Math.round(total * 100),
            reference: referencia,
            publicKey: WOMPI_PUBLIC_KEY,
            signature: { integrity: firma },
            customerData: {
                fullName: datosEnvio.nombre,
                phoneNumber: datosEnvio.contacto,
                phoneNumberPrefix: "+57",
            },
            shippingAddress: {
                addressLine1: datosEnvio.direccion,
                city: datosEnvio.ciudad,
                region: datosEnvio.ciudad,
                country: "CO",
                phoneNumber: datosEnvio.contacto,
            },
        });

        checkout.open((resultado) => {
            const estado = resultado && resultado.transaction && resultado.transaction.status;
            if (estado === "APPROVED" || estado === "PENDING") {
                finalizarPedidoPorWhatsApp({ referencia, subtotal, flete, total, datosEnvio, estado });
            } else {
                mostrarErrorPago();
            }
        });
    } catch (error) {
        console.error("No se pudo iniciar el pago con Wompi:", error);
        mostrarErrorPago();
    } finally {
        botonContinuar.disabled = false;
        botonContinuar.innerHTML = textoOriginalBoton;
    }
}

async function obtenerFirma(referencia, amountInCents, currency) {
    const respuesta = await fetch(WOMPI_SIGNATURE_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reference: referencia, amountInCents, currency }),
    });
    if (!respuesta.ok) throw new Error("El servidor de firma respondió con un error");
    const datos = await respuesta.json();
    if (!datos.signature) throw new Error("El servidor de firma no devolvió una firma válida");
    return datos.signature;
}

function finalizarPedidoPorWhatsApp({ referencia, subtotal, flete, total, datosEnvio, estado }) {
    let mensaje = "¡Hola! Acabo de completar mi pedido:\n\n";
    productosEnCarrito.forEach(producto => {
        mensaje += `- ${producto.titulo} x${producto.cantidad}: $${formatearPrecio(producto.precio * producto.cantidad)}\n`;
    });
    mensaje += `\nSubtotal: $${formatearPrecio(subtotal)}`;
    mensaje += `\nFlete (${datosEnvio.ciudad}): $${formatearPrecio(flete)}`;
    mensaje += `\nTotal: $${formatearPrecio(total)}`;
    mensaje += `\n\nDatos de envío:`;
    mensaje += `\nNombre: ${datosEnvio.nombre}`;
    mensaje += `\nContacto: ${datosEnvio.contacto}`;
    mensaje += `\nCiudad: ${datosEnvio.ciudad}`;
    mensaje += `\nDirección: ${datosEnvio.direccion}`;
    if (datosEnvio.documento) mensaje += `\nDocumento: ${datosEnvio.documento}`;
    mensaje += `\n\nReferencia de pedido: ${referencia}`;
    mensaje += estado === "PENDIENTE_CONFIGURACION"
        ? `\nPago: por coordinar directamente (checkout en línea aún no disponible)`
        : `\nEstado del pago: ${estado === "APPROVED" ? "Aprobado" : "Pendiente de confirmación"}`;

    const mensajeCodificado = encodeURIComponent(mensaje);
    window.open(`https://wa.me/${NUMERO_WHATSAPP}?text=${mensajeCodificado}`, "_blank");

    vaciarArregloCarrito(productosEnCarrito);

    contenedorDatosEnvio.classList.add("disabled");
    contenedorErrorPago.classList.add("disabled");
    contenedorCarritoVacio.classList.add("disabled");
    contenedorCarritoGrid.classList.add("disabled");
    contenedorCarritoComprado.classList.remove("disabled");
}

function mostrarErrorPago() {
    contenedorDatosEnvio.classList.add("disabled");
    contenedorErrorPago.classList.remove("disabled");
}
