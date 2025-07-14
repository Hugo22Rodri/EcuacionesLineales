// Espera a que el contenido del documento este completamente cargado
document.addEventListener("DOMContentLoaded", function() {
    // Selecciona el elemento con la clase "boton"
    const boton = document.querySelector(".boton");

    // Agrega un efecto de sombra cuando el mouse pasa sobre el botón
    boton.addEventListener("mouseover", function() {
        boton.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.3)"; // Agrega sombra para dar un efecto elevado
    });

    // Elimina el efecto de sombra cuando el mouse sale del botón
    boton.addEventListener("mouseout", function() {
        boton.style.boxShadow = "none"; // Quita la sombra
    });
});
