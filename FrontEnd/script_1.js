function uploadImage() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    
    if (!file) {
      alert('Please select an image file.');
      return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    fetch('http://localhost:8000/predictions', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      displayResult(data);
    })
    .catch(error => {
      console.error('Error:', error);
      displayError("Error");
    });
}

function displayResult(data) {
    const resultSection = document.getElementById('result-section');
    const resultDiv = document.getElementById('result');
    
    resultDiv.innerHTML = `
      <p><strong>Result:</strong> ${data.Result}</p>
      <p><strong>Accuracy:</strong> ${data.Accuracy}</p>
    `;
    
    resultSection.style.display = 'block';
}

function displayError(e) {
    const resultSection = document.getElementById('result-section');
    const resultDiv = document.getElementById('result');
    
    resultDiv.innerHTML = `
      <p><strong>Result:</strong> Error</p>
      <p><strong>Accuracy:</strong> Error</p>
    `;
    
    resultSection.style.display = 'block';
}

// Tooltip hover logic
const hoverLink = document.getElementById('hoverLink');
const tooltip = document.getElementById('tooltip');

// Show tooltip on hover
hoverLink.addEventListener('mouseover', function() {
  tooltip.classList.remove('hidden');
});

// Hide tooltip when not hovering
hoverLink.addEventListener('mouseout', function() {
  tooltip.classList.add('hidden');
});

// Position tooltip relative to the link
hoverLink.addEventListener('mousemove', function(e) {
  const x = e.pageX + 10;
  const y = e.pageY + 10;
  tooltip.style.left = `${x}px`;
  tooltip.style.top = `${y}px`;
});
