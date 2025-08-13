// Alerta de mensaje

$(document).ready(function () {
    const alert = $(".alert");

    setTimeout(function () {
        alert.removeClass("translate-x-full opacity-0")
            .addClass("translate-x-0 opacity-100");
    }, 100);

    setTimeout(function () {
        alert.removeClass("translate-x-0 opacity-100")
            .addClass("translate-x-full opacity-0");
        setTimeout(function () {
            alert.remove();
        }, 500);
    }, 4000);
});

function mostrarAlerta(mensaje, tipo = 'success') {
    // Elimina alertas previas
    $('.alert-auditoria').remove();
    let color = tipo === 'success' ? 'bg-green-500' : 'bg-red-500';
    let html = `<div class="alert-auditoria fixed top-4 left-1/2 transform -translate-x-1/2 z-50 ${color} text-white px-6 py-3 rounded shadow transition-all opacity-0">${mensaje}</div>`;
    $('body').append(html);
    let $alert = $('.alert-auditoria');
    setTimeout(() => $alert.removeClass('opacity-0').addClass('opacity-100'), 50);
    setTimeout(() => {
        $alert.removeClass('opacity-100').addClass('opacity-0');
        setTimeout(() => $alert.remove(), 500);
    }, 3000);
}

$('#btn-exportar').on('click', function () {
    window.location.href = '/auditoria/exportar';
});
// --- Paginación AJAX personalizada ---


let paginaActual = 1;
let registrosPorPagina = 10;
let filtrosActuales = {};
let estadoConfirmacion = 'por_confirmar'; // por defecto
let ordenFecha = 'desc'; // asc o desc

function cargarPaginaAuditoria(pagina, filtros = null) {
    if (filtros !== null) filtrosActuales = filtros;
    // Determinar campo de orden según rol
    let campoOrden = 'fecha_confirmacion_redes';
    if (window.sessionRol === 'admin' || window.sessionRol === 'verificador') {
        campoOrden = 'fecha_confirmacion_gerencia';
    }
    $.post('/auditoria/tabla', {
        pagina: pagina,
        por_pagina: registrosPorPagina,
        estado_confirmacion: estadoConfirmacion,
        orden_campo: campoOrden,
        orden_dir: ordenFecha,
        ...filtrosActuales
    }, function (res) {
        if (typeof res === 'string') {
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
        let totalPaginas = Math.max(1, Math.ceil(res.total / registrosPorPagina));
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
                htmlPaginas += '<button class="relative z-10 inline-flex items-center bg-indigo-600 px-4 py-2 text-sm font-semibold text-white border border-gray-300 focus:z-20 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" data-pag="' + i + '">' + i + '</button>';
            } else {
                htmlPaginas += '<button class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 border border-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0" data-pag="' + i + '">' + i + '</button>';
            }
        }
        if (end < totalPaginas) {
            if (end < totalPaginas - 1) htmlPaginas += '<span class="relative inline-flex items-center px-2 py-2 text-sm font-semibold text-gray-700">...</span>';
            htmlPaginas += '<button class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 border border-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0" data-pag="' + totalPaginas + '">' + totalPaginas + '</button>';
        }
        // Actualizar paginación en ambos contenedores (móvil y desktop)
        $('#paginas-numeros').each(function(){
            $(this).html(htmlPaginas);
        });

        // Delegar evento click para los botones de página (funciona aunque se reemplace el HTML)
        $(document).off('click', '#paginas-numeros button[data-pag]');
        $(document).on('click', '#paginas-numeros button[data-pag]', function () {
            let pag = parseInt($(this).attr('data-pag'));
            if (!isNaN(pag) && pag !== paginaActual) cargarPaginaAuditoria(pag);
        });
    }, 'json');
}


$(document).ready(function () {
    // --- Botón Confirmar Masivo (solo vendedor y verificador) ---
    if (window.sessionRol === 'vendedor' || window.sessionRol === 'verificador') {
        const btnMasivo = `<button id="btn-confirmar-masivo" class="ml-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded font-semibold text-sm">Confirmar masivo</button>`;
        $('#paginacion_auditoria').append(btnMasivo);
    }

    // Handler para Confirmar Masivo
    $(document).on('click', '#btn-confirmar-masivo', function () {
        let datos = [];
        // Solo inputs de la tabla visible (página actual)
        let $filas = $('#registros_auditoria tr').not('#no-registros-row');
        if (window.sessionRol === 'vendedor') {
            $filas.each(function () {
                let $input = $(this).find('input[id^="fecha_redes_"]');
                if ($input.length && $input.val() && !$input.prop('disabled')) {
                    const id = $input.attr('id').replace('fecha_redes_', '');
                    datos.push({ id, fecha: $input.val() });
                }
            });
        } else if (window.sessionRol === 'verificador') {
            $filas.each(function () {
                let $input = $(this).find('input[id^="fecha_ingreso_cuenta_"]');
                if ($input.length && $input.val() && !$input.prop('disabled')) {
                    const id = $input.attr('id').replace('fecha_ingreso_cuenta_', '');
                    datos.push({ id, fecha: $input.val() });
                }
            });
        }
        if (datos.length === 0) {
            mostrarAlerta('No hay fechas seleccionadas para confirmar.', 'error');
            return;
        }
        mostrarDialogoConfirmacion({
            titulo: 'Confirmación masiva',
            mensaje: '¿Estás seguro de que deseas confirmar masivamente? <br>Revisa bien las fechas antes de continuar. Esta acción es irreversible.',
            textoBoton: 'Confirmar todo',
            onConfirm: function () {
                $.ajax({
                    url: window.sessionRol === 'vendedor' ? '/confirmar_redes_masivo' : '/confirmar_gerencia_masivo',
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ registros: datos }),
                    success: function (resp) {
                        if (resp.success) {
                            mostrarAlerta('¡Confirmación masiva exitosa!', 'success');
                            actualizarTablaAuditoria();
                        } else {
                            mostrarAlerta(resp.error || 'Error al confirmar masivo.', 'error');
                        }
                    },
                    error: function (xhr) {
                        mostrarAlerta('Error en el servidor: ' + (xhr.responseJSON?.error || xhr.statusText), 'error');
                    }
                });
            }
        });
    });

    // Inicial: cargar primera página
    cargarPaginaAuditoria(1, {});

    // Mostrar/ocultar botón de orden según estado
    function actualizarBotonOrden() {
        if (estadoConfirmacion === 'confirmados') {
            $('#btn-ordenar-fecha').show();
            $('#btn-confirmar-masivo').hide();
        } else {
            $('#btn-ordenar-fecha').hide();
            $('#btn-confirmar-masivo').show();
        }
    }
    actualizarBotonOrden();

    // Tabs de registros por confirmar/confirmados
    $(document).on('click', '.tab-auditoria', function () {
        $('.tab-auditoria').removeClass('bg-[#b07c40] text-white').addClass('bg-gray-300 text-gray-700');
        $(this).removeClass('bg-gray-300 text-gray-700').addClass('bg-[#b07c40] text-white');
    estadoConfirmacion = $(this).data('estado');
    actualizarBotonOrden();
    cargarPaginaAuditoria(1, {});
    // Lógica de botón de orden
    $('#btn-ordenar-fecha').on('click', function () {
        // Alternar dirección
        ordenFecha = (ordenFecha === 'desc') ? 'asc' : 'desc';
        // Cambiar icono
        $('#icono-orden').html(ordenFecha === 'desc' ? '&#10597;' : '&#10595;');

        if (ordenFecha === 'desc') {
            msg = 'Se ha ordenado de mayor a menor'
            mostrarAlerta(msg, 'success');
        } else {
            msg = 'Se ha ordenado de menor a mayor'
            mostrarAlerta(msg, 'success');
        }
        cargarPaginaAuditoria(1, {});
    });
    });

    $('#select-registros-pagina').on('change', function () {
        registrosPorPagina = parseInt($(this).val());
        cargarPaginaAuditoria(1, {});
    });

    $('#btn-buscar-rango').on('click', function () {
        const fechaDesde = $('#fecha_desde').val();
        const fechaHasta = $('#fecha_hasta').val();
        let filtros = {};
        if (fechaDesde) filtros.fecha_desde = fechaDesde;
        if (fechaHasta) filtros.fecha_hasta = fechaHasta;
        cargarPaginaAuditoria(1, filtros);
    });

    $('#btn-borrar-filtros').on('click', function () {
        $('#fecha_desde').val('');
        $('#fecha_hasta').val('');
        cargarPaginaAuditoria(1, {});
    });

    $('#btn-pag-anterior').on('click', function () {
        if (paginaActual > 1) cargarPaginaAuditoria(paginaActual - 1);
    });
    $('#btn-pag-siguiente').on('click', function () {
        cargarPaginaAuditoria(paginaActual + 1);
    });

    // Buscador general en la tabla (filtro en tiempo real)
    $('#buscador-general').on('input', function () {
        const valor = $(this).val().toLowerCase();
        let filas = $('#registros_auditoria tr').not('#no-registros-row');
        let visibles = 0;
        filas.each(function () {
            let mostrar = false;
            $(this).find('td').each(function () {
                if ($(this).text().toLowerCase().indexOf(valor) !== -1) {
                    mostrar = true;
                }
            });
            $(this).toggle(mostrar);
            if (mostrar) visibles++;
        });
        // Quitar mensaje previo si existe
        $('#no-registros-row').remove();
        // Si no hay filas visibles, mostrar mensaje
        if (visibles === 0) {
            let colCount = $('#registros_auditoria').closest('table').find('thead tr th').length || 10;
            $('#registros_auditoria').append('<tr id="no-registros-row"><td colspan="' + colCount + '" class="text-center py-8 text-gray-500">No se encontró registros.</td></tr>');
        }
    });
});

$('#btn-borrar-filtros').on('click', function () {
    $('#fecha_desde').val('');
    $('#fecha_hasta').val('');
    cargarPaginaAuditoria(1, {});
});

$('#btn-pag-anterior').on('click', function () {
    if (paginaActual > 1) {
        cargarPaginaAuditoria(paginaActual - 1);
    }
});
$('#btn-pag-siguiente').on('click', function () {
    cargarPaginaAuditoria(paginaActual + 1);
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
    let mensaje = `¿Deseas guardar la fecha <b>${fecha}</b> para el voucher? Esta acción es irreversible y quedará registrada en auditoría.`;
    mostrarDialogoConfirmacion({
        titulo: 'Confirmar edición de fecha de voucher',
        mensaje: mensaje,
        textoBoton: 'Guardar fecha',
        onConfirm: function (motivo) {
            $.ajax({
                url: '/admin/editar_fecha_voucher',
                method: 'POST',
                data: { id: id, fecha: fecha, motivo: motivo },
                success: function (resp) {
                    if (resp.success) {
                        actualizarTablaAuditoria();
                    } else {
                        alert(resp.error || 'Error al guardar fecha.');
                    }
                },
                error: function (xhr) {
                    alert('Error en el servidor: ' + (xhr.responseJSON?.error || xhr.statusText));
                }
            });
        }
    });
    // Insertar textarea de motivo solo para admin después de abrir el modal
    setTimeout(function () {
        if (window.sessionRol === 'admin') {
            var $motivoDestino = $('#motivo-admin-modal-destino');
            $motivoDestino.empty();
            $motivoDestino.append(`
                <div class='mt-4 w-full' id='motivo-admin-modal'>
                    <label for='motivo-admin' class='block text-sm font-medium text-gray-700 mb-1'>Motivo (obligatorio):</label>
                    <textarea id='motivo-admin' class='block w-full border border-gray-300 rounded px-2 py-1 text-sm focus:ring focus:ring-yellow-200 focus:border-yellow-400 resize-none' rows='2' required placeholder='Describe el motivo de la edición...'></textarea>
                </div>
            `);
        }
    }, 100);
}


function guardarFechaIngreso(id) {
    const input = document.getElementById(`fecha_ingreso_cuenta_${id}`);
    const fecha = input?.value;
    if (!fecha) {
        alert('Por favor, selecciona una fecha.');
        return;
    }
    let mensaje = `¿Deseas guardar la fecha <b>${fecha}</b> para el ingreso de dinero? Esta acción es irreversible y quedará registrada en auditoría.`;
    mostrarDialogoConfirmacion({
        titulo: 'Confirmar edición de fecha de ingreso',
        mensaje: mensaje,
        textoBoton: 'Guardar fecha',
        onConfirm: function (motivo) {
            $.ajax({
                url: '/admin/editar_fecha_ingreso',
                method: 'POST',
                data: { id: id, fecha: fecha, motivo: motivo },
                success: function (resp) {
                    if (resp.success) {
                        actualizarTablaAuditoria();
                    } else {
                        alert(resp.error || 'Error al guardar fecha.');
                    }
                },
                error: function (xhr) {
                    alert('Error en el servidor: ' + (xhr.responseJSON?.error || xhr.statusText));
                }
            });
        }
    });
    // Insertar textarea de motivo solo para admin después de abrir el modal
    setTimeout(function () {
        if (window.sessionRol === 'admin') {
            var $motivoDestino = $('#motivo-admin-modal-destino');
            $motivoDestino.empty();
            $motivoDestino.append(`
                <div class='mt-4 w-full' id='motivo-admin-modal'>
                    <label for='motivo-admin' class='block text-sm font-medium text-gray-700 mb-1'>Motivo (obligatorio):</label>
                    <textarea id='motivo-admin' class='block w-full border border-gray-300 rounded px-2 py-1 text-sm focus:ring focus:ring-yellow-200 focus:border-yellow-400 resize-none' rows='2' required placeholder='Describe el motivo de la edición...'></textarea>
                </div>
            `);
        }
    }, 100);
}

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
            $.ajax({
                url: `/confirmar_redes/${id}`,
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify({ fecha: fechaSeleccionada }),
                success: function (data) {
                    if (data.success) {
                        mostrarAlerta('¡Confirmación exitosa!', 'success');
                        actualizarTablaAuditoria();
                    } else {
                        mostrarAlerta(data.error || 'Ocurrió un error al confirmar.', 'error');
                    }
                },
                error: function (jqXHR) {
                    let msg = jqXHR.responseJSON?.error || jqXHR.statusText || 'Ocurrió un error en el servidor.';
                    mostrarAlerta(msg, 'error');
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
                success: function (data) {
                    if (data.success) {
                        mostrarAlerta('¡Confirmación exitosa!', 'success');
                        actualizarTablaAuditoria();
                    } else {
                        mostrarAlerta(data.error || 'Ocurrió un error al confirmar.', 'error');
                    }
                },
                error: function (jqXHR) {
                    let msg = jqXHR.responseJSON?.error || jqXHR.statusText || 'Ocurrió un error en el servidor.';
                    mostrarAlerta(msg, 'error');
                }
            });
        }
    });
// Alerta visual tipo login (reutilizable)
function mostrarAlerta(mensaje, tipo = 'success') {
    // Elimina alertas previas
    $('.alert-auditoria').remove();
    let color = tipo === 'success' ? 'bg-green-500' : 'bg-red-500';
    let html = `<div class="alert-auditoria fixed top-4 left-1/2 transform -translate-x-1/2 z-50 ${color} text-white px-6 py-3 rounded shadow transition-all opacity-0">${mensaje}</div>`;
    $('body').append(html);
    let $alert = $('.alert-auditoria');
    setTimeout(() => $alert.removeClass('opacity-0').addClass('opacity-100'), 50);
    setTimeout(() => {
        $alert.removeClass('opacity-100').addClass('opacity-0');
        setTimeout(() => $alert.remove(), 500);
    }, 3000);
}
}


function mostrarDialogoConfirmacion({ titulo, mensaje, textoBoton, onConfirm }) {
    const dialog = document.getElementById("dialog-confirmar");
    const title = document.getElementById("dialog-title");
    const mensajeElem = dialog.querySelector("p");
    const confirmarBtn = document.getElementById("btn-confirmar-modal");
    const cancelarBtn = document.getElementById("btn-cancelar-modal");

    // Siempre mostrar el título y mensaje
    title.innerText = titulo;
    $(mensajeElem).html(mensaje);
    confirmarBtn.innerText = textoBoton || "Confirmar";

    // Limpiar el destino del motivo
    var $motivoDestino = $('#motivo-admin-modal-destino');
    $motivoDestino.empty();

    // Insertar textarea de motivo solo para admin cuando el modal ya está visible
    dialog.addEventListener('shown', function handler() {
        dialog.removeEventListener('shown', handler);
        if (window.sessionRol === 'admin') {
            $motivoDestino.append(`
                <div class='mt-4 w-full' id='motivo-admin-modal'>
                    <label for='motivo-admin' class='block text-sm font-medium text-gray-700 mb-1'>Motivo (obligatorio):</label>
                    <textarea id='motivo-admin' class='block w-full border border-gray-300 rounded px-2 py-1 text-sm focus:ring focus:ring-yellow-200 focus:border-yellow-400 resize-none' rows='2' required placeholder='Describe el motivo de la edición...'></textarea>
                </div>
            `);
        }
    });

    // Clonar el botón para eliminar escuchadores de eventos anteriores
    const nuevoBtn = confirmarBtn.cloneNode(true);
    confirmarBtn.parentNode.replaceChild(nuevoBtn, confirmarBtn);

    nuevoBtn.addEventListener("click", () => {
        let motivo = '';
        if (window.sessionRol === 'admin') {
            motivo = document.getElementById('motivo-admin')?.value || '';
            if (!motivo.trim()) {
                alert('El motivo es obligatorio para admin.');
                document.getElementById('motivo-admin').focus();
                return;
            }
        }
        onConfirm(motivo);
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
    }, function (res) {
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
                htmlPaginas += '<button class="relative z-10 inline-flex items-center bg-indigo-600 px-4 py-2 text-sm font-semibold text-white border border-gray-300 focus:z-20 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" data-pag="' + i + '">' + i + '</button>';
            } else {
                htmlPaginas += '<button class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 border border-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0" data-pag="' + i + '">' + i + '</button>';
            }
        }
        if (end < totalPaginas) {
            if (end < totalPaginas - 1) htmlPaginas += '<span class="relative inline-flex items-center px-2 py-2 text-sm font-semibold text-gray-700">...</span>';
            htmlPaginas += '<button class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 border border-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0" data-pag="' + totalPaginas + '">' + totalPaginas + '</button>';
        }
        $('#paginas-numeros').html(htmlPaginas);
        // Click en número de página
        $('#paginas-numeros button[data-pag]').off('click').on('click', function () {
            let pag = parseInt($(this).attr('data-pag'));
            if (pag !== paginaActual) cargarPaginaAuditoria(pag);
        });
    }, 'json');
}