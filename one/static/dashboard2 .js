// Function to fetch data from the API and populate the table
async function populateTable() {
    const apiUrl = 'https://customer-complaint.onrender.com/staff2';  // Replace with your actual API URL
    
    try {
        // Fetch the data from the API
        const response = await fetch(apiUrl, {mode: 'cors'});
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        
        // Parse the JSON data
        const data = await response.json();

        // Get the table body where data will be inserted
        const tableBody = document.querySelector('#data-table tbody');
        
        // Clear any existing rows
        tableBody.innerHTML = '';

        // Iterate over the data and create table rows
        data.forEach(item => {
            const row = document.createElement('tr');
            
            // Create table cells for each item in the data
            const idCell = document.createElement('td');
            idCell.textContent = item.id; // Assuming the data has an 'id' property

            const nameCell = document.createElement('td');
            nameCell.textContent = item.name; // Assuming the data has a 'name' property

            const emailCell = document.createElement('td');
            emailCell.textContent = item.email; // Assuming the data has an 'email' property

            const phoneCell = document.createElement('td');
            phoneCell.textContent = item.telephone; // Assuming the data has a 'phone' property
            
            const categoryCell = document.createElement('td');
            categoryCell.textContent = item.category; // Assuming the data has a 'category' property
            
            // Append the cells to the row
            row.appendChild(idCell);
            row.appendChild(nameCell);
            row.appendChild(emailCell);
            row.appendChild(phoneCell);
            row.appendChild(categoryCell);
            
            // Append the row to the table body
            tableBody.appendChild(row);
        });
        
    } catch (error) {
        console.error('Error populating the table:', error);
    }
}

// Call the function to populate the table when the page loads
window.onload = populateTable;
