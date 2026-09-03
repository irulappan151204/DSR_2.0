document.addEventListener('DOMContentLoaded', function () {
    console.log("Team 3 Audit Form Loaded");

    // Set today's date in Indian format (DD-MM-YYYY) and make readonly
    const dateInput = document.getElementById('dsr-date');
    if (dateInput) {
        const today = new Date();
        const day = String(today.getDate()).padStart(2, '0');
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const year = today.getFullYear();
        dateInput.value = `${day}-${month}-${year}`;
        dateInput.readOnly = true;
        dateInput.style.background = '#f1f5f9';
        dateInput.style.cursor = 'not-allowed';
    }

    // Handle quick navigation dropdown
    const navSelect = document.getElementById('nav-select');
    if (navSelect) {
        navSelect.addEventListener('change', function () {
            const sectionId = this.value;
            if (sectionId) {
                const target = document.querySelector(sectionId);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    }

    // Function to add a new row to a specified table body
    function addRow(tbodyId) {
        const tbody = document.getElementById(tbodyId);
        if (!tbody || tbody.rows.length === 0) {
            console.error("Tbody not found or is empty for ID:", tbodyId);
            return;
        }

        const templateRow = tbody.rows[tbody.rows.length - 1];
        const newRow = templateRow.cloneNode(true);

        // Clear input/select/textarea values in the new row
        const inputs = newRow.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            if (input.type === 'checkbox' || input.type === 'radio') {
                input.checked = false;
            } else if (input.tagName === 'SELECT') {
                input.selectedIndex = 0;
            } else {
                input.value = '';
            }
        });

        tbody.appendChild(newRow);
    }

    // Make the addRow function globally accessible
    window.addRow = addRow;

    // Handle form submissions
    const team3AuditForm = document.getElementById('team3-audit-form');
    const newAuditForm = document.getElementById('new-audit-form');

    function generateSummary(form) {
        // Get form title from the section heading
        const formSection = form.querySelector('.dsr-section');
        const formTitle = formSection ? formSection.querySelector('h3')?.textContent || 'Form Submission' : 'Form Submission';
        
        const entries = [];
        const groupedEntries = {};
        
        // Get all form inputs
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            if (input.name && input.value.trim()) {
                const fieldName = input.name.replace('[]', '');
                const fieldValue = input.value.trim();
                
                if (!groupedEntries[fieldName]) {
                    groupedEntries[fieldName] = [];
                }
                groupedEntries[fieldName].push(fieldValue);
            }
        });
        
        // Build summary HTML
        let summaryHTML = `<h4>${formTitle}</h4>`;
        summaryHTML += '<div style="text-align: left; max-height: 300px; overflow-y: auto;">';
        
        Object.keys(groupedEntries).forEach(fieldName => {
            const values = groupedEntries[fieldName];
            if (values.length > 0) {
                summaryHTML += `<p><strong>${fieldName}:</strong> ${values.join(', ')}</p>`;
            }
        });
        
        summaryHTML += '</div>';
        return summaryHTML;
    }

    function handleSubmit(event) {
        event.preventDefault();
        const form = event.target;

        // Show confirmation dialog first
        Swal.fire({
            title: 'Please confirm your entries',
            html: generateSummary(form),
            icon: 'info',
            showCancelButton: true,
            confirmButtonText: 'Confirm & Submit',
            cancelButtonText: 'Cancel'
        }).then(result => {
            if (!result.isConfirmed) {
                return; // User cancelled
            }

            const formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData,
                redirect: 'follow'
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                    return null;
                }
                return response.text();
            })
            .then(text => {
                if (text === null) return;
                if (text && text.toLowerCase().includes('success')) {
                    Swal.fire({
                        title: 'Success!',
                        text: 'Form submitted successfully',
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then(() => {
                        form.reset();
                        // Reset the date to today after form reset
                        const dateInput = document.getElementById('dsr-date');
                        if (dateInput) {
                            const today = new Date();
                            const day = String(today.getDate()).padStart(2, '0');
                            const month = String(today.getMonth() + 1).padStart(2, '0');
                            const year = today.getFullYear();
                            dateInput.value = `${day}-${month}-${year}`;
                        }
                    });
                } else {
                    Swal.fire({
                        title: 'Error!',
                        text: 'Failed to submit form. Please try again.',
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
                }
            })
            .catch(error => {
                console.error('Submission Error:', error);
                Swal.fire({
                    title: 'Error!',
                    text: 'An error occurred while submitting the form.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            });
        });
    }

    // Add event listeners to all forms
    const forms = [
        team3AuditForm,
        newAuditForm
    ];

    forms.forEach(form => {
        if (form) {
            form.addEventListener('submit', handleSubmit);
        }
    });
});
