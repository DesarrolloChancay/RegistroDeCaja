// --- Tabla de registros de auditoría (admin) ---
function cargarTablaRegistrosAuditoriaAdmin(pagina = 1) {
    let por_pagina = parseInt($('#select-registros-pagina-admin').val()) || 10;
    let fecha_desde = $('#fecha_desde_admin').val();
    let fecha_hasta = $('#fecha_hasta_admin').val();
    let busqueda = $('#buscador-general-admin').val();
    // Ordenamiento
    let orden_dir = window.ordenFechaAdmin || 'desc';
    let campoOrden = (window.sessionRol === 'admin' || window.sessionRol === 'verificador') ? 'fecha_confirmacion_gerencia' : 'fecha_confirmacion_redes';
    $.post('/admin/registrosauditoria/tabla', {
        pagina: pagina,
        por_pagina: por_pagina,
        fecha_desde: fecha_desde,
        fecha_hasta: fecha_hasta,
        busqueda: busqueda
    }, function (res) {
        $('#registros_auditoria_admin').html(res.html);
        // Paginación
        let desde = res.total === 0 ? 0 : ((pagina - 1) * por_pagina) + 1;
        let hasta = Math.min(pagina * por_pagina, res.total);
        $('#pag-desde-admin').text(desde);
        $('#pag-hasta-admin').text(hasta);
        $('#pag-total-admin').text(res.total);
        // Botones
        $('#btn-pag-anterior-admin').prop('disabled', pagina <= 1);
        $('#btn-pag-siguiente-admin').prop('disabled', !res.hay_mas);
        // Números de página
        let totalPaginas = Math.ceil(res.total / por_pagina);
        let htmlPaginas = '';
        if (totalPaginas < 1) totalPaginas = 1;
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
        // Si no hay páginas, mostrar al menos la 1
        if (htmlPaginas === '') {
            htmlPaginas = '<button class="relative z-10 inline-flex items-center bg-indigo-600 px-4 py-2 text-sm font-semibold text-white border border-gray-300" data-pag="1">1</button>';
        }
        $('#paginas-numeros-admin').html(htmlPaginas);
        // Click en número de página
        $('#paginas-numeros-admin button[data-pag]').off('click').on('click', function () {
            let pag = parseInt($(this).attr('data-pag'));
            if (pag !== pagina) cargarTablaRegistrosAuditoriaAdmin(pag);
        });
    }, 'json');
}

$(document).ready(function () {
    // Estado de pestaña (por confirmar/confirmados)
    let estadoConfirmacionAdmin = 'por_confirmar';
    let ordenFechaAdmin = 'desc';

    // Mostrar/ocultar botón de orden según estado
    function actualizarBotonOrdenAdmin() {
        if (estadoConfirmacionAdmin === 'confirmados') {
            $('#btn-ordenar-fecha-admin').show();
        } else {
            $('#btn-ordenar-fecha-admin').hide();
        }
    }
    actualizarBotonOrdenAdmin();

    // Si tienes tabs, actualiza estadoConfirmacionAdmin y llama actualizarBotonOrdenAdmin() en el click
    $(document).on('click', '.tab-auditoria', function () {
        estadoConfirmacionAdmin = $(this).data('estado');
        actualizarBotonOrdenAdmin();
        cargarTablaRegistrosAuditoriaAdmin(1);
    });

    // Lógica de botón de orden
    $('#btn-ordenar-fecha-admin').on('click', function () {
        ordenFechaAdmin = (ordenFechaAdmin === 'desc') ? 'asc' : 'desc';
        window.ordenFechaAdmin = ordenFechaAdmin;
        $('#icono-orden-admin').html(ordenFechaAdmin === 'desc' ? '&#10597;' : '&#10595;');
        let msg = ordenFechaAdmin === 'desc' ? 'Se ha ordenado de mayor a menor' : 'Se ha ordenado de menor a mayor';
        if (typeof mostrarAlerta === 'function') {
            mostrarAlerta(msg, 'success');
        } else {
            // fallback simple
            alert(msg);
        }
        cargarTablaRegistrosAuditoriaAdmin(1);
    });
    // Inicial: cargar primera página
    if ($('#registros_auditoria_admin').length) {
        cargarTablaRegistrosAuditoriaAdmin(1);
        // Filtros
        $('#select-registros-pagina-admin').on('change', function () { cargarTablaRegistrosAuditoriaAdmin(1); });
        $('#btn-buscar-rango-admin').on('click', function () { cargarTablaRegistrosAuditoriaAdmin(1); });
        $('#btn-borrar-filtros-admin').on('click', function () {
            $('#fecha_desde_admin').val('');
            $('#fecha_hasta_admin').val('');
            $('#buscador-general-admin').val('');
            cargarTablaRegistrosAuditoriaAdmin(1);
        });
        // Corregido: calcular página actual correctamente
        let paginaActual = 1;
        // Guardar la página actual en cada carga
        function setPaginaActual(pag) { paginaActual = pag; }
        // Sobrescribir cargarTablaRegistrosAuditoriaAdmin para guardar página
        const cargarOriginal = cargarTablaRegistrosAuditoriaAdmin;
        cargarTablaRegistrosAuditoriaAdmin = function (pag) {
            setPaginaActual(pag);
            cargarOriginal(pag);
        };
        $('#btn-pag-anterior-admin').on('click', function () {
            if (paginaActual > 1) cargarTablaRegistrosAuditoriaAdmin(paginaActual - 1);
        });
        $('#btn-pag-siguiente-admin').on('click', function () {
            let por_pagina = parseInt($('#select-registros-pagina-admin').val()) || 10;
            let total = parseInt($('#pag-total-admin').text()) || 0;
            let totalPaginas = Math.ceil(total / por_pagina);
            if (paginaActual < totalPaginas) cargarTablaRegistrosAuditoriaAdmin(paginaActual + 1);
        });
        // Buscador general (en tiempo real)
        $('#buscador-general-admin').on('input', function () {
            cargarTablaRegistrosAuditoriaAdmin(1);
        });
    }
});
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
                    if (resp.success) { location.reload(); } else { alert(resp.error || 'Error al guardar'); }
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
                    if (resp.success) { location.reload(); } else { alert(resp.error || 'Error al guardar'); }
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
// admin.js - Lógica AJAX para mantenimiento admin
// --- Modal reutilizable para agregar entidades ---
function abrirModalAgregar(tab, campos) {
    $('#form-modal-agregar').data('tab', tab);
    $('#modal-titulo').text('Agregar ' + tab.replace('_', ' '));
    let html = '';
    campos.forEach(function (campo) {
        if (tab === 'usuarios' && campo.nombre === 'rol') {
            html += `<label class="flex flex-col gap-1">
                <span class="text-sm font-semibold">Rol</span>
                <select name="rol" class="border rounded px-2 py-1 text-sm" required>
                  <option value="">Selecciona un rol</option>
                  <option value="admin">Admin</option>
                  <option value="verificador">Verificador</option>
                  <option value="vendedor">Vendedor</option>
                  <option value="contabilidad">Contabilidad</option>
                </select>
            </label>`;
        } else if (tab === 'usuarios' && campo.nombre === 'contrasena') {
            html += `<label class="flex flex-col gap-1">
                <span class="text-sm font-semibold">${campo.placeholder}</span>
                <div class="relative w-full max-w-sm">
                    <input type="password" id="input-${campo.nombre}_new" name="${campo.nombre}" class="border rounded px-2 py-1 text-sm w-100" required />
                    <button
                        type="button"
                        id="togglePassword"
                        class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-500 hover:text-gray-700"
                    >
                        <!-- Ícono del ojito -->
                        <svg id="eyeOpen" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        <svg id="eyeClosed" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 hidden" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.477 0-8.268-2.943-9.542-7a9.956 9.956 0 012.104-3.362M9.88 9.88a3 3 0 104.24 4.24M6.1 6.1l11.8 11.8" />
                        </svg>
                    </button>
                </div>
            </label>
            <script>
                $("#togglePassword").on("click", function () {
                    const password = $("#input-contrasena_new");
                    const eyeOpen = $("#eyeOpen");
                    const eyeClosed = $("#eyeClosed");

                    if (password.attr("type") === "password") {
                        password.attr("type", "text");
                        eyeOpen.addClass("hidden");
                        eyeClosed.removeClass("hidden");
                    } else {
                        password.attr("type", "password");
                        eyeOpen.removeClass("hidden");
                        eyeClosed.addClass("hidden");
                    }
                });
            </script>
            `;
        } else {
            html += `<label class="flex flex-col gap-1">
                <span class="text-sm font-semibold">${campo.placeholder}</span>
                <input type="text" name="${campo.nombre}" class="border rounded px-2 py-1 text-sm" required />
            </label>`;
        }
    });
    if (tab === 'usuarios' && !campos.some(c => c.nombre === 'rol')) {
        html += `<label class="flex flex-col gap-1">
                <span class="text-sm font-semibold">Rol</span>
                <select name="rol" class="border rounded px-2 py-1 text-sm" required>
                  <option value="">Selecciona un rol</option>
                  <option value="admin">Admin</option>
                  <option value="verificador">Verificador</option>
                  <option value="vendedor">Vendedor</option>
                </select>
            </label>`;
    }
    $('#modal-campos').html(html);
    $('#modal-agregar').removeClass('hidden').addClass('flex');
}

function cerrarModalAgregar() {
    $('#modal-agregar').addClass('hidden').removeClass('flex');
    $('#form-modal-agregar')[0].reset();
}

// Inicialización y AJAX
$(document).ready(function () {
    function cargar_tabla(tab, pagina = 1) {
        $.get(`/admin/${tab}/tabla`, { pagina: pagina }, function (html) {
            $('#tab-content').html(html);
        });
    }

    // Botones de tabs
    $('.tab-btn').on('click', function () {
        let tab = $(this).data('tab');
        cargar_tabla(tab, 1);
    });

    // Cargar la primera tabla por defecto
    cargar_tabla('empresas', 1);

    // Delegar eventos para paginación
    $('#tab-content').on('click', '.btn-pag', function () {
        let tab = $(this).data('tab');
        let pag = $(this).data('pag');
        cargar_tabla(tab, pag);
    });

    // Submit del modal
    $(document).on('submit', '#form-modal-agregar', function (e) {
        e.preventDefault();
        let tab = $(this).data('tab');
        let form = $(this);
        $.post(`/admin/${tab}/agregar`, form.serialize(), function (resp) {
            if (resp.success) {
                cerrarModalAgregar();
                cargar_tabla(tab, 1);
            } else {
                alert(resp.error || 'Error al agregar');
            }
        }, 'json');
    });
});
