// Wait for the HTML document to fully load before running scripts
document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    // Grab all elements once to save browser processing power.
    const form = document.getElementById('search-form');
    const input = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const statusMsg = document.getElementById('status-message');
    const resultsContainer = document.getElementById('results-container');
    const resultsBody = document.getElementById('results-body');
    const downloadBtn = document.getElementById('download-btn');

    // Store the latest API response for the download feature
    let currentData = null;

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent the page from refreshing
        
        const query = input.value.trim();
        if (!query) return;

        // Set UI to Loading State
        searchBtn.disabled = true;
        statusMsg.textContent = 'Searching...';
        statusMsg.className = 'status-loading';
        statusMsg.classList.remove('hidden');
        resultsContainer.classList.add('hidden');
        resultsBody.innerHTML = '';

        try {
            // Make the API Call to our Flask backend
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });

            const data = await response.json();

            // Handle non-200 responses
            if (!response.ok) {
                throw new Error(data.error || 'Failed to fetch results.');
            }

            // Render Success State
            currentData = data; // Save for download
            renderResults(data.results);
            statusMsg.classList.add('hidden');
            resultsContainer.classList.remove('hidden');

        } catch (error) {
            // Render Error State
            statusMsg.textContent = error.message;
            statusMsg.className = 'status-error';
        } finally {
            // Re-enable the search button regardless of success/failure
            searchBtn.disabled = false;
        }
    });

    // Helper function to inject rows into the table
    function renderResults(results) {
        // Handle empty results gracefully
        if (results.length === 0) {
            resultsBody.innerHTML = '<tr><td colspan="3">No organic results found.</td></tr>';
            return;
        }

        // Create and append a row for each result
        results.forEach(result => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${result.position || '-'}</td>
                <td>
                    <a href="${result.url}" target="_blank" rel="noopener noreferrer">
                        <strong>${escapeHTML(result.title)}</strong>
                    </a>
                </td>
                <td>${escapeHTML(result.snippet || '')}</td>
            `;
            resultsBody.appendChild(tr);
        });
    }

    // Handle JSON download
    downloadBtn.addEventListener('click', () => {
        if (!currentData) return;
        
        // Convert JS object to formatted JSON string and create a Blob file
        const blob = new Blob([JSON.stringify(currentData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        // Create a temporary anchor link to trigger the download
        const a = document.createElement('a');
        a.href = url;
        a.download = 'results.json';
        document.body.appendChild(a);
        a.click();
        
        // Clean up memory and DOM
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });

    // Security helper to prevent XSS injection when rendering text into HTML
    function escapeHTML(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }
});