// Get all tables on the page
var tables = document.querySelectorAll('table');

// Iterate through each table
tables.forEach(function(table) {
    // Find the expand row and not-today rows within this table
    var expandRow = table.querySelector('.expand');
    var notTodayRows = table.querySelectorAll('.not-today');

    // Add click event listener to the expand row
    expandRow.addEventListener('click', function() {
        // Rickroll the user by redirecting to the YouTube video
        window.location.href = 'https://cn.bing.com/';
    });
});