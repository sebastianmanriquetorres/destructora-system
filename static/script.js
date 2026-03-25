document.getElementById("formSolicitud").addEventListener("submit", async function(e){

e.preventDefault()

const data = {

solicitante: document.getElementById("solicitante").value,
correo: document.getElementById("correo").value,
cargo: document.getElementById("cargo").value,
fecha_inicio: document.getElementById("inicio").value,
fecha_fin: document.getElementById("fin").value,
motivo: document.getElementById("motivo").value

}

const res = await fetch("/solicitudes", {

method: "POST",
headers: {
"Content-Type": "application/json"
},

body: JSON.stringify(data)

})

const result = await res.json()

alert(JSON.stringify(result))

})