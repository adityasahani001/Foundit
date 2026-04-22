// ===== IMAGE PREVIEW =====
function setupImagePreview(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);

    if (!input || !preview) return;

    input.addEventListener("change", function () {
        const file = input.files[0];

        if (!file) {
            preview.src = "";
            preview.style.display = "none";
            return;
        }

        // 🔥 Validate type
        if (!file.type.startsWith("image/")) {
            alert("Only image files are allowed!");
            input.value = "";
            return;
        }

        // 🔥 Validate size (max 2MB)
        if (file.size > 2 * 1024 * 1024) {
            alert("Image size must be less than 2MB");
            input.value = "";
            return;
        }

        const reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = "block";
        };

        reader.readAsDataURL(file);
    });
}


// ===== HANDLE FORM SUBMISSION =====
function setupFormSubmit(formId, type = "found") {
    const form = document.getElementById(formId);

    if (!form) return;

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const btn = form.querySelector("button");
        btn.innerText = "Submitting...";
        btn.disabled = true;

        const formData = new FormData();

        formData.append("title", document.getElementById("itemname").value);
        formData.append("category", document.getElementById("category").value);
        formData.append("description", document.getElementById("description").value);
        formData.append("date", document.getElementById("date").value);
        formData.append("location", document.getElementById("location").value);
        formData.append("type", type);

        const file = document.getElementById("image").files[0];
        if (file) {
            formData.append("image", file);
        }

        try {
            const res = await fetch("/items/add", {
                method: "POST",
                body: formData,
                credentials: "include"   // ✅ VERY IMPORTANT
            });

            const data = await res.json();

            if (res.ok) {
                alert(data.message || "Item submitted!");
                window.location.href = "/dashboard";   // ✅ better UX
            } else {
                alert(data.message || "Submission failed");
            }

        } catch (error) {
            alert("Upload failed. Try again.");
            console.error(error);
        }

        btn.innerText = "Submit";
        btn.disabled = false;
    });
}


// ===== AUTO INIT =====
document.addEventListener("DOMContentLoaded", () => {

    // Found item page
    if (document.getElementById("foundForm")) {
        setupImagePreview("image", "preview");
        setupFormSubmit("foundForm", "found");
    }

    // Lost item page
    if (document.getElementById("lostForm")) {
        setupImagePreview("image", "preview");
        setupFormSubmit("lostForm", "lost");
    }

});