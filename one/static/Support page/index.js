//form validation
function validateForm(){
  const name_input = document.getElementById('name').value;
const emailInput = document.getElementById('email').value;
const telephoneInput = document.getElementById('telephone').value;
const complaintInput = document.getElementById('complaint').value;
//const image = document.getElementById('image').value;
  //radio inputs
  const radioInput= document.querySelectorAll('#report-option input[type="radio"]')
  const isSelected = Array.from(radioInput).some(option => option.checked);
  if(name_input===''){
    alert('Please fill in the fields marked with *')
    return;
  } 
   if (emailInput===''){
    alert('Please fill in the fields marked with *')
    return;
  }
   if (telephoneInput===''){
    alert('Please fill in the fields marked with *')
    return;
  }
   if (complaintInput===''){
    alert('Please fill in the fields marked with *')
    return;
  }
  if (!isSelected){
    alert('Please fill in the fields marked with *')
    return;
  }
    else{
      alert('Form submitted successively')
    }
    window.location.href = 'success_page.html'
  }
//API
document.getElementById('complaint-form').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent the default form submission

  const formData = new FormData(); // Corrected here
  formData.append('name', document.getElementById('name').value);
  formData.append('telephone', document.getElementById('telephone').value);
  formData.append('complaint', document.getElementById('complaint').value);

  // Get the selected category from radio buttons
  const selectedCategory = document.querySelector('input[name="report-reason"]:checked');
  if (selectedCategory) {
      formData.append('category', selectedCategory.value);
  } else {
      console.error('No category selected');
  }
  formData.append('email', document.getElementById('email').value);
  
  // Correctly handle the image input
  const imageInput = document.getElementById('image');
  if (imageInput.files.length > 0) {
    formData.append('image', imageInput.files[0]); // Use files[0] to get the file object
  }

  fetch('https://customer-complaint.onrender.com/user', {
    method: 'POST',
    body: formData
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json();
  })
  .then(data => {
    console.log('Success:', data);
    document.getElementById('response').innerText = 'Success: ' + JSON.stringify(data);
  })
  .catch((error) => {
    console.error('Error:', error);
    document.getElementById('response').innerText = 'Error: ' + error;
  });
  
});