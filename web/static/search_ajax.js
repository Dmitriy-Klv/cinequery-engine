document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.getElementById('movieTableBody');
    const paginationControls = document.getElementById('paginationControls');
    const searchForm = document.getElementById('searchForm');
    const clearBtn = document.getElementById('clearBtn');

    const handleSearch = async (formData, append = false) => {
        try {
            if (!append) tableBody.style.opacity = "0.5";

            const response = await fetch('/search', { method: 'POST', body: formData });
            const text = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(text, 'text/html');

            const newRows = doc.querySelectorAll('#movieTableBody tr');
            const newPagination = doc.getElementById('paginationControls');

            if (!append) {
                tableBody.innerHTML = '';
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }

            if (newRows.length > 0 && !newRows[0].innerText.includes("No movies found")) {
                newRows.forEach(row => tableBody.appendChild(row));
            } else if (!append) {
                tableBody.innerHTML = '<tr><td colspan="4" class="text-center py-5 text-muted">No movies found.</td></tr>';
            }

            if (paginationControls) {
                paginationControls.innerHTML = newPagination ? newPagination.innerHTML : '';
            }
        } catch (err) {
            console.error(err);
        } finally {
            tableBody.style.opacity = "1";
        }
    };

    if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            handleSearch(new FormData(searchForm), false);
        });
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            if (searchForm) searchForm.reset();
            tableBody.innerHTML = '<tr><td colspan="4" class="text-center py-5 text-muted">No movies found.</td></tr>';
            if (paginationControls) paginationControls.innerHTML = '';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    document.addEventListener('click', (e) => {
        const btn = e.target.closest('#loadMoreBtn');
        if (btn) {
            btn.innerText = "LOADING...";
            btn.disabled = true;

            const formData = new FormData();
            formData.append('page', btn.dataset.page);
            formData.append('keyword', btn.dataset.keyword);
            formData.append('category', btn.dataset.category);
            formData.append('year_start', btn.dataset.start);
            formData.append('year_end', btn.dataset.end);

            handleSearch(formData, true);
        }
    });
});