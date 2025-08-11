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
                </select>
            </label>`;
        } else if (tab === 'usuarios' && campo.nombre === 'contrasena') {
            html += `<label class="flex flex-col gap-1">
                <span class="text-sm font-semibold">${campo.placeholder}</span>
                <input type="password" name="${campo.nombre}" class="border rounded px-2 py-1 text-sm" required />
            </label>`;
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
