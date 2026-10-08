document.querySelectorAll(".faq-pregunta").forEach(boton => {
    boton.addEventListener("click", () => {
        const contenido = boton.nextElementSibling;
        const abierta = !contenido.classList.contains("disabled");

        document.querySelectorAll(".faq-respuesta").forEach(c => c.classList.add("disabled"));

        if (!abierta) contenido.classList.remove("disabled");
    });
});
