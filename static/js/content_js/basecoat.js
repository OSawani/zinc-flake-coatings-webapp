<script>
document.addEventListener("DOMContentLoaded", function() {
    var tableContainers = document.querySelectorAll(".table-container");

    function checkScroll() {
        tableContainers.forEach(function(tableContainer) {
            if (tableContainer.scrollWidth > tableContainer.clientWidth) {
                tableContainer.classList.add("scrollable");
            } else {
                tableContainer.classList.remove("scrollable");
            }
        });
    }

    tableContainers.forEach(function(tableContainer) {
        tableContainer.addEventListener("scroll", checkScroll);
    });
    window.addEventListener("resize", checkScroll);
    checkScroll();
});
</script>
