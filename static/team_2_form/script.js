document.addEventListener('DOMContentLoaded', function () {
  console.log("Academics DSR Form Loaded");

  // Set today's date for the DSR date input
  const dateInput = document.getElementById('dsr-date');
  if (dateInput) {
      const today = new Date().toISOString().split('T')[0];
      dateInput.value = today;
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

  // Initialize functions
  setupLeaveCalculations();
  setupQuickNavigation();
  setupFormSubmissions();
  checkFlashMessages();
});

// Display flash messages using SweetAlert2
function checkFlashMessages() {
  const flashMessages = document.getElementById('flash-messages');
  if (flashMessages && flashMessages.innerHTML.trim()) {
    // Find success messages
    const successMsg = flashMessages.querySelector('.bg-green-100');
    if (successMsg) {
      Swal.fire({
        title: 'Success!',
        text: successMsg.textContent.trim(),
        icon: 'success',
        confirmButtonText: 'OK'
      });
    }
    
    // Find error messages
    const errorMsg = flashMessages.querySelector('.bg-red-100');
    if (errorMsg) {
      Swal.fire({
        title: 'Error!',
        text: errorMsg.textContent.trim(),
        icon: 'error',
        confirmButtonText: 'OK'
      });
    }
    
    // Find info messages
    const infoMsg = flashMessages.querySelector('.bg-blue-100');
    if (infoMsg && !successMsg && !errorMsg) {
      Swal.fire({
        title: 'Information',
        text: infoMsg.textContent.trim(),
        icon: 'info',
        confirmButtonText: 'OK'
      });
    }
    
    // Hide the original flash messages container
    flashMessages.style.display = 'none';
  }
}

// -------------------------
// LEAVE CALCULATIONS
// -------------------------
function setupLeaveCalculations() {
  // For HR Attendance form
  const hrAttendanceRows = document.querySelectorAll('#hrAttendanceForm tbody tr');
  
  hrAttendanceRows.forEach(row => {
    const totalInput = row.querySelector('input[name*="_total"]');
    const presentInput = row.querySelector('input[name*="_present"]');
    const leaveInput = row.querySelector('input[name*="_leave"]');
    const leavePercInput = row.querySelector('input[name*="_leave_perc"]');

    if (totalInput && presentInput && leaveInput) {
      [totalInput, presentInput].forEach(input => {
        input.addEventListener('input', function () {
          const total = parseInt(totalInput.value) || 0;
          const present = parseInt(presentInput.value) || 0;

          const leave = Math.max(0, total - present);
          const leavePerc = total > 0 ? ((leave / total) * 100).toFixed(1) : '0.0';

          leaveInput.value = leave;
          if (leavePercInput) leavePercInput.value = leavePerc;
        });
      });
    }
  });

  // For Total HR Attendance form
  const totalHRAttendanceRows = document.querySelectorAll('#totalHRAttendanceForm tbody tr');
  
  totalHRAttendanceRows.forEach(row => {
    const totalInput = row.querySelector('input[name*="_total"]');
    const presentInput = row.querySelector('input[name*="_present"]');
    const leaveInput = row.querySelector('input[name*="_leave"]');
    const leavePercInput = row.querySelector('input[name*="_leave_perc"]');

    if (totalInput && presentInput && leaveInput) {
      [totalInput, presentInput].forEach(input => {
        input.addEventListener('input', function () {
          const total = parseInt(totalInput.value) || 0;
          const present = parseInt(presentInput.value) || 0;

          const leave = Math.max(0, total - present);
          const leavePerc = total > 0 ? ((leave / total) * 100).toFixed(1) : '0.0';

          leaveInput.value = leave;
          if (leavePercInput) leavePercInput.value = leavePerc;
        });
      });
    }
  });

  // For Training Attendance form
  const trainingAttendanceRows = document.querySelectorAll('#trainingAttendanceForm tbody tr');
  
  trainingAttendanceRows.forEach(row => {
    const totalInput = row.querySelector('input[name*="_total"]');
    const presentInput = row.querySelector('input[name*="_present"]');
    const leaveInput = row.querySelector('input[name*="_leave"]');
    const leavePercInput = row.querySelector('input[name*="_leave_perc"]');

    if (totalInput && presentInput && leaveInput) {
      [totalInput, presentInput].forEach(input => {
        input.addEventListener('input', function () {
          const total = parseInt(totalInput.value) || 0;
          const present = parseInt(presentInput.value) || 0;

          const leave = Math.max(0, total - present);
          const leavePerc = total > 0 ? ((leave / total) * 100).toFixed(1) : '0.0';

          leaveInput.value = leave;
          if (leavePercInput) leavePercInput.value = leavePerc;
        });
      });
    }
  });

  calculateHRAttendanceOverall();
}

function calculateHRAttendanceOverall() {
  // Academic Overall
  setupSectionCalculation(
    ['hr_att_jr_school_total', 'hr_att_sr_school_total', 'hr_att_eca_total'],
    ['hr_att_jr_school_present', 'hr_att_sr_school_present', 'hr_att_eca_present'],
    ['hr_att_jr_school_leave', 'hr_att_sr_school_leave', 'hr_att_eca_leave'],
    'hr_att_acad_overall_total',
    'hr_att_acad_overall_present',
    'hr_att_acad_overall_leave',
    'hr_att_acad_overall_leave_perc'
  );

  // Admin Overall
  setupSectionCalculation(
    ['hr_att_admin_total', 'hr_att_drivers_total', 'hr_att_sec_total', 'hr_att_hk_total', 'hr_att_cond_total'],
    ['hr_att_admin_present', 'hr_att_drivers_present', 'hr_att_sec_present', 'hr_att_hk_present', 'hr_att_cond_present'],
    ['hr_att_admin_leave', 'hr_att_drivers_leave', 'hr_att_sec_leave', 'hr_att_hk_leave', 'hr_att_cond_leave'],
    'hr_att_admin_overall_total',
    'hr_att_admin_overall_present',
    'hr_att_admin_overall_leave',
    'hr_att_admin_overall_leave_perc'
  );

  // Total HR Attendance Overall (for the separate form)
  setupSectionCalculation(
    ['hr_att_overall_total'],
    ['hr_att_overall_present'],
    ['hr_att_overall_leave'],
    'hr_att_overall_total',
    'hr_att_overall_present',
    'hr_att_overall_leave',
    'hr_att_overall_leave_perc'
  );
}

function setupSectionCalculation(totalFields, presentFields, leaveFields, overallTotalField, overallPresentField, overallLeaveField, overallPercField) {
  const allFields = [...totalFields, ...presentFields, ...leaveFields];

  allFields.forEach(fieldName => {
    const field = document.querySelector(`input[name="${fieldName}"]`);
    if (field) {
      field.addEventListener('input', calculateOverall);
    }
  });

  function calculateOverall() {
    let totalSum = 0, presentSum = 0, leaveSum = 0;

    totalFields.forEach(name => {
      const input = document.querySelector(`input[name="${name}"]`);
      if (input) totalSum += parseInt(input.value) || 0;
    });

    presentFields.forEach(name => {
      const input = document.querySelector(`input[name="${name}"]`);
      if (input) presentSum += parseInt(input.value) || 0;
    });

    leaveFields.forEach(name => {
      const input = document.querySelector(`input[name="${name}"]`);
      if (input) leaveSum += parseInt(input.value) || 0;
    });

    const perc = totalSum > 0 ? ((leaveSum / totalSum) * 100).toFixed(1) : '0.0';

    document.querySelector(`input[name="${overallTotalField}"]`).value = totalSum;
    document.querySelector(`input[name="${overallPresentField}"]`).value = presentSum;
    document.querySelector(`input[name="${overallLeaveField}"]`).value = leaveSum;
    document.querySelector(`input[name="${overallPercField}"]`).value = perc;
  }

  calculateOverall(); // run once initially
}

// -------------------------
// QUICK NAVIGATION
// -------------------------
function setupQuickNavigation() {
  const quickNav = document.getElementById('nav-select');
  if (quickNav) {
    quickNav.addEventListener('change', function () {
      const selectedSection = this.value;
      if (selectedSection) {
        // Look for elements with data-form attribute matching the selected value
        const target = document.querySelector(`[data-form="${selectedSection}"]`);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          this.value = ''; // reset selection
        }
      }
    });
  }
}
// -------------------------
// FORM SUMMARY GENERATION
// -------------------------
function generateSummary(form) {
    // Get form title from the section heading
    const formSection = form.querySelector('.dsr-section');
    const formTitle = formSection ? formSection.querySelector('h3')?.textContent || 'Form Submission' : 'Form Submission';
    
    const entries = [];
    const groupedEntries = {};
    
    function determineGroupKey(fieldName) {
        // If name ends with _suffix or _suffix[] use that as group key
        const suffixMatch = fieldName.match(/_([a-zA-Z0-9]+)(?:\[\])?$/);
        if (suffixMatch) {
            return suffixMatch[1];
        }
        // If array without suffix e.g., tc_grade[] -> use fieldName without []
        const arrayMatch = fieldName.match(/^(.*)\[\]$/);
        if (arrayMatch) {
            return arrayMatch[1];
        }
        // Default whole name
        return fieldName;
    }

    Array.from(form.elements).forEach(el => {
        if (!el.name || el.type === 'hidden' || el.type === 'submit' || el.type === 'button') return;
        
        let value = '';
        if (el.type === 'checkbox' || el.type === 'radio') {
            value = el.checked ? 'Yes' : 'No';
        } else {
            value = el.value.trim();
        }
        
        if (value) {
            // Get field label from title attribute or create readable name
            const fieldLabel = el.title || el.name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            
            // Group similar fields together
            const groupKey = determineGroupKey(el.name);
            if (!groupedEntries[groupKey]) {
                groupedEntries[groupKey] = [];
            }
            
            groupedEntries[groupKey].push({
                label: fieldLabel,
                value: value,
                name: el.name
            });
        }
    });
    
    // Build organized display as tables
    let summaryHtml = `
        <div style="text-align: left; max-height: 450px; overflow-y: auto; padding: 10px;">
            <div style="background: linear-gradient(135deg, var(--primary-color, #2c3e50), var(--primary-light, #3f5771)); 
                        color: white; padding: 15px; margin: -10px -10px 20px -10px; border-radius: 8px;">
                <h3 style="margin: 0; font-size: 1.2em; font-weight: 600;">${formTitle}</h3>
                <p style="margin: 5px 0 0 0; font-size: 0.9em; opacity: 0.9;">Please review your entries before submitting</p>
            </div>
    `;

    if (Object.keys(groupedEntries).length === 0) {
        summaryHtml += `<div style="text-align:center; padding:20px; color:#666;">No fields have been filled out yet.</div>`;
    } else {
        Object.entries(groupedEntries).forEach(([groupName, fields]) => {
            summaryHtml += `
                <div style="border:1px solid var(--border-color,#e1e4e8); border-radius:8px; margin-bottom:20px; box-shadow:0 2px 6px rgba(0,0,0,0.05);">
                    <div style="background:var(--primary-color,#2c3e50); color:#fff; padding:10px 15px; font-weight:600; border-top-left-radius:8px; border-top-right-radius:8px;">
                        ${groupName.replace(/_/g,' ').replace(/\b\w/g,l=>l.toUpperCase())}
                    </div>
                    <div style="padding:15px;">
                        <div style="display:flex; flex-direction:column; gap:12px;">
            `;
            fields.forEach(field => {
                summaryHtml += `
                            <div style="display:flex; gap:10px; flex-wrap:wrap;">
                                <div style="flex:0 0 40%; font-weight:500; color:#495057;">${field.label}</div>
                                <div style="flex:1 1 55%; color:#212529; word-wrap:break-word; white-space:pre-wrap;">${field.value}</div>
                            </div>
                `;
            });
            summaryHtml += `
                        </div>
                    </div>
                </div>
            `;
        });
    }

    summaryHtml += `</div>`;
    return summaryHtml;
}

// -------------------------
// FORM SUBMISSIONS
// -------------------------
function setupFormSubmissions() {
  const forms = {
    'hrAttendanceForm': 'HR Attendance',
    'totalHRAttendanceForm': 'Total HR Attendance',
    'recruitmentActivityForm': 'Recruitment Activity',
    'pendingRecruitmentForm': 'Pending Recruitment',
    'recruitmentPipelineForm': 'Recruitment Pipeline',
    'staffStatusUpdatesForm': 'Staff Status Updates',
    'salaryPendingForm': 'Salary Not Dispersed',
    'policeVerificationForm': 'Police Verification',
    'interviewScheduleForm': 'Interview Schedule',
    'exitInformationForm': 'Exit Information',
    'staffConcernsForm': 'Staff Concerns',
    'kuralRecitationForm': 'Kural Recitation',
    'form6PhoneCallsForm': 'Front Office Phone Calls',
    'form6VisitorLogForm': 'Visitor Log',
    'form6BSNLStatusForm': 'BSNL Phone Status',
    'form7a-inward': 'Materials Inward',
    'form7b-outward': 'Materials Outward',
    'form7c-movement': 'Materials Movement',
    'form7d-returnable': 'Returnable Materials',
    'form7e-report': 'Returnable Goods Report',
    'form-8a-campus-form': 'Campus Camera Status',
    'form-8b-vehicle-form': 'Vehicle Camera Status',
    'form-8c-busac-form': 'Bus AC Camera Status',
    'gpsMonitoringForm': 'GPS Monitoring',
    'issuesMonitoringForm': 'Monitoring Issues Identified',
    'lateTeachersForm': 'Teachers Late Reporting',
    'cameraFootageForm': 'Camera & Monitoring Footage Data Entry',
    'biometricsForm': 'Biometrics Punching',
    'waterTdsForm': 'Water TDS Deviation',
    'testingCleaningForm': 'Testing & Cleaning - General',
    'waterLevelForm': 'Water Level Checking',
    'housekeepingGeneralForm': 'Housekeeping General',
    'poolTestingForm': 'Testing & Cleaning - Pool',
    'washroomCleanlinessForm': 'Washroom Cleanliness',
    'transportAttendanceForm': 'Transport Attendance',
    'transportAcStatusForm': 'Transport AC Status',
    'lateReportingForm': 'Transport Late Reporting',
    'maintenanceServiceForm': 'Transport Maintenance/Issues',
    'carMaintenanceForm': 'Car Maintenance',
    'renewalsForm': 'Transport Renewals/Delays',
    'specialTripForm': 'Transport Special Trip',
    'parent-concern-detail-form': 'Parent Concern Detail',
    'acTempForm': 'AC Temperature',
    'laborEbSolarGensetForm': 'Maintenance Labor',
    'motorForm': 'Motor Control',
    'pestControlForm': 'Pest Control',
    'acTempDeviationForm': 'AC Temp Deviation',
    'electricityConsumptionForm': 'Electricity Consumption',
    'ebDetailsForm': 'EB Details',
    'solarDetailsForm': 'Solar Details',
    'gensetDetailsForm': 'Genset Details',
    'securityCountVerificationForm': 'Security Count Verification',
    'securityAttendanceReplacementForm': 'Security Attendance Replacement',
    'securityInfoNoteForm': 'Security Info Note',
    'securityGovtInoutForm': 'Security Govt Officials In/Out',
    'alcoholTestForm': 'Security Alcohol Test',
    'materialsInwardForm': 'Security Materials Inward',
    'securityMaterialsOutwardForm': 'Security Materials Outward',
    'transportVerificationForm': 'Security Transport Verification',
    'documentsMovementForm': 'Documents Movement',
    'govtOfficialDocumentsForm': 'Govt Official Documents Expiry',
    'thoorigaiFbForm': 'Digital Marketing - Thoorigai',
    'websiteUpdatesForm': 'Digital Marketing - Thoorigai Website',
    'mdSocialMediaForm': 'Digital Marketing - MD',
    'intercomMaintenanceForm': 'Intercom Maintenance',
    'healthCheckUpForm': 'Health Check Up',
    'netConnectivityPrintsForm': 'Net Connectivity/Prints',
    'generalMaintenanceItForm': 'IT Maintenance',
    'calendarScheduleForm': 'Calendar Schedule',
    'trainingAttendanceForm': 'Training Attendance',
    'trainingDetailsForm': 'Training Details',
    'manpowerPlanningForm': 'Manpower Planning',
    'overallConsolidationForm': 'Overall Consolidation',
    'uniformDetailsForm': 'Uniform Details',
    'deptWiseUniformDetailsForm': 'Department Wise Uniform Details'
    };

  Object.keys(forms).forEach(formId => {
    const form = document.getElementById(formId);
    if (form) {
      form.addEventListener('submit', handleFormSubmit);
    }
  });
}

function handleFormSubmit(event) {
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
    const submitBtn = form.querySelector('.submit-btn');
    
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Submitting...';
    }

    fetch(form.action, {
      method: 'POST',
      body: formData,
      redirect: 'manual' // Don't automatically follow redirects
    })
    .then(response => {
      if (response.type === 'opaqueredirect') {
        // Server redirected, reload the page to show flash messages
        window.location.reload();
        return null;
      } else {
        return response.json(); // Try to parse JSON for API responses
      }
    })
    .then(data => {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit';
      }
      
      if (data) {
        if (data.message) {
          Swal.fire({
            title: 'Success!',
            text: data.message,
            icon: 'success',
            confirmButtonText: 'OK'
          }).then((result) => {
            if (result.isConfirmed) {
              form.reset();
            }
          });
        } else if (data.error) {
          Swal.fire({
            title: 'Error!',
            text: data.error,
            icon: 'error',
            confirmButtonText: 'OK'
          });
        }
      }
    })
    .catch(error => {
      console.error('Error:', error);
      
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit';
      }
      
      // For non-JSON responses, just reload the page to show flash messages
      window.location.reload();
    });
  });
}

// -------------------------
// MOTOR CONTROL FORM FUNCTIONS
// -------------------------
function addMotorRow() {
  const tbody = document.getElementById('motorTableBody');
  const newRow = document.createElement('tr');
  newRow.className = 'data-row';
  
  newRow.innerHTML = `
    <td><input type="time" name="motor_on_time[]" data-col-name="Motor On Time"></td>
    <td><input type="time" name="motor_off_time[]" data-col-name="Motor Off Time"></td>
    <td>
      <select name="motor_nature[]" class="nature-select" data-col-name="Nature of Issue">
        <option value="All Well">All Well</option>
        <option value="Manageable">Manageable</option>
        <option value="Critical">Critical</option>
      </select>
    </td>
    <td><textarea name="motor_issue[]" rows="1" data-col-name="Issue Description"></textarea></td>
    <td><textarea name="motor_comments[]" rows="1" data-col-name="Comments"></textarea></td>
    <td>
      <button type="button" class="add-row-btn" onclick="addMotorRow()" title="Add Row">+</button>
      <button type="button" class="remove-row-btn" onclick="removeMotorRow(this)" title="Remove Row">-</button>
    </td>
  `;
  
  tbody.appendChild(newRow);
}

function removeMotorRow(button) {
  const tbody = document.getElementById('motorTableBody');
  const rows = tbody.querySelectorAll('tr');
  
  // Don't remove if it's the last row
  if (rows.length > 1) {
    button.closest('tr').remove();
  } else {
    alert('Cannot remove the last row. At least one row is required.');
  }
}

// -------------------------
// PEST CONTROL FORM FUNCTIONS
// -------------------------
function addPestRow() {
  const tbody = document.getElementById('pestTableBody');
  const newRow = document.createElement('tr');
  newRow.className = 'data-row';
  
  newRow.innerHTML = `
    <td><input type="time" name="pest_in_time[]" data-col-name="Pest In Time"></td>
    <td><input type="time" name="pest_out_time[]" data-col-name="Pest Out Time"></td>
    <td><textarea name="pest_area[]" rows="1" data-col-name="Area Covered"></textarea></td>
    <td>
      <select name="pest_nature[]" class="nature-select" data-col-name="Nature of Issue">
        <option value="All Well">All Well</option>
        <option value="Manageable">Manageable</option>
        <option value="Critical">Critical</option>
      </select>
    </td>
    <td><textarea name="pest_issue[]" rows="1" data-col-name="Issue Description"></textarea></td>
    <td><textarea name="pest_comments[]" rows="1" data-col-name="Comments"></textarea></td>
    <td>
      <button type="button" class="add-row-btn" onclick="addPestRow()" title="Add Row">+</button>
      <button type="button" class="remove-row-btn" onclick="removePestRow(this)" title="Remove Row">-</button>
    </td>
  `;
  
  tbody.appendChild(newRow);
}

function removePestRow(button) {
  const tbody = document.getElementById('pestTableBody');
  const rows = tbody.querySelectorAll('tr');
  
  // Don't remove if it's the last row
  if (rows.length > 1) {
    button.closest('tr').remove();
  } else {
    alert('Cannot remove the last row. At least one row is required.');
  }
}

// -------------------------
// GLOBAL ADD ROW FUNCTION
// -------------------------
function addRow(tbodyId) {
  const tbody = document.getElementById(tbodyId);
  if (!tbody) {
    console.error('Table body with ID', tbodyId, 'not found');
    return;
  }
  
  const firstRow = tbody.querySelector('tr');
  if (!firstRow) {
    console.error('No rows found in table body', tbodyId);
    return;
  }
  
  const newRow = firstRow.cloneNode(true);
  
  // Update S.No if it exists
  const snoElement = newRow.querySelector('.sno');
  if (snoElement) {
    const rowCount = tbody.rows.length;
    snoElement.textContent = rowCount + 1;
  }
  
  // Clear all input, select, and textarea values
  newRow.querySelectorAll('input, select, textarea').forEach(el => {
    if (el.tagName.toLowerCase() === 'select') {
      el.selectedIndex = 0;
    } else {
      el.value = '';
    }
  });
  
  tbody.appendChild(newRow);
}


