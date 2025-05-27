document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("codeForm");
    const loading = document.getElementById("loading");
    const commentedCode = document.getElementById("commentedCode");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();
        
        // Show loading text
        loading.classList.remove("hidden");
        commentedCode.innerText = "";

        const code = document.getElementById("code").value;
        const language = document.getElementById("language").value;

        const response = await fetch("/api/comment", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code, language })
        });

        const data = await response.json();
        
        // Hide loading text
        loading.classList.add("hidden");

        if (data.commented_code) {
            commentedCode.innerText = data.commented_code;
        } else {
            commentedCode.innerText = "Error generating comments. Please try again.";
        }
    });
});
