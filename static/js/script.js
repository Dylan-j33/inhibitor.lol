document.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch("/api/data");
    const data = await response.json();
    document.getElementById("data").innerText = `Message: ${data.message}, Rang: ${data.rank}`;
});
