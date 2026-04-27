const form = document.getElementById("formSolicitud");

form?.addEventListener("submit", async function(event) {
    event.preventDefault();

    const payload = {
        nombre_apellido: document.getElementById("nombre_apellido").value.trim(),
        correo: document.getElementById("correo").value.trim(),
        cedula: document.getElementById("cedula").value.trim(),
        cargo: document.getElementById("cargo").value.trim(),
        proceso: document.getElementById("proceso").value.trim(),
        fecha_inicio: document.getElementById("fecha_inicio").value,
        hora_inicio: document.getElementById("hora_inicio").value,
        fecha_fin: document.getElementById("fecha_fin").value,
        hora_fin: document.getElementById("hora_fin").value
    };

    try {
        const response = await fetch("/solicitudes", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error("No se pudo enviar la solicitud");
        }

        form.reset();
        alert("Solicitud enviada correctamente. El panel administrativo la procesará.");
    } catch (error) {
        console.error(error);
        alert("Error al enviar la solicitud. Intente de nuevo más tarde.");
    }
});