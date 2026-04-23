// ===== LOAD ITEMS =====
async function loadItems() {
    const container = document.getElementById("items-container");

    if (!container) return;

    // 🔥 Loading state
    container.innerHTML = `<div class="loading">Loading items...</div>`;

    try {
        const res = await fetch("/items/all");
        const data = await res.json();

        const items = data.items || [];

        container.innerHTML = "";

        // 🔥 Empty state
        if (items.length === 0) {
            container.innerHTML = `<p class="loading">No items found</p>`;
            return;
        }

        // 🔥 Show latest 6
        items.slice(0, 6).forEach(item => {

            const card = document.createElement("div");
            card.className = "item-card";

            card.innerHTML = `
                ${item.image_url ? `<img src="${item.image_url}" alt="item">` : ""}
                <h3>${item.title}</h3>
                <p><strong>Location:</strong> ${item.location}</p>
                <p><strong>Date:</strong> ${item.date}</p>
                <button onclick="viewItem('${item.id}')">View Details</button>
            `;

            container.appendChild(card);
        });

    } catch (err) {
        console.error("Error loading items:", err);

        container.innerHTML = `
            <p class="loading" style="color:red;">
                Failed to load items
            </p>
        `;
    }
}


// ===== VIEW ITEM (FOR MODAL - NEXT STEP READY) =====
function viewItem(id) {
    // 🔥 for now simple redirect
    // later we will convert this to modal popup

    window.location.href = `/view_items?id=${id}`;
}


// ===== INIT =====
document.addEventListener("DOMContentLoaded", loadItems);