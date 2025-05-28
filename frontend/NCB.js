function toggleForm(otherFormId, currentForm) {
    const otherForm = document.getElementById(otherFormId);
    const otherFormContainer = otherForm.closest('.form-container');
    const otherInputs = otherForm.querySelectorAll('input, button');
    const currentInputs = currentForm.querySelectorAll('input, button');

    const isCurrentFormFilled = Array.from(currentInputs).some(input => input.value.trim() !== '');

    otherInputs.forEach(input => {
        input.disabled = isCurrentFormFilled;
    });

    
    if (isCurrentFormFilled) {
        otherFormContainer.classList.add('disabled');
    } else {
        otherFormContainer.classList.remove('disabled');
    }
}