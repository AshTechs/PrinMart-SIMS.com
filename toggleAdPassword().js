function togglePasswords() {
    const passwordInput = document.getElementById("password");
    const repeatPasswordInput = document.getElementById("repeat-password");
    const toggleIcon = document.querySelector(".toggle-password");

    if (passwordInput.type === "password" && repeatPasswordInput.type === "password") {
        passwordInput.type = "text";
        repeatPasswordInput.type = "text";
        toggleIcon.classList.remove("fa-eye-slash");
        toggleIcon.classList.add("fa-eye");
    } else {
        passwordInput.type = "password";
        repeatPasswordInput.type = "password";
        toggleIcon.classList.remove("fa-eye");
        toggleIcon.classList.add("fa-eye-slash");
    }
}
