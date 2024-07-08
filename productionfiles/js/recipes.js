document.addEventListener('DOMContentLoaded', function() {
    // Handle tag rendering
    const tagContainers = document.querySelectorAll('.tags-container');
    tagContainers.forEach(container => {
        const tagsString = container.dataset.tags;
        if (tagsString) {
            const tags = tagsString.split(',').map(tag => tag.trim());
            
            tags.forEach(tag => {
                const span = document.createElement('span');
                span.className = 'inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2';
                span.textContent = tag.startsWith('#') ? tag : `#${tag}`;
                container.appendChild(span);
            });
        }
    });

    // Lazy loading for images
    if ("IntersectionObserver" in window) {
        const lazyImages = document.querySelectorAll("img.lazy");
        let lazyImageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    let lazyImage = entry.target;
                    lazyImage.src = lazyImage.dataset.src;
                    lazyImage.classList.remove("lazy");
                    lazyImageObserver.unobserve(lazyImage);
                }
            });
        });

        lazyImages.forEach(function(lazyImage) {
            lazyImageObserver.observe(lazyImage);
        });
    }
});