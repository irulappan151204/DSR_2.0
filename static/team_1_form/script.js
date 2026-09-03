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

        // Initialize special behaviour if needed (e.g., dynamic filtering)
        if (tbodyId === 'school-counsellor-tbody' && typeof window.setupSchoolCounsellorRow === 'function') {
            window.setupSchoolCounsellorRow(newRow);
        }
    }

    // Make the addRow function globally accessible
    window.addRow = addRow;

    // Handle form submissions
    // Handle form submissions
const calendarForm = document.getElementById('calendar-form');
const asaForm = document.getElementById('asa-form');
const asaSportsForm = document.getElementById('asa-sports-form');
const asaGeneralForm = document.getElementById('asa-general-form');
const studentAttendanceForm = document.getElementById('student-attendance-form');
const groomingForm = document.getElementById('grooming-form');
const latecomingForm = document.getElementById('latecoming-form');
const admissionStatusForm = document.getElementById('admission-status-form');
const tcForm = document.getElementById('tc-form');
const parentActivityForm = document.getElementById('parent-activity-form');
const parentVisitForm = document.getElementById('parent-visit-form');
const examScheduleForm = document.getElementById('exam-schedule-form');
const externalInfoForm = document.getElementById('external-info-form');
const sickBayForm = document.getElementById('sick-bay-form');
const homeSchoolForm = document.getElementById('home-school-form');
const disciplinaryForm = document.getElementById('disciplinary-form');
const logisticsForm = document.getElementById('logistics-form');
const competitionCertForm = document.getElementById('competition-cert-form');
const staffConcernForm = document.getElementById('staff-concern-form');
const parentConcernForm = document.getElementById('parent-concern-summary-form');
const parentConcernDetailForm = document.getElementById('parent-concern-detail-form');
const aepForm = document.getElementById('aep-form');
const extendedClassForm = document.getElementById('extended-class-form');
const trainingForm = document.getElementById('training-form');
const weeklyMeetingForm = document.getElementById('weekly-meeting-form');
const studentConcernForm = document.getElementById('student-concern-form');
const specialEducationForm = document.getElementById('special-education-form');
const hostelForm = document.getElementById('hostel-form');
const secForm = document.getElementById('sec-form');
const schoolCounsellorForm = document.getElementById('school-counsellor-form');
const scholoriusForm = document.getElementById('scholorius-form');

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

    const tableStyle = null; // removed table style
    const thStyle = null;
    const tdStyle = null;

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
    calendarForm,
    asaForm,
    asaSportsForm,
    asaGeneralForm,
    studentAttendanceForm,
    groomingForm,
    latecomingForm,
    admissionStatusForm,
    tcForm,
    parentActivityForm,
    parentVisitForm,
    examScheduleForm,
    externalInfoForm,
    sickBayForm,
    homeSchoolForm,
    disciplinaryForm,
    logisticsForm,
    competitionCertForm,
    staffConcernForm,
    parentConcernForm,
    parentConcernDetailForm,
    aepForm,
    extendedClassForm,
    trainingForm,
    weeklyMeetingForm,
    studentConcernForm,
    specialEducationForm,
    hostelForm,
    secForm,
    schoolCounsellorForm,
    scholoriusForm
];

forms.forEach(form => {
    if (form) {
        form.addEventListener('submit', handleSubmit);
    }
});

    // Calculate percentages for ASA form
    function setupASACalculations() {
        const rows = document.querySelectorAll('#asa-activities tbody tr');
        
        rows.forEach(row => {
            const strengthInput = row.querySelector('input[name*="strength"]');
            const enrolledInput = row.querySelector('input[name*="enrolled"]');
            const enrolPercInput = row.querySelector('input[name*="enrol_pct"]');
            const expectedInput = row.querySelector('input[name*="expected"]');
            const attendedInput = row.querySelector('input[name*="attended"]');
            const attendPercInput = row.querySelector('input[name*="attend_pct"]');

            if (strengthInput && enrolledInput && enrolPercInput) {
                [strengthInput, enrolledInput].forEach(input => {
                    input.addEventListener('input', function() {
                        const strength = parseInt(strengthInput.value) || 0;
                        const enrolled = parseInt(enrolledInput.value) || 0;
                        const enrolPerc = strength > 0 ? ((enrolled / strength) * 100).toFixed(1) : '0.0';
                        enrolPercInput.value = enrolPerc;
                    });
                });
            }

            if (expectedInput && attendedInput && attendPercInput) {
                [expectedInput, attendedInput].forEach(input => {
                    input.addEventListener('input', function() {
                        const expected = parseInt(expectedInput.value) || 0;
                        const attended = parseInt(attendedInput.value) || 0;
                        const attendPerc = expected > 0 ? ((attended / expected) * 100).toFixed(1) : '0.0';
                        attendPercInput.value = attendPerc;
                    });
                });
            }
        });
    }

    // Calculate percentages for ASA Sports form
    function setupASASportsCalculations() {
        const rows = document.querySelectorAll('#asa-sports tbody tr');
        
        rows.forEach(row => {
            const strengthInput = row.querySelector('input[name*="strength"]');
            const enrolledInput = row.querySelector('input[name*="enrolled"]');
            const enrolPercInput = row.querySelector('input[name*="enrol_pct"]');
            const expectedInput = row.querySelector('input[name*="expected"]');
            const attendedInput = row.querySelector('input[name*="attended"]');
            const attendPercInput = row.querySelector('input[name*="attend_pct"]');

            if (strengthInput && enrolledInput && enrolPercInput) {
                [strengthInput, enrolledInput].forEach(input => {
                    input.addEventListener('input', function() {
                        const strength = parseInt(strengthInput.value) || 0;
                        const enrolled = parseInt(enrolledInput.value) || 0;
                        const enrolPerc = strength > 0 ? ((enrolled / strength) * 100).toFixed(1) : '0.0';
                        enrolPercInput.value = enrolPerc;
                    });
                });
            }

            if (expectedInput && attendedInput && attendPercInput) {
                [expectedInput, attendedInput].forEach(input => {
                    input.addEventListener('input', function() {
                        const expected = parseInt(expectedInput.value) || 0;
                        const attended = parseInt(attendedInput.value) || 0;
                        const attendPerc = expected > 0 ? ((attended / expected) * 100).toFixed(1) : '0.0';
                        attendPercInput.value = attendPerc;
                    });
                });
            }
        });
    }

    setupASACalculations();
    setupASASportsCalculations();

    // Calculate percentages for ASA General form
    function setupASAGeneralCalculations() {
        const rows = document.querySelectorAll('#asa-general tbody tr');
        
        rows.forEach(row => {
            const strengthInput = row.querySelector('input[name*="strength"]');
            const enrolledInput = row.querySelector('input[name*="enrolled"]');
            const enrolPercInput = row.querySelector('input[name*="enrol_pct"]');
            const expectedInput = row.querySelector('input[name*="expected"]');
            const attendedInput = row.querySelector('input[name*="attended"]');
            const attendPercInput = row.querySelector('input[name*="attend_pct"]');

            if (strengthInput && enrolledInput && enrolPercInput) {
                [strengthInput, enrolledInput].forEach(input => {
                    input.addEventListener('input', function() {
                        const strength = parseInt(strengthInput.value) || 0;
                        const enrolled = parseInt(enrolledInput.value) || 0;
                        const enrolPerc = strength > 0 ? ((enrolled / strength) * 100).toFixed(1) : '0.0';
                        enrolPercInput.value = enrolPerc;
                    });
                });
            }

            if (expectedInput && attendedInput && attendPercInput) {
                [expectedInput, attendedInput].forEach(input => {
                    input.addEventListener('input', function() {
                        const expected = parseInt(expectedInput.value) || 0;
                        const attended = parseInt(attendedInput.value) || 0;
                        const attendPerc = expected > 0 ? ((attended / expected) * 100).toFixed(1) : '0.0';
                        attendPercInput.value = attendPerc;
                    });
                });
            }
        });
    }

    setupASAGeneralCalculations();

    // Auto-calculate Present % and Absent % for Calendar Schedule
    function setupCalendarScheduleCalculations() {
        // Jr. School
        const totalJr = document.querySelector('input[name="cal_total_jr"]');
        const expectedJr = document.querySelector('input[name="cal_expected_jr"]');
        const presentPctJr = document.querySelector('input[name="cal_present_pct_jr"]');
        const absentPctJr = document.querySelector('input[name="cal_absent_pct_jr"]');

        // Sr. School
        const totalSr = document.querySelector('input[name="cal_total_sr"]');
        const expectedSr = document.querySelector('input[name="cal_expected_sr"]');
        const presentPctSr = document.querySelector('input[name="cal_present_pct_sr"]');
        const absentPctSr = document.querySelector('input[name="cal_absent_pct_sr"]');

        function calcAndSetPct(totalInput, expectedInput, presentPctInput, absentPctInput) {
            const total = parseFloat(totalInput.value) || 0;
            const expected = parseFloat(expectedInput.value) || 0;
            let presentPct = 0;
            let absentPct = 0;
            if (total > 0) {
                presentPct = (expected / total) * 100;
                absentPct = 100 - presentPct;
            }
            presentPctInput.value = presentPct ? presentPct.toFixed(2) : '';
            absentPctInput.value = absentPct ? absentPct.toFixed(2) : '';
        }

        if (totalJr && expectedJr && presentPctJr && absentPctJr) {
            [totalJr, expectedJr].forEach(input => {
                input.addEventListener('input', function() {
                    calcAndSetPct(totalJr, expectedJr, presentPctJr, absentPctJr);
                });
            });
        }
        if (totalSr && expectedSr && presentPctSr && absentPctSr) {
            [totalSr, expectedSr].forEach(input => {
                input.addEventListener('input', function() {
                    calcAndSetPct(totalSr, expectedSr, presentPctSr, absentPctSr);
                });
            });
        }
    }

    setupCalendarScheduleCalculations();

    // Auto-calculate Present % for Students Attendance
    function setupStudentAttendanceCalculations() {
        const groups = [
            { str: 'att_str_kg', present: 'att_present_kg', pct: 'att_present_pct_kg' },
            { str: 'att_str_g15', present: 'att_present_g15', pct: 'att_present_pct_g15' },
            { str: 'att_str_g610', present: 'att_present_g610', pct: 'att_present_pct_g610' },
            { str: 'att_str_g1112', present: 'att_present_g1112', pct: 'att_present_pct_g1112' },
            { str: 'att_str_overall', present: 'att_present_overall', pct: 'att_present_pct_overall' }
        ];
        groups.forEach(group => {
            const strInput = document.querySelector(`input[name="${group.str}"]`);
            const presentInput = document.querySelector(`input[name="${group.present}"]`);
            const pctInput = document.querySelector(`input[name="${group.pct}"]`);
            if (strInput && presentInput && pctInput) {
                [strInput, presentInput].forEach(input => {
                    input.addEventListener('input', function() {
                        const str = parseFloat(strInput.value) || 0;
                        const present = parseFloat(presentInput.value) || 0;
                        let pct = 0;
                        if (str > 0) {
                            pct = (present / str) * 100;
                        }
                        pctInput.value = pct ? pct.toFixed(2) : '';
                    });
                });
            }
        });
    }

    setupStudentAttendanceCalculations();

    // Set up dynamic filtering for School Counsellor (KK vs Others)
    function setupSchoolCounsellorFiltering() {
        const kkOptions = ['Gadgets', 'Family', 'Behaviour', 'Peer Issues', 'Body Shaming', 'Relationship Curiosity', 'Teacher', 'Loneliness', 'Sibling', 'Self-Esteem', 'Fear', 'General Counselling', 'Self-Harm', 'Completed', 'Total'];
        const otherOptions = ['Follow-Up', 'Teachers', 'KK.,Individual', 'Sp.Kid', 'Teachers Referral', 'New', 'Total'];

        function populateSubtopics(selectElem, list) {
            selectElem.innerHTML = '<option value="">Select...</option>';
            list.forEach(opt => {
                const optionEl = document.createElement('option');
                optionEl.value = opt.toLowerCase().replace(/\\s+/g, '_').replace(/[.,]/g, '');
                optionEl.textContent = opt;
                selectElem.appendChild(optionEl);
            });
        }

        function setupRow(row) {
            const categorySelect = row.querySelector('.rapid-category-select');
            const subtopicSelect = row.querySelector('.rapid-subtopic-select');
            if (!categorySelect || !subtopicSelect) return;
            const refresh = () => {
                const list = (categorySelect.value === 'kk') ? kkOptions : otherOptions;
                populateSubtopics(subtopicSelect, list);
            };
            categorySelect.addEventListener('change', refresh);
            refresh();
        }

        // Initialize existing rows
        document.querySelectorAll('#school-counsellor-tbody tr').forEach(setupRow);

        // Expose for dynamically added rows
        window.setupSchoolCounsellorRow = setupRow;
    }

    // Auto-calculate % for AEP Attendance, Extended Class Attendance, and Team Weekly Meeting
    function setupAEPAndExtendedAndMeetingCalculations() {
        // 19. AEP Attendance
        const aepGroups = [
            { str: 'aep_str_g11', enr: 'aep_enr_g11', enrpct: 'aep_enrpct_g11', exp: 'aep_exp_g11', att: 'aep_att_g11', attpct: 'aep_attpct_g11' },
            { str: 'aep_str_g12', enr: 'aep_enr_g12', enrpct: 'aep_enrpct_g12', exp: 'aep_exp_g12', att: 'aep_att_g12', attpct: 'aep_attpct_g12' }
        ];
        aepGroups.forEach(group => {
            const strInput = document.querySelector(`input[name="${group.str}"]`);
            const enrInput = document.querySelector(`input[name="${group.enr}"]`);
            const enrpctInput = document.querySelector(`input[name="${group.enrpct}"]`);
            const expInput = document.querySelector(`input[name="${group.exp}"]`);
            const attInput = document.querySelector(`input[name="${group.att}"]`);
            const attpctInput = document.querySelector(`input[name="${group.attpct}"]`);
            // Enrollment %
            if (strInput && enrInput && enrpctInput) {
                [strInput, enrInput].forEach(input => {
                    input.addEventListener('input', function() {
                        const str = parseFloat(strInput.value) || 0;
                        const enr = parseFloat(enrInput.value) || 0;
                        let pct = 0;
                        if (str > 0) {
                            pct = (enr / str) * 100;
                        }
                        enrpctInput.value = pct ? pct.toFixed(2) : '';
                    });
                });
            }
            // Attendance %
            if (expInput && attInput && attpctInput) {
                [expInput, attInput].forEach(input => {
                    input.addEventListener('input', function() {
                        const exp = parseFloat(expInput.value) || 0;
                        const att = parseFloat(attInput.value) || 0;
                        let pct = 0;
                        if (exp > 0) {
                            pct = (att / exp) * 100;
                        }
                        attpctInput.value = pct ? pct.toFixed(2) : '';
                    });
                });
            }
        });

        // 20. Extended Class Attendance
        const ecGroups = [
            { str: 'ec_str_g35', enr: 'ec_enr_g35', enrpct: 'ec_enrpct_g35', exp: 'ec_exp_g35', att: 'ec_att_g35', attpct: 'ec_attpct_g35' },
            { str: 'ec_str_g68', enr: 'ec_enr_g68', enrpct: 'ec_enrpct_g68', exp: 'ec_exp_g68', att: 'ec_att_g68', attpct: 'ec_attpct_g68' },
            { str: 'ec_str_g910', enr: 'ec_enr_g910', enrpct: 'ec_enrpct_g910', exp: 'ec_exp_g910', att: 'ec_att_g910', attpct: 'ec_attpct_g910' },
            { str: 'ec_str_g1112', enr: 'ec_enr_g1112', enrpct: 'ec_enrpct_g1112', exp: 'ec_exp_g1112', att: 'ec_att_g1112', attpct: 'ec_attpct_g1112' }
        ];
        ecGroups.forEach(group => {
            const strInput = document.querySelector(`input[name="${group.str}"]`);
            const enrInput = document.querySelector(`input[name="${group.enr}"]`);
            const enrpctInput = document.querySelector(`input[name="${group.enrpct}"]`);
            const expInput = document.querySelector(`input[name="${group.exp}"]`);
            const attInput = document.querySelector(`input[name="${group.att}"]`);
            const attpctInput = document.querySelector(`input[name="${group.attpct}"]`);
            // Enrollment %
            if (strInput && enrInput && enrpctInput) {
                [strInput, enrInput].forEach(input => {
                    input.addEventListener('input', function() {
                        const str = parseFloat(strInput.value) || 0;
                        const enr = parseFloat(enrInput.value) || 0;
                        let pct = 0;
                        if (str > 0) {
                            pct = (enr / str) * 100;
                        }
                        enrpctInput.value = pct ? pct.toFixed(2) : '';
                    });
                });
            }
            // Attendance %
            if (expInput && attInput && attpctInput) {
                [expInput, attInput].forEach(input => {
                    input.addEventListener('input', function() {
                        const exp = parseFloat(expInput.value) || 0;
                        const att = parseFloat(attInput.value) || 0;
                        let pct = 0;
                        if (exp > 0) {
                            pct = (att / exp) * 100;
                        }
                        attpctInput.value = pct ? pct.toFixed(2) : '';
                    });
                });
            }
        });

        // 22. Team Weekly Meeting
        const meetGroups = [
            { str: 'meet_str_kg', att: 'meet_att_kg', pct: 'meet_attpct_kg' },
            { str: 'meet_str_12', att: 'meet_att_12', pct: 'meet_attpct_12' },
            { str: 'meet_str_35', att: 'meet_att_35', pct: 'meet_attpct_35' },
            { str: 'meet_str_68', att: 'meet_att_68', pct: 'meet_attpct_68' },
            { str: 'meet_str_910', att: 'meet_att_910', pct: 'meet_attpct_910' },
            { str: 'meet_str_1112', att: 'meet_att_1112', pct: 'meet_attpct_1112' }
        ];
        meetGroups.forEach(group => {
            const strInput = document.querySelector(`input[name="${group.str}"]`);
            const attInput = document.querySelector(`input[name="${group.att}"]`);
            const pctInput = document.querySelector(`input[name="${group.pct}"]`);
            if (strInput && attInput && pctInput) {
                [strInput, attInput].forEach(input => {
                    input.addEventListener('input', function() {
                        const str = parseFloat(strInput.value) || 0;
                        const att = parseFloat(attInput.value) || 0;
                        let pct = 0;
                        if (str > 0) {
                            pct = (att / str) * 100;
                        }
                        pctInput.value = pct ? pct.toFixed(2) : '';
                    });
                });
            }
        });
    }

    setupSchoolCounsellorFiltering();
    setupAEPAndExtendedAndMeetingCalculations();
});
