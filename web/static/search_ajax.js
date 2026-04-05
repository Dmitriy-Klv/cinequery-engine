document.addEventListener("DOMContentLoaded", function() {
    const searchForm = document.getElementById("searchForm");
    const tableBody = document.getElementById("movieTableBody");

    if (searchForm) {
        searchForm.addEventListener("submit", async function(e) {
            e.preventDefault();

            tableBody.style.opacity = "0.5";

            const formData = new FormData(searchForm);

            try {
                const response = await fetch("/search", {
                    method: "POST",
                    body: formData
                });

                const html = await response.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newTableBody = doc.getElementById("movieTableBody");

                if (newTableBody) {
                    tableBody.innerHTML = newTableBody.innerHTML;
                }
            } catch (error) {
                console.error("Fetch error:", error);
            } finally {
                tableBody.style.opacity = "1";
            }
        });
    }
});