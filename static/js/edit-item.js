// ===== GET ITEM ID FROM URL =====
const params = new URLSearchParams(window.location.search);
const itemId = params.get("id");

// ===== LOAD ITEM DATA =====
async function loadItem() {
  try {
    const res = await fetch("/items/my-items", {
      credentials: "include"
    });

    const data = await res.json();
    const items = data.items || [];

    const item = items.find(i => i.id === itemId);

    if (!item) {
      alert("Item not found");
      window.location.href = "/dashboard";
      return;
    }

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

  if (!itemId) {
    alert("Invalid item ID");
    return;
  }

  const updatedData = {
    title: document.getElementById("title").value.trim(),
    category: document.getElementById("category").value.trim(),
    description: document.getElementById("description").value.trim(),
    date: document.getElementById("date").value,
    location: document.getElementById("location").value.trim()
  };

  try {
    const res = await fetch(`/items/update/${itemId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: "include",
      body: JSON.stringify(updatedData)   // 🔥 IMPORTANT
    });

    const data = await res.json();

    if (data.success) {
      alert("Item updated successfully");
      window.location.href = "/dashboard";
    } else {
      alert(data.message || "Update failed");
    }

  } catch (error) {
    console.error("Update error:", error);
    alert("Error updating item");
  }
}


// ===== INIT =====
document.addEventListener("DOMContentLoaded", () => {
  loadItem();

  const form = document.getElementById("editForm");
  form.addEventListener("submit", updateItem);
});