// (function() {
//     let scrollToTopBtn;
//
//     function initScrollToTop() {
//         scrollToTopBtn = document.getElementById('scroll-to-top');
//         if (!scrollToTopBtn) {
//             console.error('Scroll to top button not found');
//             return;
//         }
//
//         window.addEventListener('scroll', toggleScrollToTopButton);
//         toggleScrollToTopButton(); // Initial check
//     }
//
//     function toggleScrollToTopButton() {
//         if (!scrollToTopBtn) return;
//
//         if (window.pageYOffset > 300) {
//             scrollToTopBtn.style.display = 'flex';
//         } else {
//             scrollToTopBtn.style.display = 'none';
//         }
//     }
//
//     // Initialize on DOMContentLoaded
//     document.addEventListener('DOMContentLoaded', initScrollToTop);
//
//     // Reinitialize after HTMX content swaps
//     document.body.addEventListener('htmx:load', initScrollToTop);
// })();

(function() {
    let scrollToTopBtn;

    function initScrollToTop() {
        scrollToTopBtn = document.getElementById('scroll-to-top');
        if (!scrollToTopBtn) {
            console.error('Scroll to top button not found');
            return;
        }

        window.addEventListener('scroll', toggleScrollToTopButton);
        toggleScrollToTopButton(); // Initial check
    }

    function toggleScrollToTopButton() {
        if (!scrollToTopBtn) return;

        if (window.pageYOffset > 300) {
            scrollToTopBtn.style.display = 'block';
        } else {
            scrollToTopBtn.style.display = 'none';
        }
    }

    // Initialize on DOMContentLoaded
    document.addEventListener('DOMContentLoaded', initScrollToTop);

    // Reinitialize after HTMX content swaps
    document.body.addEventListener('htmx:load', initScrollToTop);

    // Your existing scroll highlight code goes here
    // ...

})();