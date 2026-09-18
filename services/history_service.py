import re
import json
from datetime import datetime, timedelta, date, time
from flask import url_for
from models import CAPA_STATUS_LABELS
from repositories.history_repository import (
    get_model_meta,
    get_form_choices,
    fetch_capa_history,
    fetch_form_history
)

# Common prefixes to strip for cleaner human labels
PREFIX_PATTERNS = [
    r'^transfer_certificate_', r'^transfer_', r'^parent_activity_', r'^parent_visit_', r'^parent_',
    r'^exam_schedule_', r'^exam_', r'^late_coming_', r'^late_', r'^admission_', r'^grooming_',
    r'^sick_bay_', r'^sick_', r'^pc_detail_', r'^pc_', r'^dwud_', r'^hsc_', r'^disc_',
    r'^cal_', r'^att_', r'^asa_', r'^ext_', r'^ud_', r'^oc_', r'^mp_', r'^sec_', r'^aep_',
    r'^ec_', r'^sc_', r'^st_', r'^train_', r'^cert_', r'^meet_', r'^log_', r'^hostel_',
    r'^rapid_', r'^scholorius_', r'^exit_', r'^concern_', r'^kural_', r'^sal_pend_', r'^sal_',
    r'^obs_', r'^rec_pend_acad_', r'^rec_pend_admin_', r'^rec_act_acad_', r'^rec_act_admin_',
    r'^rec_', r'^hr_att_jr_school_', r'^hr_att_sr_school_', r'^hr_att_eca_',
    r'^hr_att_acad_overall_', r'^hr_att_admin_overall_', r'^hr_att_admin_',
    r'^hr_att_drivers_', r'^hr_att_sec_', r'^hr_att_hk_', r'^hr_att_cond_',
    r'^hr_att_', r'^hr_'
]

EM_DASH = '\u2014'


def _parse_column_group_and_label(col_name):
    """Analyze a database column name to determine its subcategory group and human-friendly label.
    
    This ensures multi-category forms (e.g. Jr/Sr school, Kindergarten/Grades 1-5/6-10,
    Document types, Power sources, Staff types, Boards) display all their columns organized under clear categories.
    """
    group_name = "Submission Details"
    clean_name = col_name

    # Check for category infixes and prefixes first
    if col_name.startswith('rec_pend_acad_'):
        group_name = "Academic Staff Vacancies"
        clean_name = col_name[14:]
    elif col_name.startswith('rec_pend_admin_'):
        group_name = "Admin Staff Vacancies"
        clean_name = col_name[15:]
    elif col_name.startswith('rec_act_acad_'):
        group_name = "Academic Vacancies & Activity"
        clean_name = col_name[13:]
    elif col_name.startswith('rec_act_admin_'):
        group_name = "Admin Vacancies & Activity"
        clean_name = col_name[14:]
    elif col_name.startswith('hr_att_jr_school_'):
        group_name = "Junior School Staff Attendance"
        clean_name = col_name[17:]
    elif col_name.startswith('hr_att_sr_school_'):
        group_name = "Senior School Staff Attendance"
        clean_name = col_name[17:]
    elif col_name.startswith('hr_att_eca_'):
        group_name = "Extra-Curricular (ECA) Attendance"
        clean_name = col_name[11:]
    elif col_name.startswith('hr_att_acad_overall_'):
        group_name = "Academic Staff Overall Attendance"
        clean_name = col_name[20:]
    elif col_name.startswith('hr_att_admin_overall_'):
        group_name = "Admin Staff Overall Attendance"
        clean_name = col_name[21:]
    elif col_name.startswith('hr_att_admin_'):
        group_name = "Administrative Staff Attendance"
        clean_name = col_name[13:]
    elif col_name.startswith('hr_att_drivers_'):
        group_name = "Transport Drivers Attendance"
        clean_name = col_name[15:]
    elif col_name.startswith('hr_att_sec_'):
        group_name = "Security Personnel Attendance"
        clean_name = col_name[11:]
    elif col_name.startswith('hr_att_hk_'):
        group_name = "Housekeeping Staff Attendance"
        clean_name = col_name[10:]
    elif col_name.startswith('hr_att_cond_'):
        group_name = "Bus Conductors Attendance"
        clean_name = col_name[12:]
    elif col_name.startswith('doc_new_'):
        group_name = "New Documents Received"
        clean_name = col_name[8:]
    elif col_name.startswith('doc_nonret_'):
        group_name = "Non-Returnable Documents Issued"
        clean_name = col_name[11:]
    elif col_name.startswith('doc_orig_'):
        group_name = "Original Documents Returned"
        clean_name = col_name[9:]
    elif col_name.startswith('eb_') and not col_name.startswith('eb_details'):
        group_name = "EB Power Supply"
        clean_name = col_name[3:]
    elif col_name.startswith('solar_') and not col_name.startswith('solar_details'):
        group_name = "Solar Power Generation"
        clean_name = col_name[6:]
    elif col_name.startswith('genset_') and not col_name.startswith('genset_details'):
        group_name = "Genset Generator"
        clean_name = col_name[7:]
    # Check for category suffixes
    elif col_name.endswith('_jr'):
        group_name = "Junior School"
        clean_name = col_name[:-3]
    elif col_name.endswith('_sr'):
        group_name = "Senior School"
        clean_name = col_name[:-3]
    elif col_name.endswith('_kg'):
        group_name = "Kindergarten (KG)"
        clean_name = col_name[:-3]
    elif col_name.endswith('_12'):
        group_name = "Grades 1 to 2"
        clean_name = col_name[:-3]
    elif col_name.endswith('_35') or col_name.endswith('_g35'):
        group_name = "Grades 3 to 5"
        clean_name = col_name[:-4] if col_name.endswith('_g35') else col_name[:-3]
    elif col_name.endswith('_g15'):
        group_name = "Grades 1 to 5"
        clean_name = col_name[:-4]
    elif col_name.endswith('_68') or col_name.endswith('_g68'):
        group_name = "Grades 6 to 8"
        clean_name = col_name[:-4] if col_name.endswith('_g68') else col_name[:-3]
    elif col_name.endswith('_910') or col_name.endswith('_g910'):
        group_name = "Grades 9 to 10"
        clean_name = col_name[:-5] if col_name.endswith('_g910') else col_name[:-4]
    elif col_name.endswith('_g610'):
        group_name = "Grades 6 to 10"
        clean_name = col_name[:-5]
    elif col_name.endswith('_1112') or col_name.endswith('_g1112'):
        group_name = "Grades 11 to 12"
        clean_name = col_name[:-6] if col_name.endswith('_g1112') else col_name[:-5]
    elif col_name.endswith('_g11'):
        group_name = "Grade 11"
        clean_name = col_name[:-4]
    elif col_name.endswith('_g12'):
        group_name = "Grade 12"
        clean_name = col_name[:-4]
    elif col_name.endswith('_overall'):
        group_name = "Overall Summary"
        clean_name = col_name[:-8]
    elif col_name.endswith('_paid'):
        group_name = "Paid Activities"
        clean_name = col_name[:-5]
    elif col_name.endswith('_reg'):
        group_name = "Regular Activities"
        clean_name = col_name[:-4]
    elif col_name.endswith('_rifle'):
        group_name = "Rifle Shooting"
        clean_name = col_name[:-6]
    elif col_name.endswith('_ncc'):
        group_name = "NCC"
        clean_name = col_name[:-4]
    elif col_name.endswith('_cbse'):
        group_name = "CBSE Board"
        clean_name = col_name[:-5]
    elif col_name.endswith('_cisce') or col_name.endswith('_cis'):
        group_name = "CISCE Board"
        clean_name = col_name[:-6] if col_name.endswith('_cisce') else col_name[:-4]
    elif col_name.endswith('_state'):
        group_name = "State Board"
        clean_name = col_name[:-6]
    elif col_name.endswith('_emis'):
        group_name = "EMIS Portal"
        clean_name = col_name[:-5]
    elif col_name.endswith('_cambridge'):
        group_name = "Cambridge Board"
        clean_name = col_name[:-10]
    elif col_name.endswith('_ib'):
        group_name = "IB Board"
        clean_name = col_name[:-3]

    # Strip domain-specific redundant prefixes
    for pat in PREFIX_PATTERNS:
        clean_name = re.sub(pat, '', clean_name)

    # Convert special terms & abbreviations
    clean_name = re.sub(r'_pct$', ' %', clean_name)
    clean_name = re.sub(r'_perc$', ' %', clean_name)
    clean_name = re.sub(r'_desc$', ' Description', clean_name)
    clean_name = re.sub(r'_status$', ' Status', clean_name)
    clean_name = re.sub(r'_no$', ' Number', clean_name)

    # Specific well-known exact column mappings
    exact_map = {
        'rw_230_240': 'R-Phase Voltage (230-240V)',
        'yw_230_240': 'Y-Phase Voltage (230-240V)',
        'bw_230_240': 'B-Phase Voltage (230-240V)',
        'max_demand_104': 'Max Demand (104 KVA)',
        'units_per_day': 'Units Consumed / Day',
        'media_file_id': 'Attached Document / Media',
        'footage_file_id': 'Attached Footage File',
        'file_id': 'Attached File',
        'sec_md_mom_review': 'MD MoM Review Status',
        'sec_atr_completion_status': 'ATR Completion Status',
        'sec_meeting_status': 'SEC Meeting Status',
        'sec_next_meeting': 'Next Meeting Schedule',
        'sec_committee': 'Committee Name',
        'sec_schedule': 'Meeting Schedule',
    }

    if col_name in exact_map:
        return group_name, exact_map[col_name]
    if clean_name in exact_map:
        return group_name, exact_map[clean_name]

    # Word-level mappings
    word_map = {
        'str': 'Total Strength',
        'att': 'Attended',
        'notatt': 'Not Attended',
        'present': 'Present',
        'absent': 'Absent',
        'leave': 'On Leave',
        'enr': 'Enrolled',
        'enrpct': 'Enrolled %',
        'attpct': 'Attendance %',
        'prog': 'Program',
        'exp': 'Expected',
        'subj': 'Subject',
        'appln': 'Applications',
        'dc': 'DC',
        'inv': 'Invoice',
        'po': 'PO',
        'qty': 'Quantity',
        'inf': 'Informed',
        'disc': 'Disciplinary',
        'hsc': 'Communication',
        's': 'S.No',
        'sno': 'S.No',
        'tc': 'TC',
        'ela': 'ELA',
        'cctv': 'CCTV',
        'gps': 'GPS',
        'bsnl': 'BSNL',
        'ro': 'RO',
        'tds': 'TDS',
        'ph': 'pH',
        'eb': 'EB',
        'ac': 'AC',
        'mom': 'MoM',
        'md': 'MD',
        'atr': 'ATR',
        'sec': 'SEC',
        'aep': 'AEP',
        'sen': 'SEN',
        'eca': 'ECA',
        'emis': 'EMIS',
        'cbse': 'CBSE',
        'cisce': 'CISCE',
        'cis': 'CISCE',
        'vac': 'Vacancies',
        'nos': 'Numbers',
        'pos': 'Position',
        'desig': 'Designation',
        'dept': 'Department',
        'cat': 'Category',
        'media_file_id': 'Attached Document / Media',
        'footage_file_id': 'Attached Footage File',
    }

    if clean_name in word_map:
        label = word_map[clean_name]
    else:
        parts = clean_name.split('_')
        converted = [word_map.get(p.lower(), p.title()) for p in parts if p]
        label = ' '.join(converted)

    return group_name, label or col_name.replace('_', ' ').title()


def _format_display_value(val, col_name=''):
    """Format any database value for human display, returning (formatted_string, is_empty)."""
    if val is None or val == '':
        return EM_DASH, True

    if isinstance(val, bool):
        return ('Yes' if val else 'No'), False

    if isinstance(val, (datetime, date)):
        fmt = '%b %d, %Y' if isinstance(val, date) and not isinstance(val, datetime) else '%b %d, %Y %I:%M %p'
        return val.strftime(fmt), False

    if isinstance(val, time):
        return val.strftime('%I:%M %p'), False

    if isinstance(val, float):
        if 'pct' in col_name.lower() or 'percent' in col_name.lower() or 'perc' in col_name.lower():
            return f"{val:.1f}%", False
        return f"{val:.2f}", False

    if isinstance(val, int):
        return str(val), False

    # JSON fields
    if isinstance(val, (dict, list)):
        try:
            if isinstance(val, dict):
                items = []
                for k, v in val.items():
                    if isinstance(v, dict):
                        sub = ', '.join(f"{sk}: {sv}" for sk, sv in v.items() if sv not in (None, ''))
                        items.append(f"{k.title()}: {sub}")
                    else:
                        items.append(f"{k.title()}: {v}")
                return (' | '.join(items) if items else EM_DASH), (not bool(items))
            elif isinstance(val, list):
                return (', '.join(str(x) for x in val) if val else EM_DASH), (not bool(val))
        except Exception:
            return str(val), False

    # Check if string is serialized JSON
    str_val = str(val).strip()
    if (str_val.startswith('{') and str_val.endswith('}')) or (str_val.startswith('[') and str_val.endswith(']')):
        try:
            parsed = json.loads(str_val)
            return _format_display_value(parsed, col_name)
        except Exception:
            pass

    return str_val, False


def serialize_form_record(record, model_name):
    """Safely serialize an operational form model instance into clean display data.
    
    CRITICAL: Guarantees 100% of the model's defined columns are accounted for.
    Never drops empty fields; empty values are formatted cleanly as '—'.
    File attachments (media_file_id, footage_file_id) are converted to working download links.
    Nested JSON structures (ASA sports/general) are unpacked into category groups.
    """
    meta = get_model_meta(model_name)
    excluded_cols = {'form_id', 'team_id', 'submitted_by', 'submitted_at'}

    # Retrieve all defined table columns
    columns = [c for c in record.__table__.columns if c.name not in excluded_cols] if hasattr(record, '__table__') else []

    groups_map = {}
    flat_data_fields = {}

    for col in columns:
        col_name = col.name
        raw_val = getattr(record, col_name, None)

        # Handle nested dictionary JSON columns (like ASA sports/general attendance)
        if isinstance(raw_val, dict) and any(isinstance(v, dict) for v in raw_val.values()):
            for sub_group_key, sub_dict in raw_val.items():
                if not isinstance(sub_dict, dict):
                    continue
                display_group = sub_group_key.replace('_', ' ').title()
                if display_group not in groups_map:
                    groups_map[display_group] = []
                for sk, sv in sub_dict.items():
                    _, s_label = _parse_column_group_and_label(sk)
                    s_disp, s_empty = _format_display_value(sv, sk)
                    groups_map[display_group].append({
                        'name': f"{col_name}.{sub_group_key}.{sk}",
                        'label': s_label,
                        'value': s_disp,
                        'is_empty': s_empty,
                        'link_url': None
                    })
                    flat_data_fields[f"{display_group} - {s_label}"] = s_disp
            continue

        is_file_col = 'file_id' in col_name or col_name.endswith('_file')
        group_name, clean_label = _parse_column_group_and_label(col_name)

        if is_file_col:
            link_url = f"/file/{raw_val}" if (raw_val and isinstance(raw_val, (int, str)) and str(raw_val).isdigit()) else None
            display_val = f"View Attached File (#{raw_val})" if link_url else EM_DASH
            is_empty = not bool(link_url)
        else:
            link_url = None
            display_val, is_empty = _format_display_value(raw_val, col_name)

        field_obj = {
            'name': col_name,
            'label': clean_label,
            'value': display_val,
            'is_empty': is_empty,
            'link_url': link_url
        }

        if group_name not in groups_map:
            groups_map[group_name] = []
        groups_map[group_name].append(field_obj)

        flat_data_fields[clean_label] = display_val

    # Convert groups_map to ordered list of groups
    groups_list = []
    total_fields_count = 0
    for g_title, g_fields in groups_map.items():
        groups_list.append({
            'group_title': g_title,
            'fields': g_fields
        })
        total_fields_count += len(g_fields)

    return {
        'type': 'form',
        'category': meta['dept_name'],
        'badge_class': meta['badge'],
        'reference': f"REF-#{record.form_id}",
        'title': meta['title'],
        'form_key': model_name,
        'form_id': record.form_id,
        'submitted_at': record.submitted_at,
        'status': 'Submitted',
        'status_label': 'Submitted',
        'status_css': 'capa-closed',
        'user_relation': 'Submitter',
        'detail_url': None,
        'data_fields': flat_data_fields,
        'data_groups': groups_list,
        'column_count': total_fields_count or len(columns)
    }


def serialize_capa_record(record, user_id):
    """Serialize a CAPA audit finding with rich workflow metadata and full column preservation."""
    status_label = CAPA_STATUS_LABELS.get(record.status, record.status.replace('_', ' ').title())
    status_css = getattr(record, 'status_css', 'capa-pending-recipient')

    if record.recipient_id == user_id:
        relation = 'Assigned Recipient'
    elif record.submitted_by == user_id:
        relation = 'Auditor / Creator'
    elif record.capa_1_submitted_by == user_id:
        relation = 'CAPA 1 Author'
    elif record.capa_2_submitted_by == user_id:
        relation = 'CAPA 2 Author'
    else:
        relation = 'Participant'

    detail_url = None
    try:
        detail_url = url_for('critical.finding_detail', finding_id=record.form_id)
    except Exception:
        pass

    # Group 1: Audit Observation Details
    obs_fields = [
        {'label': 'Audit Reference', 'value': record.audit_reference or f"AUD-#{record.form_id}", 'is_empty': False, 'link_url': None},
        {'label': 'Audit Date', 'value': record.audit_date.strftime('%b %d, %Y') if record.audit_date else '—', 'is_empty': not bool(record.audit_date), 'link_url': None},
        {'label': 'Audited By', 'value': record.audited_by or '—', 'is_empty': not bool(record.audited_by), 'link_url': None},
        {'label': 'Staff Name', 'value': record.staff_name or '—', 'is_empty': not bool(record.staff_name), 'link_url': None},
        {'label': 'Grade', 'value': record.grade or '—', 'is_empty': not bool(record.grade), 'link_url': None},
        {'label': 'Section', 'value': record.section or '—', 'is_empty': not bool(record.section), 'link_url': None},
        {'label': 'Component', 'value': record.component or '—', 'is_empty': not bool(record.component), 'link_url': None},
        {'label': 'Specification', 'value': record.specification or '—', 'is_empty': not bool(record.specification), 'link_url': None},
        {'label': 'Nature of Issue', 'value': record.nature_of_issue or '—', 'is_empty': not bool(record.nature_of_issue), 'link_url': None},
        {'label': 'Priority', 'value': record.priority or '—', 'is_empty': not bool(record.priority), 'link_url': None},
        {'label': 'Frequency', 'value': record.frequency or '—', 'is_empty': not bool(record.frequency), 'link_url': None},
        {'label': 'Description', 'value': record.description or '—', 'is_empty': not bool(record.description), 'link_url': None},
        {'label': 'Remark', 'value': record.remark or '—', 'is_empty': not bool(record.remark), 'link_url': None},
    ]

    # Group 2: CAPA Resolution & Workflow
    capa_fields = [
        {'label': 'Assigned Recipient', 'value': (record.recipient.username if getattr(record, 'recipient', None) else f"User #{record.recipient_id}") if record.recipient_id else '—', 'is_empty': not bool(record.recipient_id), 'link_url': None},
        {'label': 'Current Status', 'value': status_label, 'is_empty': False, 'link_url': None},
        {'label': 'Action Taken Report (ATR)', 'value': record.action_taken_report or '— (Pending)', 'is_empty': not bool(record.action_taken_report), 'link_url': None},
        {'label': 'Root Cause Analysis (RCA)', 'value': record.root_cause_analysis or '— (Pending)', 'is_empty': not bool(record.root_cause_analysis), 'link_url': None},
        {'label': 'CAPA 1 (Corrective Action)', 'value': record.capa_1 or '— (Pending)', 'is_empty': not bool(record.capa_1), 'link_url': None},
        {'label': 'CAPA 2 (Preventive Action)', 'value': record.capa_2 or '— (Pending)', 'is_empty': not bool(record.capa_2), 'link_url': None},
        {'label': 'Audit Decision', 'value': record.audit_decision or '— (Pending Review)', 'is_empty': not bool(record.audit_decision), 'link_url': None},
        {'label': 'Audit Justification', 'value': record.audit_justification or '—', 'is_empty': not bool(record.audit_justification), 'link_url': None},
    ]

    groups_list = [
        {'group_title': 'Audit Observation Details', 'fields': obs_fields},
        {'group_title': 'CAPA Workflow & Resolution', 'fields': capa_fields}
    ]

    flat_data_fields = {f['label']: f['value'] for f in obs_fields + capa_fields}

    return {
        'type': 'capa',
        'category': 'Quality Audit & CAPA',
        'badge_class': 'badge-capa',
        'reference': record.audit_reference or f"AUD-#{record.form_id}",
        'title': record.title,
        'form_key': 'CapaFinding',
        'form_id': record.form_id,
        'submitted_at': record.submitted_at,
        'status': record.status,
        'status_label': status_label,
        'status_css': status_css,
        'user_relation': relation,
        'priority': record.priority,
        'detail_url': detail_url,
        'data_fields': flat_data_fields,
        'data_groups': groups_list,
        'column_count': len(obs_fields) + len(capa_fields)
    }


def get_user_history_rows(user_id, start=None, end=None, form_query=None, category='all', search_query=None):
    """Fetch, filter, and construct clean historical activity records for a user."""
    start_dt = None
    end_dt = None
    try:
        if start:
            start_dt = datetime.strptime(start, '%Y-%m-%d')
        if end:
            end_dt = datetime.strptime(end, '%Y-%m-%d') + timedelta(days=1)
    except Exception:
        start_dt = None
        end_dt = None

    history_rows = []
    category = (category or 'all').lower().strip()

    # 1. Fetch CAPA Findings if requested
    if category in ('all', 'capa') and (not form_query or form_query == 'CapaFinding'):
        capa_records = fetch_capa_history(user_id, start_dt, end_dt)
        for cr in capa_records:
            history_rows.append(serialize_capa_record(cr, user_id))

    # 2. Fetch Operational Form Submissions if requested
    if category in ('all', 'forms') and form_query != 'CapaFinding':
        form_results = fetch_form_history(user_id, start_dt, end_dt, form_query)
        for model_name, records in form_results:
            for r in records:
                history_rows.append(serialize_form_record(r, model_name))

    # 3. Apply keyword search filter across reference, title, or field values if provided
    if search_query:
        sq = search_query.lower().strip()
        filtered = []
        for row in history_rows:
            matched = (
                sq in row['reference'].lower() or
                sq in row['title'].lower() or
                sq in row.get('status_label', '').lower() or
                any(sq in k.lower() or sq in str(v).lower() for k, v in row['data_fields'].items())
            )
            if matched:
                filtered.append(row)
        history_rows = filtered

    # 4. Sort overall records chronologically (newest first)
    history_rows.sort(key=lambda x: x['submitted_at'] if x['submitted_at'] else datetime.min, reverse=True)

    # 5. Compute summary statistics
    total_count = len(history_rows)
    forms_count = sum(1 for r in history_rows if r['type'] == 'form')
    capa_count = sum(1 for r in history_rows if r['type'] == 'capa')

    return {
        'rows': history_rows,
        'total_count': total_count,
        'forms_count': forms_count,
        'capa_count': capa_count,
        'form_choices': get_form_choices()
    }
