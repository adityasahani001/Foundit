// ===== LOAD ITEMS (GENERIC) =====
async function loadItems(containerId, showActions = false) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = "Loading...";

    try {
        const res = await fetch("/items/all", {
            credentials: "include"
        });

        const data = await res.json();
        const items = data.items || [];

        container.innerHTML = "";

        if (items.length === 0) {
            container.innerHTML = "<p>No items found.</p>";
            return;
        }

        const isHome = window.location.pathname === "/";

        const displayItems = isHome
            ? items.slice(-5).reverse()
            : items.slice().reverse();

        displayItems.forEach((item) => {
            const div = document.createElement("div");
            div.className = "item-card";

            div.innerHTML = `
                <h3>${item.title}</h3>
                <p>${item.description || ""}</p>

                <p><strong>Category:</strong> ${item.category || "-"}</p>
                <p><strong>Location:</strong> ${item.location || "-"}</p>
                <p><strong>Date:</strong> ${item.date || "-"}</p>
                <p><strong>Status:</strong> ${item.type || "found"}</p>

                ${
                    showActions && !isHome ? `
                    <div style="margin-top:10px;">
                        <a href="/edit-item?id=${item.id}">Edit</a> |
                        <a href="#" onclick="deleteItem('${item.id}')">Delete</a>
                    </div>
                    ` : ""
                }
            `;

            container.appendChild(div);
        });

    } catch (error) {
        container.innerHTML = "<p>Error loading items.</p>";
        console.error("Load Items Error:", error);
    }
}


// ===== LOAD USER ITEMS (PROFILE / DASHBOARD CARDS) =====
async function loadMyItems(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = "Loading your items...";

    try {
        const res = await fetch("/items/my-items", {
            credentials: "include"
        });

        const data = await res.json();
        const items = data.items || [];

        container.innerHTML = "";

        if (items.length === 0) {
            container.innerHTML = "<p>No items posted yet.</p>";
            return;
        }

        items.reverse().forEach((item) => {
            const div = document.createElement("div");
            div.className = "item-card";

            div.innerHTML = `
                <h3>${item.title}</h3>
                <p>${item.description || ""}</p>

                <p><strong>Category:</strong> ${item.category}</p>
                <p><strong>Location:</strong> ${item.location}</p>
                <p><strong>Date:</strong> ${item.date}</p>
                <p><strong>Status:</strong> ${item.type}</p>

                <div style="margin-top:10px;">
                    <a href="/edit-item?id=${item.id}">Edit</a> |
                    <a href="#" onclick="deleteItem('${item.id}')">Delete</a>
                </div>
            `;

            container.appendChild(div);
        });

    } catch (error) {
        container.innerHTML = "<p>Error loading your items.</p>";
        console.error("Load My Items Error:", error);
    }
}


// ===== DELETE ITEM =====
async function deleteItem(itemId) {
    const confirmDelete = confirm("Are you sure you want to delete this item?");
    if (!confirmDelete) return;

    try {
        const res = await fetch(`/items/delete/${itemId}`, {
            method: "DELETE",
            credentials: "include"
        });

        const data = await res.json();

        alert(data.message || "Item deleted successfully");
        location.reload();

    } catch (error) {
        alert("Error deleting item");
        console.error("Delete Error:", error);
    }
}


// ===== DASHBOARD TABLE =====
async function loadDashboard() {
    const table = document.getElementById("itemsTable");
    if (!table) return;

    table.innerHTML = "<tr><td colspan='5'>Loading...</td></tr>";

    try {
        const res = await fetch("/items/my-items", {
            credentials: "include"
        });

        const data = await res.json();
        const items = data.items || [];

        table.innerHTML = "";

        if (items.length === 0) {
            table.innerHTML = "<tr><td colspan='5'>No items found</td></tr>";
            return;
        }

        items.reverse().forEach((item) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${item.title}</td>
                <td>${item.category}</td>
                <td>${item.date}</td>
                <td>${item.type}</td>
                <td>
                    <a href="/edit-item?id=${item.id}">Edit</a> |
                    <a href="#" onclick="deleteItem('${item.id}')">Delete</a>
                </td>
            `;

            table.appendChild(row);
        });

    } catch (error) {
        table.innerHTML = "<tr><td colspan='5'>Error loading data</td></tr>";
        console.error("Dashboard Error:", error);
    }
}


// ===== AUTO RUN BASED ON PAGE =====
document.addEventListener("DOMContentLoaded", () => {

    const path = window.location.pathname;

    // Homepage → latest items
    if (path === "/" && document.getElementById("items-container")) {
        loadItems("items-container", false);
    }

    // View items page
    else if (document.getElementById("items-container")) {
        loadItems("items-container", true);
    }

    // Profile / My Items section
    if (document.getElementById("my-items-container")) {
        loadMyItems("my-items-container");
    }

    // Dashboard table
    if (document.getElementById("itemsTable")) {
        loadDashboard();
    }

});