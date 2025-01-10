async function populateTable(apiUrl = '/staff2') {
    try {
        // Fetch the data from the API
        const response = await fetch(apiUrl, { mode: 'cors' });
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }

        // Parse the JSON response
        const jsonResponse = await response.json();
        const { pagination, users } = jsonResponse;

        console.log('API Response:', jsonResponse);  // Debugging logs
        console.log('Pagination:', pagination);
        console.log('Users:', users);

        // Ensure pagination and user data are present
        if (!pagination || !Array.isArray(users)) {
            throw new Error('Invalid API response structure');
        }

        // Clear existing table data to avoid duplication
        const tableBody = document.querySelector('#data-table tbody');
        tableBody.innerHTML = '';

        // Populate table with new data
        users.forEach(item => {
            const row = document.createElement('tr');

            // Create table cells
            const idCell = document.createElement('td');
            idCell.textContent = item.id;

            const nameCell = document.createElement('td');
            nameCell.textContent = item.name;

            const emailCell = document.createElement('td');
            emailCell.textContent = item.email;

            const phoneCell = document.createElement('td');
            phoneCell.textContent = item.telephone;

            const categoryCell = document.createElement('td');
            categoryCell.textContent = item.category;

            // Status column with color coding
            const statusCell = document.createElement('td');
            const statusDiv = document.createElement('div');
            statusDiv.textContent = item.status || 'Unresolved';
            statusDiv.classList.add(item.status === 'resolved' ? 'resolved' : 'status-cell');
            statusCell.appendChild(statusDiv);

            // Action button
            const actionCell = document.createElement('td');
            const viewButton = document.createElement('button');
            viewButton.textContent = 'View More';
            viewButton.classList.add('view-more-btn');
            actionCell.appendChild(viewButton);

            // Attach click event to View More button
            viewButton.addEventListener('click', () => {
                showDetails(item, statusDiv);
            });

            // Append cells to the row
            row.appendChild(idCell);
            row.appendChild(nameCell);
            row.appendChild(emailCell);
            row.appendChild(phoneCell);
            row.appendChild(categoryCell);
            row.appendChild(statusCell);
            row.appendChild(actionCell);

            // Append row to table body
            tableBody.appendChild(row);
        });

        // Update pagination UI
        updatePaginationUI(pagination);

    } catch (error) {
        console.error('Error populating the table:', error);
    }
}

function updatePaginationUI(pagination) {
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');
    const currentPage = document.getElementById('current-page');
    const totalPages = document.getElementById('total-pages');

    // Update page display
    currentPage.textContent = pagination.page || 1;
    totalPages.textContent = pagination.pages || 1;

    // Enable/disable buttons
    prevButton.disabled = !pagination.prev_page;
    nextButton.disabled = !pagination.next_page;

    // Update button click handlers
    prevButton.onclick = () => pagination.prev_page && populateTable(pagination.prev_page);
    nextButton.onclick = () => pagination.next_page && populateTable(pagination.next_page);
}



// Function to show detailed information about a complaint
function showDetails(item, statusDiv) {
  const detailsContainer = document.getElementById('details-container');
  const tableContainer = document.getElementById('table-container');
  const detailsContent = document.getElementById('details-content');

  // Populate the details content
  detailsContent.innerHTML = `
    <h3>Complaint Details</h3>
    <div class="container">
        <div class="user-logo">
            <i class="fa-solid fa-user"></i>
            <p><strong>Name:</strong> ${item.name}</p>
        </div>
        <div id="info-section">
            <div class="left-right">
                <div class="left-section">
                    <p><strong>Customer ID:</strong> ${item.id}</p>
                    <p><strong>Complaint ID:</strong> ${item.complaint_id} </p>
                    <p><strong>Status:</strong> ${item.status} </p>
                    <p><strong>Time:</strong> ${item.date} </p>
                </div>
                <div class="right-section">
                    <p><strong>Email:</strong> ${item.email}</p>
                    <p><strong>Telephone:</strong> ${item.telephone}</p>
                    <p><strong>Category:</strong> ${item.category}</p>
                </div>
            </div>
            <div class="message_download">
                <p><strong>Complaint:</strong></p>
                <p><textarea id="textarea">${item.complaint}</textarea></p>
                <p><strong>Attached file:</strong><a href="${item.image}" target="_blank"> <i class="fa-solid fa-file-arrow-down"></i></a></p>
            </div>
            <div class="button-section">
                <button id="back-button"><i class="fa-solid fa-arrow-left"></i> Back </button>
                <button id="resolve-button">Mark as resolved <i class="fa-solid fa-check"></i></button>
                <button id="call-button">Call <i class="fa-solid fa-phone"></i></button>
                <button id="email-button">Send Email <i class="fa-regular fa-envelope"></i></button>
            </div>
        </div>
       
       
    </div>
  `;
  // Show the details container and hide the table container
  detailsContainer.style.display = 'block';
  tableContainer.style.display = 'none';

  // Back button functionality
  const backButton = document.getElementById('back-button');
  backButton.addEventListener('click', () => {
      detailsContainer.style.display = 'none';
      tableContainer.style.display = 'block';
  });

  // Resolve button functionality
  const resolveButton = document.getElementById('resolve-button');
  resolveButton.addEventListener('click', async () => {
      try {
          // Create a FormData object to send form data
          const formData = new FormData();
          formData.append('complaint_id', item.complaint_id); // Add complaint_id
          formData.append('status', 'resolved'); // Add status
  
          // URL for the API endpoint that updates the status

          const apiUrl = '/update_status'; // Replace with your actual API endpoint

          // Make the POST request
          const response = await fetch(apiUrl, {
              method: 'POST',
              body: formData, // Send form data
          });
  
          if (!response.ok) {
              throw new Error('Failed to update status. Please try again.');
          }
  
          // Handle the success response
          const result = await response.json(); // Parse the response if needed
  
          // Update the complaint status in the table
          statusDiv.textContent = 'Resolved'; // Update the status text
          statusDiv.style.border = '2px solid green';
          statusDiv.style.color = 'green';
  
          alert('Complaint has been resolved!');
      } catch (error) {
          console.error('Error resolving complaint:', error);
          alert('Failed to resolve complaint. Please try again.');
      }
  });


  // Call button functionality
  const callButton = document.getElementById('call-button');
  callButton.addEventListener('click', () => {
      window.open(`tel:${item.telephone}`, '_blank');
  });

  // Email button functionality
  const emailButton = document.getElementById('email-button');
  emailButton.addEventListener('click', () => {
      window.open(`mailto:${item.email}`, '_blank');
  });
}


// Call the function to populate the table when the page loads
window.onload = populateTable();

//search bar and filters
function filterTable() {
    const searchBarValue = document.getElementById('searchBar').value.toLowerCase(); // Search bar input
    const filterCategoryValue = document.getElementById('filterCategory').value; // Category filter value
    const filterStatusValue = document.getElementById('filterStatus').value; // Status filter value
    const tableRows = document.querySelectorAll('#data-table tbody tr'); // All table rows

    tableRows.forEach(row => {
        const name = row.cells[1].textContent.toLowerCase(); // Name column
        const email = row.cells[2].textContent.toLowerCase(); // Email column
        const phone = row.cells[3].textContent.toLowerCase(); // Phone column
        const category = row.cells[4].textContent; // Category column
        const status = row.cells[5].textContent; // Status column

        // Apply individual filters
        const searchMatch = 
            searchBarValue === '' || 
            name.includes(searchBarValue) || 
            email.includes(searchBarValue) || 
            phone.includes(searchBarValue);

        const categoryMatch = filterCategoryValue === '' || category === filterCategoryValue;

        const statusMatch = filterStatusValue === '' || status === filterStatusValue;

        // Show or hide the row based on independent filters
        if (searchMatch && categoryMatch && statusMatch) {
            row.style.display = ''; // Show row
        } else {
            row.style.display = 'none'; // Hide row
        }
    });
}

//Logout
function handleLogout() {
    // Show the modal
    const modal = document.getElementById('logoutModal');
    modal.style.display = 'block';

    // Get the buttons
    const confirmButton = document.getElementById('confirmLogout');
    const cancelButton = document.getElementById('cancelLogout');

    // Confirm Logout
    confirmButton.onclick = () => {
        modal.style.display = 'none';
        // Redirect to the login page
        window.location.href = '/staff_login'; // Replace with the actual login page URL
    };

    // Cancel Logout
    cancelButton.onclick = () => {
        modal.style.display = 'none';
        alert("Logout canceled.");
    };

    // Close modal when clicking outside of it
    window.onclick = (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };
}


