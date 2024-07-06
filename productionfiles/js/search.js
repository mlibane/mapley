// static/js/search.js
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('recipe-search');
    const suggestionsList = document.getElementById('search-suggestions');

    searchInput.addEventListener('input', debounce(function() {
        const query = this.value;
        if (query.length < 3) {
            suggestionsList.innerHTML = '';
            return;
        }

        fetch(`/api/search-suggestions/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                suggestionsList.innerHTML = data.suggestions
                    .map(suggestion => `<li>${suggestion}</li>`)
                    .join('');
            });
    }, 300));
});

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}