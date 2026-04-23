// ===== GET ITEM ID FROM URL =====
const params = new URLSearchParams(window.location.search);
const itemId = params.get("id");


// ===== LOAD ITEM DATA =====
async function loadItem() {
    try {
        // 🔒 Check session first
        const sessionRes = await fetch("/auth/check-session", {
            credentials: "include"
        });
        const sessionData = await sessionRes.json();

        if (!sessionData.logged_in) {
            window.location.href = "/login";
            return;
        }

        const res = await fetch("/items/my-items", {
            credentials: "include"
        });

        let data = {};
        try {
            data = await res.json();
        } catch {
            alert("Invalid server response");
            return;
        }

        const items = data.items || [];

        const item = items.find(i => i.id === itemId);

        if (!item) {
            alert("Item not found");
            window.location.href = "/dashboard";
            return;
        }

        // 🔥 Fill form
        document.getElementById("title").value = item.title || "";
        document.getElementById("category").value = item.category || "";
        document.getElementById("description").value = item.description || "";
        document.getElementById("date").value = item.date || "";
        document.getElementById("location").value = item.location || "";

    } catch (error) {
        console.error("Load error:", error);
        alert("Error loading item");
    }
}


// ===== UPDATE ITEM =====
async function updateItem(e) {
    e.preventDefault();

    const btn = document.querySelector("#editForm button");

    // 🔥 Prevent double click
    if (btn.disabled) return;

    if (!itemId) {
        alert("Invalid item ID");
        return;
    }

    btn.innerText = "Updating...";
    btn.disabled = true;

    const updatedData = {
        title: document.getElementById("title").value.trim(),
        category: document.getElementById("category").value.trim(),
        description: document.getElementById("description").value.trim(),
        date: document.getElementById("date").value,
        location: document.getElementById("location").value.trim()
    };

    // 🔥 Basic validation
    if (!updatedData.title || !updatedData.category || !updatedData.date || !updatedData.location) {
        alert("Please fill all required fields");
        btn.innerText = "Update Item";
        btn.disabled = false;
        return;
    }

    try {
        const res = await fetch(`/items/update/${itemId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify(updatedData)
        });

        let data = {};
        try {
            data = await res.json();
        } catch {
            data.message = "Unexpected server response";
        }

        if (res.ok && data.success) {
            alert("Item updated successfully");
            window.location.href = "/dashboard";
        } else {
            alert(data.message || "Update failed");
        }

    } catch (error) {
        console.error("Update error:", error);
        alert("Error updating item");
    }

    btn.innerText = "Update Item";
    btn.disabled = false;
}


// ===== INIT =====
document.addEventListener("DOMContentLoaded", () => {

    // 🔥 Check ID first
    if (!itemId) {
        alert("Invalid request");
        window.location.href = "/dashboard";
        return;
    }

    loadItem();

    const form = document.getElementById("editForm");
    if (form) {
        form.addEventListener("submit", updateItem);
    }
});