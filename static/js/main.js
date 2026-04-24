// ===== GLOBAL USER =====
let currentUserId = null;

// ===== FETCH CURRENT USER =====
async function fetchCurrentUser() {
    try {
        const res = await fetch("/auth/check-session", {
            credentials: "include"
        });

        const data = await res.json();

        if (data.logged_in) {
            currentUserId = data.user_id;
        }
    } catch (err) {
        console.error("User fetch error:", err);
    }
}

// ===== LOAD ITEMS (PUBLIC) =====
async function loadItems(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = `<div class="loading">Loading items...</div>`;

    try {
        const res = await fetch("/items/all", {
            credentials: "include"
        });

        const data = await res.json();
        const items = data.items || [];

        container.innerHTML = "";

        if (items.length === 0) {
            container.innerHTML = "<p class='loading'>No items found.</p>";
            return;
        }

        const isHome = window.location.pathname === "/";

        const displayItems = isHome
            ? items.slice(-6).reverse()
            : items.slice().reverse();

        displayItems.forEach((item) => {
            const div = document.createElement("div");
            div.className = "item-card";

            const isOwner = currentUserId === item.user_id;

            div.innerHTML = `
                ${item.image_url ? `<img src="${item.image_url}" alt="item">` : ""}
                
                <h3>${item.title}</h3>
                <p>${item.description || ""}</p>

                <p><strong>Category:</strong> ${item.category || "-"}</p>
                <p><strong>Location:</strong> ${item.location || "-"}</p>
                <p><strong>Date:</strong> ${item.date || "-"}</p>
                <p><strong>Reported By:</strong> ${item.user_name || "Unknown"}</p>

                <span class="badge ${item.type}">
                    ${(item.type || "found").toUpperCase()}
                </span>

                <div style="margin-top:10px;">
                    <button onclick="viewItem('${item.id}')">View</button>
                    ${
    isOwner
    ? `
    | <a href="/edit-item?id=${item.id}">Edit</a>
    | <a href="#" onclick="deleteItem('${item.id}', this)">Delete</a>
    `
    : `
    | <button onclick="claimItem('${item.id}')">Claim</button>
    `
}

                </div>
            `;

            container.appendChild(div);
        });

    } catch (error) {
        container.innerHTML = "<p class='loading' style='color:red;'>Error loading items.</p>";
        console.error("Load Items Error:", error);
    }
}

// ===== VIEW ITEM =====
function viewItem(id) {
    openModal(id);
}

// ===== DROPDOWN =====
function toggleMenu(event) {
    if (event) event.stopPropagation();

    const menu = document.getElementById("dropdown");
    if (!menu) return;

    menu.style.display =
        menu.style.display === "block" ? "none" : "block";
}

// Close dropdown outside
document.addEventListener("click", function(e) {
    const menu = document.getElementById("dropdown");
    const profile = document.querySelector(".nav-user");

    if (!menu || !profile) return;

    if (!profile.contains(e.target)) {
        menu.style.display = "none";
    }
});

// ===== LOAD MY ITEMS (PROFILE) =====
async function loadMyItems(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = `<div class="loading">Loading your items...</div>`;

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
                ${item.image_url ? `<img src="${item.image_url}">` : ""}

                <h3>${item.title}</h3>
                <p>${item.description || ""}</p>

                <p><strong>Category:</strong> ${item.category}</p>
                <p><strong>Location:</strong> ${item.location}</p>
                <p><strong>Date:</strong> ${item.date}</p>

                <span class="badge ${item.type}">
                    ${item.type.toUpperCase()}
                </span>

                <div style="margin-top:10px;">
                    <a href="/edit-item?id=${item.id}">Edit</a> |
                    <a href="#" onclick="deleteItem('${item.id}', this)">Delete</a>
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
async function deleteItem(itemId, element) {
    const confirmDelete = confirm("Are you sure you want to delete this item?");
    if (!confirmDelete) return;

    try {
        const res = await fetch(`/items/delete/${itemId}`, {
            method: "DELETE",
            credentials: "include"
        });

        const data = await res.json();

        alert(data.message || "Item deleted");

        if (element) {
            const card = element.closest(".item-card");
            if (card) card.remove();
        }

    } catch (error) {
        alert("Error deleting item");
        console.error("Delete Error:", error);
    }
}

// ===== DASHBOARD TABLE =====
async function loadDashboard() {
    const table = document.getElementById("itemsTable");
    if (!table) return;

    table.innerHTML = "<tr><td colspan='6'>Loading...</td></tr>";

    try {
        const res = await fetch("/items/my-items", {
            credentials: "include"
        });

        const data = await res.json();
        const items = data.items || [];

        table.innerHTML = "";

        if (items.length === 0) {
            table.innerHTML = "<tr><td colspan='6'>No items found</td></tr>";
            return;
        }

        items.reverse().forEach((item) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>
                    ${
                        item.image_url
                        ? `<img src="${item.image_url}" class="item-img" onclick="openModal('${item.id}')">`
                        : "-"
                    }
                </td>
                <td>${item.title}</td>
                <td>${item.category}</td>
                <td>${item.date}</td>
                <td>
                    <span class="badge ${item.type}">
                        ${item.type.toUpperCase()}
                    </span>
                </td>
                <td>
                    <a href="/edit-item?id=${item.id}">Edit</a> |
                    <a href="#" onclick="deleteItem('${item.id}')">Delete</a>
                </td>
            `;

            table.appendChild(row);
        });

    } catch (error) {
        table.innerHTML = "<tr><td colspan='6'>Error loading data</td></tr>";
        console.error("Dashboard Error:", error);
    }
}

// ===== AUTO INIT =====
document.addEventListener("DOMContentLoaded", async () => {

    await fetchCurrentUser(); // 🔥 VERY IMPORTANT

    const path = window.location.pathname;

    const itemsContainer = document.getElementById("items-container");
    const myItemsContainer = document.getElementById("my-items-container");
    const dashboardTable = document.getElementById("itemsTable");

    if (path === "/" && itemsContainer) {
        loadItems("items-container");
    } 
    else if (itemsContainer) {
        loadItems("items-container");
    }

    if (myItemsContainer) {
        loadMyItems("my-items-container");
    }

    if (dashboardTable) {
        loadDashboard();
    }
});

// ===== MODAL =====
async function openModal(itemId) {
    try {
        const res = await fetch("/items/all");
        const data = await res.json();

        const item = data.items.find(i => i.id === itemId);
        if (!item) return;

        document.getElementById("modalImg").src = item.image_url || "";
        document.getElementById("modalTitle").innerText = item.title;
        document.getElementById("modalDesc").innerText = item.description || "";
        document.getElementById("modalCategory").innerText = item.category;
        document.getElementById("modalLocation").innerText = item.location;
        document.getElementById("modalDate").innerText = item.date;

        if (item.user_id) {
            const userRes = await fetch(`/user/${item.user_id}`);
            const userData = await userRes.json();

            if (userData.success) {
                document.getElementById("modalUser").innerText = userData.user.fullname;
                document.getElementById("modalPhone").innerText = userData.user.phone;
            }
        }

        document.getElementById("itemModal").style.display = "flex";

    } catch (err) {
        console.error("Modal error:", err);
    }
}

function closeModal() {
    document.getElementById("itemModal").style.display = "none";
}

window.addEventListener("click", function(e) {
    const modal = document.getElementById("itemModal");
    if (e.target === modal) {
        modal.style.display = "none";
    }
});

async function claimItem(itemId) {
    const confirmClaim = confirm("Do you want to claim this item?");
    if (!confirmClaim) return;

    try {
        const res = await fetch(`/items/claim/${itemId}`, {
            method: "POST",
            credentials: "include"
        });

        const data = await res.json();

        if (data.success) {
            alert("✅ Claim request sent!");
        } else {
            alert(data.message || "Failed");
        }

    } catch (err) {
        alert("Error sending claim");
        console.error(err);
    }
}