// quantity.js
document.addEventListener('DOMContentLoaded', function() {
    const medicines = document.querySelectorAll('.medicine');
    medicines.forEach(med => {
      const minusBtn = med.querySelector('.minus');
      const plusBtn = med.querySelector('.plus');
      const quantityValue = med.querySelector('.quantity-value');
  
      minusBtn.addEventListener('click', () => {
        let currentVal = parseInt(quantityValue.textContent);
        if (currentVal > 1) {
          quantityValue.textContent = currentVal - 1;
        }
      });
  
      plusBtn.addEventListener('click', () => {
        let currentVal = parseInt(quantityValue.textContent);
        quantityValue.textContent = currentVal + 1;
      });
    });
  });
  