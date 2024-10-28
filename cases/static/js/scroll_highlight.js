document.addEventListener('DOMContentLoaded', function() {
    const SCROLL_THRESHOLD_PERCENTAGE = 2;  // 2% of window height
    const FOOTER_ID = 'footer-contacts';

    function getOffset(element) {
        const rect = element.getBoundingClientRect();
        return rect.top + window.scrollY;
    }

    function setActiveLink() {
        const scrollPosition = window.scrollY;
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;
        console.log('Current scroll position:', scrollPosition);

        const sections = document.querySelectorAll('.section');
        // sections.forEach(section)
        // {
        //     console.log(section);
        // }
        // console.log(`Sections: ${sections}`);

        const navLinks = document.querySelectorAll('.nav-link');

        let currentSectionId = '';

        // Check if we're at the bottom of the page
        const scrollThreshold = windowHeight * (SCROLL_THRESHOLD_PERCENTAGE / 100);


        // if (scrollPosition + windowHeight >= documentHeight - 50) { // 50px threshold
        if (scrollPosition + windowHeight >= documentHeight - scrollThreshold) {
            // currentSectionId = 'footer-contacts';
            currentSectionId = FOOTER_ID;
            // console.log('At bottom of page, setting Contacts active');
            console.log(`At bottom of page, setting ${FOOTER_ID} active`);
            // Remove 'active' class from all links and add it only to Contacts
            navLinks.forEach((link) => {
                link.classList.remove('active');
                // if (link.getAttribute('href') === '#footer-contacts') {
                if (link.getAttribute('href') === `#${FOOTER_ID}`) {
                    link.classList.add('active');
                }
            });
            return; // Exit the function early as we've handled the bottom case
        }

        // If we're at the top of the page, set Home as active
        if (scrollPosition < 100) { // Adjust this value if needed
            navLinks.forEach((link) => link.classList.remove('active'));
            navLinks[0].classList.add('active');
            console.log('Home set as active due to top of page');
            return; // Exit the function early as we've handled the top case
        }

        // For all other cases, find the current section
        sections.forEach((section) => {
            const sectionTop = getOffset(section) - 100; // Adjust this value based on your header height
            const sectionBottom = sectionTop + section.offsetHeight;
            console.log(`Section ${section.id}: top=${sectionTop}, bottom=${sectionBottom}, offsetTop=${section.offsetTop}, offsetHeight=${section.offsetHeight}`);

            if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                currentSectionId = section.id;
                console.log('Current section:', currentSectionId);
            }
        });

        // Set active class on the corresponding nav link
        navLinks.forEach((link) => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSectionId}`) {
                link.classList.add('active');
                console.log('Active link set to:', link.textContent);
            }
        });
    }

    // Set Home as active by default
    document.querySelector('.nav-link').classList.add('active');
    console.log('Home set as active by default');

    // Update active link on scroll
    window.addEventListener('scroll', setActiveLink);

    // Update active link on page load (in case of refresh on a specific section)
    setActiveLink();

    // Listen for HTMX events
    document.body.addEventListener('htmx:afterSwap', function(event) {
        console.log('HTMX afterSwap event triggered');
        // Use requestAnimationFrame to ensure DOM is fully updated
        requestAnimationFrame(setActiveLink);
    });

    document.body.addEventListener('htmx:afterSettle', function(event) {
        console.log('HTMX afterSettle event triggered');
        setActiveLink();
    });
});


// document.addEventListener('DOMContentLoaded', function() {
//     function getOffset(element) {
//         const rect = element.getBoundingClientRect();
//         return rect.top + window.scrollY;
//     }
//
//     function setActiveLink() {
//         const scrollPosition = window.scrollY;
//         console.log('Current scroll position:', scrollPosition);
//
//         // Re-query the sections to ensure we have the latest DOM state
//         const sections = document.querySelectorAll('.section');
//         const navLinks = document.querySelectorAll('.nav-link');
//
//         let currentSectionId = '';
//
//         // Find the current section
//         sections.forEach((section) => {
//             const sectionTop = getOffset(section) - 100; // Adjust this value based on your header height
//             const sectionBottom = sectionTop + section.offsetHeight;
//             console.log(`Section ${section.id}: top=${sectionTop}, bottom=${sectionBottom}, offsetTop=${section.offsetTop}, offsetHeight=${section.offsetHeight}`);
//
//             if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
//                 currentSectionId = section.id;
//                 console.log('Current section:', currentSectionId);
//             }
//         });
//
//         // Set active class on the corresponding nav link
//         navLinks.forEach((link) => {
//             link.classList.remove('active');
//             if (link.getAttribute('href') === `#${currentSectionId}`) {
//                 link.classList.add('active');
//                 console.log('Active link set to:', link.textContent);
//             }
//         });
//
//         // If we're at the top of the page, set Home as active
//         if (scrollPosition < 100) { // Adjust this value if needed
//             navLinks[0].classList.add('active');
//             console.log('Home set as active due to top of page');
//         }
//     }
//
//     // Set Home as active by default
//     document.querySelector('.nav-link').classList.add('active');
//     console.log('Home set as active by default');
//
//     // Update active link on scroll
//     window.addEventListener('scroll', setActiveLink);
//
//     // Update active link on page load (in case of refresh on a specific section)
//     setActiveLink();
//
//     // Listen for HTMX events
//     document.body.addEventListener('htmx:afterSwap', function(event) {
//         console.log('HTMX afterSwap event triggered');
//         // Use requestAnimationFrame to ensure DOM is fully updated
//         requestAnimationFrame(setActiveLink);
//     });
//
//     document.body.addEventListener('htmx:afterSettle', function(event) {
//         console.log('HTMX afterSettle event triggered');
//         setActiveLink();
//     });
// });

