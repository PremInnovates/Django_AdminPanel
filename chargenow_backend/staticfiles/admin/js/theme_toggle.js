const toggle = document.getElementById("themeToggle");

toggle.addEventListener("change", () => {
    document.body.classList.toggle("dark");
    document.body.classList.toggle("light");
});
