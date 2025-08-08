// Archivo: app/static/js/app.js

function confirmarRedes(id) {
    const inputFecha = document.getElementById(`fecha_redes_${id}`);
    const fechaSeleccionada = inputFecha?.value;

    console.log("Fecha seleccionada:", fechaSeleccionada);

    if (!fechaSeleccionada) {
        // En lugar de alert, se podría usar un modal más amigable.
        alert("⚠️ Por favor, selecciona una fecha para confirmar redes.");
        return;
    }

    mostrarDialogoConfirmacion({
        titulo: "Confirmar desde Redes",
        mensaje: "¿Deseas confirmar esta transacción desde redes? Esta acción es irreversible.",
        textoBoton: "Sí, confirmar",
        onConfirm: () => {
            fetch(`/confirmar_redes/${id}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ fecha: fechaSeleccionada }),
            })
            .then(async (res) => {
                if (!res.ok) {
                    const errorText = await res.text();
                    console.error("Server Error:", errorText);
                    throw new Error("Ocurrió un error en el servidor. Por favor, revisa la consola para más detalles.");
                }
                return res.json();
            })
            .then((data) => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert(data.error || "Error al confirmar.");
                }
            })
            .catch((err) => {
                console.error(err);
                alert(err.message || "Error en la comunicación con el servidor.");
            });
        }
    });
}

function confirmarGerencia(id) {
    const inputFecha = document.getElementById(`fecha_ingreso_cuenta_${id}`);
    const fechaSeleccionada = inputFecha?.value;

    if (!fechaSeleccionada) {
        // En lugar de alert, se podría usar un modal más amigable.
        alert("⚠️ Por favor, selecciona una fecha para confirmar gerencia.");
        return;
    }

    mostrarDialogoConfirmacion({
        titulo: "Confirmar desde Gerencia",
        mensaje: "¿Deseas confirmar esta transacción desde gerencia? Esta acción es irreversible.",
        textoBoton: "Sí, confirmar",
        onConfirm: () => {
            fetch(`/confirmar_gerencia/${id}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ fecha: fechaSeleccionada }),
            })
            .then(async (res) => {
                if (!res.ok) {
                    const errorText = await res.text();
                    console.error("Server Error:", errorText);
                    throw new Error("Ocurrió un error en el servidor. Por favor, revisa la consola para más detalles.");
                }
                return res.json();
            })
            .then((data) => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert(data.error || "Error al confirmar.");
                }
            })
            .catch((err) => {
                console.error(err);
                alert(err.message || "Error en la comunicación con el servidor.");
            });
        }
    });
}


function mostrarDialogoConfirmacion({ titulo, mensaje, textoBoton, onConfirm }) {
    const dialog = document.getElementById("dialog-confirmar");
    const title = document.getElementById("dialog-title");
    const mensajeElem = dialog.querySelector("p");
    const confirmarBtn = document.getElementById("btn-confirmar-modal");
    const cancelarBtn = document.getElementById("btn-cancelar-modal");

    title.innerText = titulo;
    mensajeElem.innerText = mensaje;
    confirmarBtn.innerText = textoBoton || "Confirmar";

    // Clonar el botón para eliminar escuchadores de eventos anteriores
    const nuevoBtn = confirmarBtn.cloneNode(true);
    confirmarBtn.parentNode.replaceChild(nuevoBtn, confirmarBtn);

    nuevoBtn.addEventListener("click", () => {
        onConfirm();
        dialog.close();
    });

    // Se asigna el evento click al botón de cancelar que ya existe
    cancelarBtn.onclick = () => dialog.close();

    dialog.showModal();
}