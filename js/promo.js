// EDITA ESTA FECHA cuando tengas una promoción activa con fecha límite real.
// Formato: new Date("AAAA-MM-DDTHH:mm:ss-05:00")  (hora Colombia, UTC-5).
// Déjala en null para que la barra de cuenta regresiva permanezca oculta.
const FIN_PROMOCION = null; // ejemplo: new Date("2026-12-31T23:59:59-05:00")

const barraPromo = document.querySelector("#barra-promo");
const cuentaRegresivaEl = document.querySelector("#cuenta-regresiva");
let intervaloPromo;

function actualizarCuentaRegresiva() {
    const restanteMs = FIN_PROMOCION - new Date();
    if (restanteMs <= 0) {
        barraPromo.classList.add("disabled");
        clearInterval(intervaloPromo);
        return;
    }
    barraPromo.classList.remove("disabled");
    const totalSegundos = Math.floor(restanteMs / 1000);
    const dias = Math.floor(totalSegundos / 86400);
    const horas = String(Math.floor((totalSegundos % 86400) / 3600)).padStart(2, "0");
    const minutos = String(Math.floor((totalSegundos % 3600) / 60)).padStart(2, "0");
    const segundos = String(totalSegundos % 60).padStart(2, "0");
    cuentaRegresivaEl.innerText = dias > 0 ? `${dias}d ${horas}:${minutos}:${segundos}` : `${horas}:${minutos}:${segundos}`;
}

if (FIN_PROMOCION && barraPromo) {
    actualizarCuentaRegresiva();
    intervaloPromo = setInterval(actualizarCuentaRegresiva, 1000);
}
