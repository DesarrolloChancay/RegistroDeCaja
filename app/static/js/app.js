    $('#btn-exportar').on('click', function() {
        window.location.href = '/auditoria/exportar';
    });
// --- Paginación AJAX personalizada ---

let paginaActual = 1;
let registrosPorPagina = 10;
let filtrosActuales = {};

function cargarPaginaAuditoria(pagina, filtros = null) {
    if (filtros !== null) filtrosActuales = filtros;
    $.post('/auditoria/tabla', {
        pagina: pagina,
        por_pagina: registrosPorPagina,
        ...filtrosActuales
    }, function(res) {
        if (typeof res === 'string') {
            // Si la respuesta es HTML (retrocompatibilidad)
            $('tbody#registros_auditoria').html(res);
            $('#btn-pag-anterior').prop('disabled', pagina <= 1);
            $('#btn-pag-siguiente').prop('disabled', false);
            $('#pagina-actual').text(pagina);
            paginaActual = pagina;
            // Actualizar texto de rango (fallback)
            $('#pag-desde').text(1);
            $('#pag-hasta').text(registrosPorPagina);
            $('#pag-total').text(0);
            $('#paginas-numeros').html('');
            return;
        }
        $('tbody#registros_auditoria').html(res.html);
        $('#pagina-actual').text(pagina);
        paginaActual = pagina;
        // Control de botones
        $('#btn-pag-anterior').prop('disabled', pagina <= 1);
        $('#btn-pag-siguiente').prop('disabled', !res.hay_mas);

        // Actualizar texto de rango
        let desde = res.total === 0 ? 0 : ((pagina - 1) * registrosPorPagina) + 1;
        let hasta = Math.min(pagina * registrosPorPagina, res.total);
        $('#pag-desde').text(desde);
        $('#pag-hasta').text(hasta);
        $('#pag-total').text(res.total);

        // --- Números de página ---
        let totalPaginas = Math.ceil(res.total / registrosPorPagina);
        let htmlPaginas = '';
        let maxMostrar = 5;
        let start = Math.max(1, pagina - 2);
        let end = Math.min(totalPaginas, start + maxMostrar - 1);
        if (end - start < maxMostrar - 1) start = Math.max(1, end - maxMostrar + 1);
        if (start > 1) {
            htmlPaginas += '<button class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 border border-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0" data-pag="1">1</button>';
            if (start > 2) htmlPaginas += '<span class="relative inline-flex items-center px-2 py-2 text-sm font-semibold text-gray-700">...</span>';
        }
        for (let i = start; i <= end; i++) {
            if (i === pagina) {
                htmlPaginas += '<button class="relative z-10 inline-flex items-center bg-indigo-600 px-4 py-2 text-sm font-semibold text-white border border-gray-300 focus:z-20 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" data-pag="'+i+'">'+i+'</button>';
            } else {
                htmlPaginas += '<button class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 border border-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0" data-pag="'+i+'">'+i+'</button>';
            }
        }
        if (end < totalPaginas) {
            if (end < totalPaginas - 1) htmlPaginas += '<span class="relative inline-flex items-center px-2 py-2 text-sm font-semibold text-gray-700">...</span>';
            htmlPaginas += '<button class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 border border-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0" data-pag="'+totalPaginas+'">'+totalPaginas+'</button>';
        }
        $('#paginas-numeros').html(htmlPaginas);

        // Click en número de página
        $('#paginas-numeros button[data-pag]').off('click').on('click', function() {
            let pag = parseInt($(this).attr('data-pag'));
            if (pag !== paginaActual) cargarPaginaAuditoria(pag);
        });
    }, 'json');
}

$(document).ready(function() {
    // Inicial: cargar primera página
    cargarPaginaAuditoria(1, {});

    $('#select-registros-pagina').on('change', function() {
        registrosPorPagina = parseInt($(this).val());
        cargarPaginaAuditoria(1, filtrosActuales);
    });

    $('#btn-buscar-rango').on('click', function() {
        const fechaDesde = $('#fecha_desde').val();
        const fechaHasta = $('#fecha_hasta').val();
        cargarPaginaAuditoria(1, {fecha_desde: fechaDesde, fecha_hasta: fechaHasta});
    });

    $('#btn-borrar-filtros').on('click', function() {
        $('#fecha_desde').val('');
        $('#fecha_hasta').val('');
        cargarPaginaAuditoria(1, {});
    });

    $('#btn-pag-anterior').on('click', function() {
        if (paginaActual > 1) {
            cargarPaginaAuditoria(paginaActual - 1);
        }
    });
    $('#btn-pag-siguiente').on('click', function() {
        cargarPaginaAuditoria(paginaActual + 1);
    });
});
// Archivo: app/static/js/app.js

// --- Guardar edición de fechas (solo admin) ---

function guardarFechaVoucher(id) {
    const input = document.getElementById(`fecha_redes_${id}`);
    const fecha = input?.value;
    if (!fecha) {
        alert('Por favor, selecciona una fecha.');
        return;
    }
    mostrarDialogoConfirmacion({
        titulo: 'Confirmar edición de fecha de voucher',
        mensaje: `¿Deseas guardar la fecha <b>${fecha}</b> para el voucher? Esta acción es irreversible y quedará registrada en auditoría.`,
        textoBoton: 'Guardar fecha',
        onConfirm: () => {
            $.ajax({
                url: '/admin/editar_fecha_voucher',
                method: 'POST',
                data: { id: id, fecha: fecha },
                success: function(resp) {
                    if (resp.success) {
                        actualizarTablaAuditoria();
                    } else {
                        alert(resp.error || 'Error al guardar fecha.');
                    }
                },
                error: function(xhr) {
                    alert('Error en el servidor: ' + (xhr.responseJSON?.error || xhr.statusText));
                }
            });
        }
    });
}


function guardarFechaIngreso(id) {
    const input = document.getElementById(`fecha_ingreso_cuenta_${id}`);
    const fecha = input?.value;
    if (!fecha) {
        alert('Por favor, selecciona una fecha.');
        return;
    }
    mostrarDialogoConfirmacion({
        titulo: 'Confirmar edición de fecha de ingreso',
        mensaje: `¿Deseas guardar la fecha <b>${fecha}</b> para el ingreso de dinero? Esta acción es irreversible y quedará registrada en auditoría.`,
        textoBoton: 'Guardar fecha',
        onConfirm: () => {
            $.ajax({
                url: '/admin/editar_fecha_ingreso',
                method: 'POST',
                data: { id: id, fecha: fecha },
                success: function(resp) {
                    if (resp.success) {
                        actualizarTablaAuditoria();
                    } else {
                        alert(resp.error || 'Error al guardar fecha.');
                    }
                },
                error: function(xhr) {
                    alert('Error en el servidor: ' + (xhr.responseJSON?.error || xhr.statusText));
                }
            });
        }
    });
}

function confirmarRedes(id) {
    const inputFecha = document.getElementById(`fecha_redes_${id}`);
    const fechaSeleccionada = inputFecha?.value;

    console.log("Fecha seleccionada:", fechaSeleccionada);

    if (!fechaSeleccionada) {
        alert("⚠️ Por favor, selecciona una fecha para confirmar redes.");
        return;
    }

    mostrarDialogoConfirmacion({
        titulo: "Confirmar desde Redes",
        mensaje: "¿Deseas confirmar esta transacción desde redes? Esta acción es irreversible.",
        textoBoton: "Sí, confirmar",
        onConfirm: () => {
            $.ajax({
                url: `/confirmar_redes/${id}`,
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify({ fecha: fechaSeleccionada }),
                success: function(data) {
                    if (data.success) {
                        actualizarTablaAuditoria()
                    } else {
                        alert(data.error || "Error al confirmar.");
                    }
                },
                error: function(jqXHR) {
                    console.error("Server Error:", jqXHR.responseText);
                    alert("Ocurrió un error en el servidor. Por favor, revisa la consola para más detalles.");
                }
            });
        }
    });
}

function confirmarGerencia(id) {
    const inputFecha = document.getElementById(`fecha_ingreso_cuenta_${id}`);
    const fechaSeleccionada = inputFecha?.value;

    if (!fechaSeleccionada) {
        alert("⚠️ Por favor, selecciona una fecha para confirmar gerencia.");
        return;
    }

    mostrarDialogoConfirmacion({
        titulo: "Confirmar desde Gerencia",
        mensaje: "¿Deseas confirmar esta transacción desde gerencia? Esta acción es irreversible.",
        textoBoton: "Sí, confirmar",
        onConfirm: () => {
            $.ajax({
                url: `/confirmar_gerencia/${id}`,
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify({ fecha: fechaSeleccionada }),
                success: function(data) {
                    if (data.success) {
                        actualizarTablaAuditoria()
                    } else {
                        alert(data.error || "Error al confirmar.");
                    }
                },
                error: function(jqXHR) {
                    console.error("Server Error:", jqXHR.responseText);
                    alert("Ocurrió un error en el servidor. Por favor, revisa la consola para más detalles.");
                }
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
    // Permitir HTML en el mensaje (para resaltar la fecha)
    mensajeElem.innerHTML = mensaje;
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

function actualizarTablaAuditoria() {
    $.post('/auditoria/tabla', {
        pagina: paginaActual,
        por_pagina: registrosPorPagina,
        ...filtrosActuales
    }, function(res) {
        if (typeof res === 'string') {
            $('tbody#registros_auditoria').html(res);
            return;
        }
        $('tbody#registros_auditoria').html(res.html);
        // Actualizar paginación y totales
        let pagina = paginaActual;
        $('#pagina-actual').text(pagina);
        $('#btn-pag-anterior').prop('disabled', pagina <= 1);
        $('#btn-pag-siguiente').prop('disabled', !res.hay_mas);
        let desde = res.total === 0 ? 0 : ((pagina - 1) * registrosPorPagina) + 1;
        let hasta = Math.min(pagina * registrosPorPagina, res.total);
        $('#pag-desde').text(desde);
        $('#pag-hasta').text(hasta);
        $('#pag-total').text(res.total);
        // Números de página
        let totalPaginas = Math.ceil(res.total / registrosPorPagina);
        let htmlPaginas = '';
        let maxMostrar = 5;
        let start = Math.max(1, pagina - 2);
        let end = Math.min(totalPaginas, start + maxMostrar - 1);
        if (end - start < maxMostrar - 1) start = Math.max(1, end - maxMostrar + 1);
        if (start > 1) {
            htmlPaginas += '<button class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 border border-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0" data-pag="1">1</button>';
            if (start > 2) htmlPaginas += '<span class="relative inline-flex items-center px-2 py-2 text-sm font-semibold text-gray-700">...</span>';
        }
        for (let i = start; i <= end; i++) {
            if (i === pagina) {
                htmlPaginas += '<button class="relative z-10 inline-flex items-center bg-indigo-600 px-4 py-2 text-sm font-semibold text-white border border-gray-300 focus:z-20 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" data-pag="'+i+'">'+i+'</button>';
            } else {
                htmlPaginas += '<button class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 border border-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0" data-pag="'+i+'">'+i+'</button>';
            }
        }
        if (end < totalPaginas) {
            if (end < totalPaginas - 1) htmlPaginas += '<span class="relative inline-flex items-center px-2 py-2 text-sm font-semibold text-gray-700">...</span>';
            htmlPaginas += '<button class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 border border-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0" data-pag="'+totalPaginas+'">'+totalPaginas+'</button>';
        }
        $('#paginas-numeros').html(htmlPaginas);
        // Click en número de página
        $('#paginas-numeros button[data-pag]').off('click').on('click', function() {
            let pag = parseInt($(this).attr('data-pag'));
            if (pag !== paginaActual) cargarPaginaAuditoria(pag);
        });
    }, 'json');
}