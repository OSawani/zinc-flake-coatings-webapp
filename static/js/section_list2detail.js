document.addEventListener("DOMContentLoaded", function () {
        if (window.location.hash) {
            const hash = window.location.hash.substring(1); // Remove the #
            const element = document.getElementById(hash);
            if (element) {
                const button = element.querySelector('.accordion-button');
                if (button) {
                    button.click();
                }
                // Add a slight delay to ensure the DOM is fully loaded
                setTimeout(function() {
                    // Calculate the offset for the sticky navbar
                    const offset = 100; // Adjust this value based on your navbar height
                    const elementPosition = element.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - offset;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }, 300); // Adjust the delay time if necessary
            }
        }
    });