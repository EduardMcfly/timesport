const fila = document.querySelector(".contenedor-carousel");
const tarjetas = document.querySelectorAll(".tarjeta");

const flechaIzquierda = document.getElementById("flecha-izquierda");
const flechaDerecha = document.getElementById("flecha-derecha");

// ? ----- ----- Paginacion ----- -----
const numeroPaginas = Math.ceil(tarjetas.length / 5);
for (let i = 0; i < numeroPaginas; i++) {
  const indicador = document.createElement("button");

  if (i === 0) {
    indicador.classList.add("activo");
  }

  document.querySelector(".indicadores").appendChild(indicador);
  indicador.addEventListener("click", (e) => {
    fila.scrollLeft = i * fila.offsetWidth;

    document.querySelector(".indicadores .activo").classList.remove("activo");
    e.target.classList.add("activo");
  });
}

// ? ----- ----- Hover ----- -----
tarjetas.forEach((tarjeta) => {
  tarjeta.addEventListener("mouseenter", (e) => {
    const elemento = e.currentTarget;
    setTimeout(() => {
      tarjetas.forEach((tarjeta) => tarjeta.classList.remove("hover"));
      elemento.classList.add("hover");
    }, 300);
  });
});
