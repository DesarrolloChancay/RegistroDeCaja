function confirmarRedes(id) {
    const inputFecha = document.getElementById(`fecha_redes_${id}`);
    const fechaSeleccionada = inputFecha?.value;

    if (!fechaSeleccionada) {
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
                .then((res) => res.json())
                .then((data) => {
                    if (data.success) {
                        window.location.reload();
                    } else {
                        alert(data.error || "Error al confirmar.");
                    }
                })
                .catch((err) => {
                    console.error(err);
                    alert("Error en el servidor.");
                });
        }
    });
}

function mostrarDialogoConfirmacion({ titulo, mensaje, textoBoton, onConfirm }) {
    const dialog = document.getElementById("dialog-confirmar");
    const title = document.getElementById("dialog-title");
    const mensajeElem = dialog.querySelector("p");
    const confirmarBtn = document.getElementById("btn-confirmar-modal");

    title.innerText = titulo;
    mensajeElem.innerText = mensaje;
    confirmarBtn.innerText = textoBoton || "Confirmar";

    const nuevoBtn = confirmarBtn.cloneNode(true);
    confirmarBtn.parentNode.replaceChild(nuevoBtn, confirmarBtn);

    nuevoBtn.addEventListener("click", () => {
        onConfirm();
        dialog.close();
    });

    dialog.showModal();
}

