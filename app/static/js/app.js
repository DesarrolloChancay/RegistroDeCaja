let botonActual, fechaInputActual;

async function cargarDatos() {
    const res = await fetch('/api/auditoria');
    const datos = await res.json();

    const tbody = document.getElementById('tablaAuditoria');
    tbody.innerHTML = '';

    datos.forEach((row, index) => {
        const tr = document.createElement('tr');
        tr.classList.add('bg-white', 'border-b');

        const inputFecha = document.createElement('input');
        inputFecha.type = 'date';
        inputFecha.className = 'border border-gray-300 rounded px-2 py-1';
        inputFecha.value = row.fecha_voucher_confirmacion || '';
        inputFecha.id = `fecha-confirmacion-${index}`;

        const btnEstado = document.createElement('button');
        btnEstado.innerText = row.confirmacion_redes;
        btnEstado.className = 'text-xs px-3 py-1 rounded-full font-semibold';

        if (row.confirmacion_redes === 'Confirmado') {
            btnEstado.classList.add('bg-green-600', 'text-white');
            btnEstado.disabled = true;
        } else {
            btnEstado.classList.add('bg-blue-600', 'text-white');
            btnEstado.setAttribute('command', 'show-modal');
            btnEstado.setAttribute('commandfor', 'dialog-confirmar');

            btnEstado.addEventListener('click', (e) => {
                const fechaValor = inputFecha.value;
                if (!fechaValor) {
                    e.preventDefault(); // evita abrir el modal
                    alert("⚠️ Debes ingresar la fecha antes de confirmar.");
                    return;
                }
                botonActual = btnEstado;
                fechaInputActual = inputFecha;
            });
        }

        tr.innerHTML = `
            <td class="px-4 py-3">${row.fecha_voucher}</td>
            <td class="px-4 py-3">${row.fecha_registro}</td>
            <td class="px-4 py-3">${row.transaccion}</td>
            <td class="px-4 py-3">${row.empresa}</td>
            <td class="px-4 py-3">$${row.monto.toFixed(2)}</td>
            <td class="px-4 py-3">${row.detalle}</td>
            <td class="px-4 py-3" id="td-fecha-${index}"></td>
            <td class="px-4 py-3" id="td-btn-${index}"></td>
            <td class="px-4 py-3"><input type="date" class="border border-gray-300 rounded px-2 py-1" value="${row.fecha_ingreso_dinero || ''}" /></td>
            <td class="px-4 py-3"><span class="bg-yellow-400 text-white text-xs px-3 py-1 rounded-full">${row.confirmar_pago}</span></td>
        `;

        tbody.appendChild(tr);
        document.getElementById(`td-fecha-${index}`).appendChild(inputFecha);
        document.getElementById(`td-btn-${index}`).appendChild(btnEstado);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    cargarDatos();

    document.getElementById('btn-confirmar-modal').addEventListener('click', () => {
        if (!botonActual || !fechaInputActual) return;

        botonActual.innerText = 'Confirmado';
        botonActual.classList.remove('bg-blue-600');
        botonActual.classList.add('bg-green-600');
        botonActual.disabled = true;

        // Opcional: cerrar modal manualmente
        document.querySelector('dialog#dialog-confirmar').close();

        // Aquí podrías hacer un POST a backend para guardar
        console.log(`✅ Confirmado con fecha ${fechaInputActual.value}`);
    });
});
