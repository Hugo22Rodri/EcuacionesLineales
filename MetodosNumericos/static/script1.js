document.addEventListener('DOMContentLoaded', () => {
    // Mostrar/Ocultar pasos
    const btnPasos = document.getElementById('togglePasos');
    const pasosContainer = document.querySelector('.pasos-container');
    if (btnPasos && pasosContainer) {
        pasosContainer.style.display = 'none'; // Oculta los pasos por defecto
        btnPasos.addEventListener('click', () => {
            if (pasosContainer.style.display === 'none') {
                pasosContainer.style.display = 'block';
                btnPasos.textContent = 'Ocultar Pasos';
            } else {
                pasosContainer.style.display = 'none';
                btnPasos.textContent = 'Mostrar/Ocultar Pasos';
            }
        });
    }

    // Mostrar/Ocultar gráficos
    document.querySelectorAll('.toggle-grafico').forEach(boton => {
        const grafico = boton.closest('.seccion').querySelector('.grafico-container');
        if (grafico) {
            grafico.style.display = 'none'; // Oculta el gráfico por defecto
            boton.addEventListener('click', () => {
                if (grafico.style.display === 'none') {
                    grafico.style.display = 'block';
                    boton.textContent = 'Ocultar Gráfico';
                } else {
                    grafico.style.display = 'none';
                    // Cambia el texto según el tipo de gráfico
                    if (boton.textContent.includes('Comparación')) {
                        boton.textContent = 'Mostrar Comparación con Solución Exacta';
                    } else {
                        boton.textContent = 'Mostrar Gráfico de Convergencia';
                    }
                }
            });
        }
    });
});