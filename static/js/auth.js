// ===== LOGIN FUNCTION =====
async function handleLogin(e) {
    e.preventDefault();

    const btn = document.getElementById("loginBtn");
    const msg = document.getElementById("msg");

    btn.innerText = "Logging in...";
    btn.disabled = true;
    msg.innerText = "";

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const res = await fetch("/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password }),
            credentials: "include"   // ✅ REQUIRED for session
        });

        const data = await res.json();

        if (res.ok) {
            msg.style.color = "green";
            msg.innerText = "Login successful! Redirecting...";

            setTimeout(() => {
                window.location.href = "/dashboard";
            }, 1000);
        } else {
            msg.style.color = "red";
            msg.innerText = data.message || "Login failed";
        }

    } catch (error) {
        msg.style.color = "red";
        msg.innerText = "Server error. Try again.";
        console.error(error);
    }

    btn.innerText = "Login";
    btn.disabled = false;
}

<<<<<<< HEAD
=======
function toggleMenu() {
    const menu = document.getElementById("dropdown");
    menu.style.display = menu.style.display === "block" ? "none" : "block";
}

>>>>>>> bba30b3 (Initial commit)

// ===== REGISTER FUNCTION =====
async function handleRegister(e) {
    e.preventDefault();

    const btn = document.getElementById("registerBtn");
    const msg = document.getElementById("msg");

    btn.innerText = "Creating account...";
    btn.disabled = true;
    msg.innerText = "";

    const fullname = document.getElementById("fullname").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const password = document.getElementById("password").value;
    const confirm = document.getElementById("confirm").value;

    // validation
    if (password !== confirm) {
        msg.style.color = "red";
        msg.innerText = "Passwords do not match!";
        btn.innerText = "Register";
        btn.disabled = false;
        return;
    }

    if (password.length < 6) {
        msg.style.color = "red";
        msg.innerText = "Password must be at least 6 characters.";
        btn.innerText = "Register";
        btn.disabled = false;
        return;
    }

    try {
        const res = await fetch("/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                fullname,
                email,
                phone,
                password
            }),
            credentials: "include"   // ✅ optional but good
        });

        const data = await res.json();

        if (res.ok) {
            msg.style.color = "green";
            msg.innerText = "Account created! Redirecting...";

            setTimeout(() => {
                window.location.href = "/login";
            }, 1200);
        } else {
            msg.style.color = "red";
            msg.innerText = data.message || "Registration failed";
        }

    } catch (error) {
        msg.style.color = "red";
        msg.innerText = "Server error. Try again.";
        console.error(error);
    }

    btn.innerText = "Register";
    btn.disabled = false;
}


// ===== LOGOUT FUNCTION =====
function logout() {
    fetch("/auth/logout", {
<<<<<<< HEAD
        method: "GET",
        credentials: "include"
    })
    .then(() => {
        window.location.href = "/login";
    })
    .catch(err => console.error(err));
=======
    method: "GET",
    credentials: "include"
})
.then(() => {
    window.location.href = "/login";
});
>>>>>>> bba30b3 (Initial commit)
}


// ===== CHECK SESSION (OPTIONAL) =====
async function checkSession() {
    try {
        const res = await fetch("/auth/check-session", {
            credentials: "include"
        });

        const data = await res.json();

        if (!data.logged_in) {
            window.location.href = "/login";
        }
    } catch (err) {
        console.error(err);
    }
}


// ===== AUTO ATTACH EVENTS =====
document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");

    if (loginForm) {
        loginForm.addEventListener("submit", handleLogin);
    }

    if (registerForm) {
        registerForm.addEventListener("submit", handleRegister);
    }

});