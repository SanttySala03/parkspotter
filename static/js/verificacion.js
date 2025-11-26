document.getElementById("btn-save").addEventListener("click", async () => {
    const tipo = document.getElementById("tipo").value;
    const documento = document.getElementById("documento").value;
    const telefono = document.getElementById("telefono").value;
    const terminos = document.getElementById("terminos").checked;

    if (!terminos) {
        return alert("Debes aceptar la política de datos.");
    }

    const user_id = localStorage.getItem("user_id");

    const resp = await fetch("/verificacion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tipo_usuario: tipo, documento, telefono, user_id })
    });

    const data = await resp.json();

    if (data.success) {
        window.location.href = "/menu";
    }
});
