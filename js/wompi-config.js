// Configuración del checkout con Wompi. Mientras estos dos valores sigan
// empezando por "TU_", el checkout sigue funcionando normalmente (el pedido
// se registra por WhatsApp marcado como "pago por coordinar"), pero no se
// abre el widget de pago real — ver la guía de despliegue en CLAUDE.md.

// Tu llave pública de Wompi (sandbox o producción), desde
// Desarrollo → Programadores en tu dashboard de Wompi.
// Debe coincidir siempre con el mismo ambiente que la llave de integridad
// guardada en el servidor (ver server/wompi-signature.js).
const WOMPI_PUBLIC_KEY = "pub_prod_e2ubHDKR9cSCvTdlOgodHLNDrJrqt5kH";

// URL pública de tu función de firma ya desplegada (ver server/wompi-signature.js).
const WOMPI_SIGNATURE_ENDPOINT = "https://wompi-signature.daniel21sulaiman.workers.dev";
