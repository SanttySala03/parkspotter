console.log("script.js cargado correctamente");

// -------------------------------------------
//  Animación entre Login y Registro
// -------------------------------------------
const container = document.querySelector(".container");

const btnRegister = document.getElementById("btn-register");
const btnSignIn = document.getElementById("btn-sign-in");

if (btnRegister && btnSignIn && container) {
    btnRegister.addEventListener("click", () => {
        container.classList.add("toggle");
    });

    btnSignIn.addEventListener("click", () => {
        container.classList.remove("toggle");
    });
}

// -------------------------------------------
//  LOGIN
// -------------------------------------------
const formLogin = document.getElementById("form-login");

if (formLogin) {
    formLogin.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        if (!email || !password) {
            alert("Por favor llene todos los campos.");
            return;
        }

        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (!data.success) {
                alert(data.message || "Credenciales incorrectas");
                return;
            }

            // Guardar user_id en localStorage
            localStorage.setItem("user_id", data.user_id);

            // Si NO está verificado → ir a verificación
            if (!data.verificado) {
                window.location.href = "/verificacion";
                return;
            }

            // Si YA está verificado → ir al menú
            window.location.href = "/menu";

        } catch (err) {
            console.error(err);
            alert("Error de conexión con el servidor.");
        }
    });
}

// -------------------------------------------
//  REGISTRO
// -------------------------------------------
const formRegister = document.getElementById("form-register");

if (formRegister) {
    formRegister.addEventListener("submit", async (e) => {
        e.preventDefault();

        const name = document.getElementById("reg-name").value.trim();
        const email = document.getElementById("reg-email").value.trim();
        const password = document.getElementById("reg-password").value.trim();

        if (!name || !email || !password) {
            alert("Por favor complete todos los campos de registro.");
            return;
        }

        try {
            const response = await fetch("/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, email, password })
            });

            const data = await response.json();

            if (data.success) {
                alert("Registro exitoso");
                container.classList.remove("toggle"); // regresar al login
            } else {
                alert(data.message || "Error en el registro");
            }
        } catch (err) {
            console.error(err);
            alert("Error de conexión con el servidor.");
        }
    });
}
