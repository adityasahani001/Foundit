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
            preview.style.display = "none";
            return;
        }

        // 🔥 Validate size (max 2MB)
        if (file.size > 2 * 1024 * 1024) {
            alert("Image must be less than 2MB");
            input.value = "";
            preview.style.display = "none";
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
        const originalText = btn.innerText;

        // 🔥 Prevent multiple clicks
        if (btn.disabled) return;

        btn.innerText = "Submitting...";
        btn.disabled = true;

        const formData = new FormData();

        // ===== GET VALUES =====
        const title = document.getElementById("itemname").value.trim();
        const category = document.getElementById("category").value;
        const description = document.getElementById("description").value.trim();
        const date = document.getElementById("date").value;
        const location = document.getElementById("location").value.trim();

        // ===== VALIDATION =====
        if (!title || !category || !date || !location) {
            alert("Please fill all required fields");
            btn.innerText = originalText;
            btn.disabled = false;
            return;
        }

        // ===== APPEND DATA =====
        formData.append("title", title);
        formData.append("category", category);
        formData.append("description", description);
        formData.append("date", date);
        formData.append("location", location);
        formData.append("type", type);

        // ===== IMAGE =====
        const fileInput = document.getElementById("image");
        const file = fileInput ? fileInput.files[0] : null;

        if (file) {
            formData.append("image", file);
        }

        try {
            const res = await fetch("/items/add", {
                method: "POST",
                body: formData,
                credentials: "include"
            });

            let data = {};
            try {
                data = await res.json();
            } catch {
                data.message = "Unexpected server response";
            }

            if (res.ok && data.success) {
                alert("✅ Item submitted successfully!");

                // 🔥 Reset form
                form.reset();

                // 🔥 Clear preview
                const preview = document.getElementById("preview");
                if (preview) preview.style.display = "none";

                // 🔥 Redirect
                setTimeout(() => {
                    window.location.href = "/dashboard";
                }, 800);

            } else {
                alert(data.message || "Submission failed");
            }

        } catch (error) {
            alert("Upload failed. Try again.");
            console.error("🔥 Upload Error:", error);
        }

        btn.innerText = originalText;
        btn.disabled = false;
    });
}


// ===== AUTO INIT =====
document.addEventListener("DOMContentLoaded", () => {

    // Found item
    if (document.getElementById("foundForm")) {
        setupImagePreview("image", "preview");
        setupFormSubmit("foundForm", "found");
    }

    // Lost item
    if (document.getElementById("lostForm")) {
        setupImagePreview("image", "preview");
        setupFormSubmit("lostForm", "lost");
    }

});