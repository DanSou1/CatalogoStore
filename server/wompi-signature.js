// Cloudflare Worker: calcula la firma de integridad que exige Wompi
// (SHA256 de referencia + monto + moneda + clave secreta) sin exponer esa
// clave secreta en el sitio. Ver server/README.md para desplegarlo.
//
// El sitio (js/checkout.js) le envía { reference, amountInCents, currency }
// por POST y este Worker responde { signature: "..." }.

const ORIGEN_PERMITIDO = "https://dansou1.github.io";

export default {
    async fetch(request, env) {
        const encabezadosCORS = {
            "Access-Control-Allow-Origin": ORIGEN_PERMITIDO,
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        };

        if (request.method === "OPTIONS") {
            return new Response(null, { headers: encabezadosCORS });
        }

        if (request.method !== "POST") {
            return new Response("Método no permitido", { status: 405, headers: encabezadosCORS });
        }

        let cuerpo;
        try {
            cuerpo = await request.json();
        } catch {
            return new Response("JSON inválido", { status: 400, headers: encabezadosCORS });
        }

        const { reference, amountInCents, currency } = cuerpo;
        if (!reference || !amountInCents || !currency) {
            return new Response("Faltan reference, amountInCents o currency", { status: 400, headers: encabezadosCORS });
        }

        const datos = `${reference}${amountInCents}${currency}${env.WOMPI_INTEGRITY_SECRET}`;
        const hash = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(datos));
        const firma = [...new Uint8Array(hash)].map(b => b.toString(16).padStart(2, "0")).join("");

        return new Response(JSON.stringify({ signature: firma }), {
            headers: { "Content-Type": "application/json", ...encabezadosCORS },
        });
    },
};
