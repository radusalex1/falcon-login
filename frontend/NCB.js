function toggleForm(otherFormId, currentForm) {
    const otherForm = document.getElementById(otherFormId);
    const otherInputs = otherForm.querySelectorAll('input, button');
    const currentInputs = currentForm.querySelectorAll('input, button');
  
    console.log('Current form:', currentForm.id);
    console.log('Other form:', otherFormId);
  
    const isCurrentFormFilled = Array.from(currentInputs).some(input => input.value.trim() !== '');
    console.log('Is current form filled:', isCurrentFormFilled);
  
    otherInputs.forEach(input => {
      input.disabled = isCurrentFormFilled;
      console.log(`Disabling input: ${input.name}, Disabled: ${input.disabled}`);
    });
  }