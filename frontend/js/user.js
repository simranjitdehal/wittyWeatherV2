// async function loadUser() {
//     const token = localStorage.getItem("token");
//     if (!token) return;

//     try {
//         const res = await fetch("http://127.0.0.1:5000/me", {
//             headers: { "Authorization": `Bearer ${token}` }
//         });

//         if (res.ok) {
//             const data = await res.json();
//             document.getElementById("UsernameDisplay").innerText = `Welcome, ${data.username}`;
//         }
//     } catch (err) {
//         console.error("Failed to load user, err")
//     }
// }
// loadUser();

document.addEventListener("DOMContentLoaded", async () => {
    console.log("✅ user.js running – testing /me");

    const token = localStorage.getItem("token");
    // console.log("Token in storage:", token); 

    if (!token) {
        alert("No token found → redirecting to login.html");
        window.location.href = "login.html";
        return;
    }

    try {
        const res = await fetch("https://wittyweatherv2-production.up.railway.app/api/me", {
            headers: { Authorization: `Bearer ${token}` },
        });

        console.log("Response status:", res.status);

        if (res.ok) {
            const data = await res.json();
            // console.log("Fetched user:", data);
            document.getElementById("UsernameDisplay").innerText =
                `Welcome, ${data.username}`;
        } else {
            console.warn("Invalid/expired token → clearing & redirecting");
            localStorage.removeItem("token");
            window.location.href = "login.html";
        }
    } catch (err) {
        console.error("Fetch failed:", err);
        alert("Backend may be down or CORS is blocking the request.");
    }
});

