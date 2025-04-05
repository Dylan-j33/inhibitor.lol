document.addEventListener("DOMContentLoaded", () => {
    const parts = window.location.pathname.split("/");
    const pseudo = parts[1];
    const tagline = parts[2];

    fetch(`/internal/rank/${pseudo}/${tagline}`)
        .then(res => res.json())
        .then(data => {
            if (data.detail) {
                document.getElementById("title").textContent = data.detail;
            } else {
                document.getElementById("title").textContent = `${pseudo} - Rang SoloQ`;
                document.getElementById("rank").textContent =
                    `${data.tier} ${data.rank} - ${data.lp} LP (${data.wins}V / ${data.losses}D)`;
            }
        })
        .catch(err => {
            document.getElementById("title").textContent = "Erreur lors de la récupération des données.";
        });
});
