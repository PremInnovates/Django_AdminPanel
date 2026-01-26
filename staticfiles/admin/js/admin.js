document.addEventListener("DOMContentLoaded", function () {

    // Create toggle button
    const toggle = document.createElement("div");
    toggle.className = "theme-toggle";
    toggle.innerHTML = "🌙";
    document.body.appendChild(toggle);

    // Load saved theme
    const savedTheme = localStorage.getItem("admin-theme");
    if (savedTheme === "light") {
        document.body.classList.add("light-mode");
        toggle.innerHTML = "☀️";
    }

    // Toggle click
    toggle.addEventListener("click", function () {
        document.body.classList.toggle("light-mode");

        if (document.body.classList.contains("light-mode")) {
            localStorage.setItem("admin-theme", "light");
            toggle.innerHTML = "☀️";
        } else {
            localStorage.setItem("admin-theme", "dark");
            toggle.innerHTML = "🌙";
        }
    });
});
