//form validation
document.querySelector('form').addEventListener('submit', function(event){
  event.preventDefault();
const nameinput = document.getElementById('name').value.trim();
const emailInput = document.getElementById('email').value.trim();
const telephoneInput = document.getElementById('telephone').value.trim();
const complaintInput = document.getElementById('complaint').value.trim();
const imageInput = document.getElementById('image-upload');
const selectedCategory = document.querySelector('input[name="report-reason"]:checked');

//
  if(nameinput===''){
    alert('Please fill in the fields marked with *')
    return false;
  } 
  if(emailInput===''){
    alert('Please fill in the fields marked with *')
    return false;
  }
  if(telephoneInput===''){
    alert('Please fill in the fields marked with *')
    return false;
  }
  if(complaintInput===''){
    alert('Please fill in the fields marked with *')
    return false;
  }
  if(!selectedCategory){
    alert('Please select a report category')
    return false;
  }
  
    
  const formData = new FormData(); // Corrected here
  formData.append('name', document.getElementById('name').value);
  formData.append('telephone', document.getElementById('telephone').value);
  formData.append('complaint', document.getElementById('complaint').value);
  formData.append('email', document.getElementById('email').value);
  // Get the selected category from radio buttons
  if (selectedCategory) {
      formData.append('category', selectedCategory.value);
  }
  // Correctly handle the image input
  if (imageInput.files.length > 0) {
    formData.append('image', imageInput.files[0]); // Use files[0] to get the file object
  }

  fetch('/user', {
    method: 'POST',
    body: formData
  })
  .then(response => {
    console.log(response)
    window.location.href = response.url;
    alert('Success')
    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json();
  })
  
  .catch((error) => {
    console.error('Error:', error);
  })
});

//Email validation
function validateEmail() {
  const emailField = document.getElementById("email");
  const emailError = document.getElementById("emailError");

  // Reset error bubble state
  emailError.hidden = true;

  // Email validation pattern
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!emailPattern.test(emailField.value)) {
    // Show the error bubble if invalid
    emailError.hidden = false;

    // Position the bubble dynamically (optional)
    const rect = emailField.getBoundingClientRect();
    emailError.style.top = `${rect.bottom + window.scrollY}px`;
    emailError.style.left = `${rect.left + window.scrollX}px`;

    // Prevent form submission
    return false;
  }

  // Allow form submission if valid
  return true;
}




//image preview
const selectImage = document.querySelector('.select-image');
const inputFile = document.querySelector('#image-upload');
const imgArea = document.querySelector('.img-area');

selectImage.addEventListener('click', function (event) {
	inputFile.click();
  event.preventDefault();
})

inputFile.addEventListener('change', function () {
	const image = this.files[0]
	if(image.size < 2000000) {
		const reader = new FileReader();
		reader.onload = ()=> {
			const allImg = imgArea.querySelectorAll('img');
			allImg.forEach(item=> item.remove());
			const imgUrl = reader.result;
			const img = document.createElement('img');
			img.src = imgUrl;
			imgArea.appendChild(img);
			imgArea.classList.add('active');
			imgArea.dataset.img = image.name;
		}
		reader.readAsDataURL(image);
	} else {
		alert("Image size more than 2MB");
	}
})


