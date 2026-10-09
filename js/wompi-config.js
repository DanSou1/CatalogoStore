// Configuración del checkout con Wompi. Mientras estos dos valores sigan
// empezando por "TU_", el checkout sigue funcionando normalmente (el pedido
// se registra por WhatsApp marcado como "pago por coordinar"), pero no se
// abre el widget de pago real — ver la guía de despliegue en CLAUDE.md.

// Tu llave pública de Wompi (sandbox o producción), desde
// Desarrollo → Programadores en tu dashboard de Wompi.
// TEMPORAL: esta es la de PRUEBAS (Sandbox) — no mueve dinero real. Se usa
// para probar el flujo completo con las tarjetas de prueba oficiales de
// Wompi (https://docs.wompi.co/en/docs/colombia/datos-de-prueba-en-sandbox/)
// antes de volver a poner la llave de producción. Debe coincidir siempre
// con el mismo ambiente que la llave de integridad guardada en el servidor
// (ver server/wompi-signature.js).
const WOMPI_PUBLIC_KEY = "pub_test_WYUl7l9Mw4V2XGYAolGoCLAOkLIzOzrn";

// URL pública de tu función de firma ya desplegada (ver server/wompi-signature.js).
const WOMPI_SIGNATURE_ENDPOINT = "https://wompi-signature.daniel21sulaiman.workers.dev";
