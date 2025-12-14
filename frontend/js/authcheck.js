document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");

    fetch("/api/check-auth", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
        .then(res => res.json())
        .then(data => {
            if (!data.authenticated) {
                window.location.href = "login.html";
            } else {
                const userDiv = document.getElementById("UsernameDisplay");
                if (userDiv) userDiv.textContent = data.username;
            }
        })
        .catch(() => {
            window.location.href = "login.html";
        });
});
