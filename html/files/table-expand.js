// Get all tables on the page
var tables = document.querySelectorAll('table');

// Iterate through each table
tables.forEach(function(table) {
	// Find the expand row and not-today rows within this table
	var expandRow = table.querySelector('.expand');
	var notTodayRows = table.querySelectorAll('.not-today');

	// Hide the expand row if there is only one not-today row
	if (notTodayRows.length === 1) {
		expandRow.style.display = 'none';
		notTodayRows[0].style.display = '';
	} else {
		// Hide the expand row if there are no not-today rows
		if (notTodayRows.length === 0) {
			expandRow.style.display = 'none';
		}

		// Initialize all not-today rows to be hidden
		for (var i = 0; i < notTodayRows.length; i++) {
			notTodayRows[i].style.display = 'none';
		}

		// Add click event listener to the expand row
		expandRow.addEventListener('click', function() {
			// Toggle visibility of not-today rows
			for (var j = 0; j < notTodayRows.length; j++) {
				notTodayRows[j].style.display = notTodayRows[j].style.display === 'none' ? '' : 'none';
			}

			// Toggle expand/collapse text in the expand row
			var expandTh = this.querySelector('th');
			expandTh.textContent = expandTh.textContent === '+' ? '−' : '+';
		});
	}
});