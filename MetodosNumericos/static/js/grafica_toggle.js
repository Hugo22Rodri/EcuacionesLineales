document.addEventListener('DOMContentLoaded', function() {
    const toggleGraficaBtn = document.getElementById('toggleGraficaBtn');
    const graficaImg = document.getElementById('graficaImg');

    if (toggleGraficaBtn && graficaImg) {
        toggleGraficaBtn.addEventListener('click', function() {
            graficaImg.classList.toggle('mostrar');
            toggleGraficaBtn.textContent = graficaImg.classList.contains('mostrar') ? 'Ocultar Gráfica' : 'Mostrar Gráfica';
        });
    }
});