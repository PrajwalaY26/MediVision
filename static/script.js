// Default users
const users = {
    "yas@gmail.com": "123",
    "hash@gmail.com": "143"
};

// Login Form Handler
document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const email = document.getElementById("loginEmail").value;
            const password = document.getElementById("loginPassword").value;

            if (users[email] && users[email] === password) {
                alert("Login successful!");
                window.location.href = "dashboard.html"; // Redirect to dashboard
            } else {
                document.getElementById("loginError").textContent = "Invalid email or password.";
            }
        });
    }

    // Signup Form Handler
    const signupForm = document.getElementById("signupForm");
    if (signupForm) {
        signupForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const email = document.getElementById("signupEmail").value;
            const password = document.getElementById("signupPassword").value;

            if (users[email]) {
                document.getElementById("signupError").textContent = "User already exists.";
            } else {
                users[email] = password;
                alert("Signup successful! You can now log in.");
                window.location.href = "index.html"; // Redirect to login
            }
        });
    }
});
