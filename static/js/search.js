document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("searchForm");
    if (!form) return;

    form.addEventListener("submit", async function(e) {
        e.preventDefault();

        const msg = document.getElementById("msg");
        const resultsDiv = document.getElementById("results");

        msg.innerText = "Searching...";
        resultsDiv.innerHTML = "";

        const keyword = document.getElementById("keyword").value.toLowerCase();
        const category = document.getElementById("category").value;
        const location = document.getElementById("location").value.toLowerCase();
        const type = document.getElementById("type").value;

        try {
            const res = await fetch("/items/all", {
                credentials: "include"   // ✅ session support
            });

            const data = await res.json();
            const items = data.items || [];   // ✅ FIXED

            const filtered = items.filter(item => {
                return (
                    (!keyword || item.title?.toLowerCase().includes(keyword)) &&
                    (!category || item.category === category) &&
                    (!location || item.location?.toLowerCase().includes(location)) &&
                    (!type || item.type === type)
                );
            });

            if (filtered.length === 0) {
                msg.style.color = "red";
                msg.innerText = "No matching items found.";
                return;
            }

            msg.style.color = "green";
            msg.innerText = `${filtered.length} item(s) found`;

            filtered.reverse().forEach(item => {
                const div = document.createElement("div");
                div.className = "item-card";

                div.innerHTML = `
                    <h3>${item.title}</h3>
                    <p>${item.description || ""}</p>
                    <p><strong>Category:</strong> ${item.category}</p>
                    <p><strong>Location:</strong> ${item.location}</p>
                    <p><strong>Date:</strong> ${item.date}</p>
                    <p><strong>Status:</strong> ${item.type}</p>

                    ${
                        item.image_url ? `<img src="${item.image_url}" style="width:100%;max-width:200px;margin-top:10px;">` : ""
                    }
                `;

                resultsDiv.appendChild(div);
            });

        } catch (error) {
            msg.style.color = "red";
            msg.innerText = "Error fetching data.";
            console.error(error);
        }
    });

});