document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("searchForm");
    if (!form) return;

    form.addEventListener("submit", async function(e) {
        e.preventDefault();

        const msg = document.getElementById("msg");
        const resultsDiv = document.getElementById("results");

        msg.innerText = "Searching...";
        msg.style.color = "#6366f1";
        resultsDiv.innerHTML = `<div class="loading">Searching items...</div>`;

        // ===== GET VALUES =====
        const keyword = document.getElementById("keyword").value.trim().toLowerCase();
        const category = document.getElementById("category").value;
        const location = document.getElementById("location").value.trim().toLowerCase();
        const type = document.getElementById("type").value;

        try {
            const res = await fetch("/items/all", {
                credentials: "include"
            });

            const data = await res.json();
            const items = data.items || [];

            // ===== FILTER LOGIC =====
            const filtered = items.filter(item => {
                return (
                    (!keyword || item.title?.toLowerCase().includes(keyword)) &&
                    (!category || item.category === category) &&
                    (!location || item.location?.toLowerCase().includes(location)) &&
                    (!type || item.type === type)
                );
            });

            resultsDiv.innerHTML = "";

            // ===== NO RESULT =====
            if (filtered.length === 0) {
                msg.style.color = "red";
                msg.innerText = "No matching items found.";
                resultsDiv.innerHTML = `<p class="loading">Try different filters</p>`;
                return;
            }

            // ===== SUCCESS =====
            msg.style.color = "green";
            msg.innerText = `${filtered.length} item(s) found`;

            // ===== RENDER =====
            filtered.reverse().forEach(item => {
                const div = document.createElement("div");
                div.className = "item-card";

                div.innerHTML = `
                    ${item.image_url ? `<img src="${item.image_url}" alt="item">` : ""}

                    <h3>${item.title}</h3>
                    <p>${item.description || ""}</p>

                    <p><strong>Category:</strong> ${item.category || "-"}</p>
                    <p><strong>Location:</strong> ${item.location || "-"}</p>
                    <p><strong>Date:</strong> ${item.date || "-"}</p>

                    <span class="badge ${item.type}">
                        ${(item.type || "found").toUpperCase()}
                    </span>

                    <div style="margin-top:10px;">
                        <button onclick="viewItem('${item.id}')">View Details</button>
                    </div>
                `;

                resultsDiv.appendChild(div);
            });

        } catch (error) {
            msg.style.color = "red";
            msg.innerText = "Error fetching data.";
            resultsDiv.innerHTML = `<p class="loading">Server error</p>`;
            console.error("Search Error:", error);
        }
    });

});


// ===== VIEW ITEM (MODAL READY) =====
function viewItem(id) {
    // 🔥 currently redirect
    // next: modal popup
    window.location.href = `/view_items?id=${id}`;
}