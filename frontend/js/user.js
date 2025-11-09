async function loadUser() {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
        const res = await fetch("http://127.0.0.1:5000/me", {
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (res.ok) {
            const data = await res.json();
            document.getElementById("UsernameDisplay").innerText = `Welcome, ${data.username}`;
        }
    } catch (err) {
        console.error("Failed to load user, err")
    }
}
loadUser();
