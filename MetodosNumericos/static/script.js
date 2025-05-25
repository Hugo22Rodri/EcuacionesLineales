document.addEventListener("DOMContentLoaded", function() {
    const boton = document.querySelector(".boton");

    boton.addEventListener("mouseover", function() {
        boton.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.3)";
    });

    boton.addEventListener("mouseout", function() {
        boton.style.boxShadow = "none";
    });
});
