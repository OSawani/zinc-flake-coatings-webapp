<script>
document.addEventListener("DOMContentLoaded", function() {
    var tableContainer = document.querySelector(".table-container");

    function checkScroll() {
        if (tableContainer.scrollWidth > tableContainer.clientWidth) {
            tableContainer.classList.add("scrollable");
        } else {
            tableContainer.classList.remove("scrollable");
        }
    }

    tableContainer.addEventListener("scroll", checkScroll);
    window.addEventListener("resize", checkScroll);
    checkScroll();
});
</script>
