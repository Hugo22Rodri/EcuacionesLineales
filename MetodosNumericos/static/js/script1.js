document.addEventListener('DOMContentLoaded', () => {
    // Mostrar/Ocultar pasos
    const btnPasos = document.getElementById('togglePasos');
    const pasosContainer = document.querySelector('.pasos-container');
    if (btnPasos && pasosContainer) {
        pasosContainer.classList.remove('visible');
        btnPasos.addEventListener('click', () => {
            pasosContainer.classList.toggle('visible');
            btnPasos.textContent = pasosContainer.classList.contains('visible') ? 'Ocultar Pasos' : 'Mostrar/Ocultar Pasos';
        });
    }

    // Mostrar/Ocultar gráficos
    document.querySelectorAll('.toggle-grafico').forEach(boton => {
        const grafico = boton.closest('.seccion').querySelector('.grafico-container');
        if (grafico) {
            grafico.classList.remove('visible');
            boton.addEventListener('click', () => {
                grafico.classList.toggle('visible');
                if (grafico.classList.contains('visible')) {
                    boton.textContent = 'Ocultar Gráfico';
                } else {
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
