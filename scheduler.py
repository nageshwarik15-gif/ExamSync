
from collections import defaultdict


def generate_timetable(subjects, enrollments, exam_dates, time_slots):
    """
    Generate a timetable using preferred dates and time slots
    for the four ExamSync subjects.

    subjects: list of (subject_id, subject_code, subject_name)
    enrollments: list of (student_id, subject_id)
    exam_dates: list of dates in YYYY-MM-DD format
    time_slots: list of time slot names
    """

    if not subjects:
        raise ValueError("Add at least one subject before scheduling.")

    if not exam_dates or not time_slots:
        raise ValueError("Provide at least one exam date and time slot.")

    # Preferred schedule based on subject codes.
    preferred_schedule = {
        "CUCS1004": ("2026-11-16", "09:00 AM - 12:00 PM"),
        "CUTM1674": ("2026-11-17", "09:00 AM - 12:00 PM"),
        "CUTM1004": ("2026-11-18", "02:00 PM - 05:00 PM"),
        "CUGG1004": ("2026-11-19", "02:00 PM - 05:00 PM"),
    }

    available_slots = {
        (exam_date, time_slot)
        for exam_date in exam_dates
        for time_slot in time_slots
    }

    subject_by_id = {subject[0]: subject for subject in subjects}
    subject_ids = set(subject_by_id)

    student_subjects = defaultdict(set)

    for student_id, subject_id in enrollments:
        if subject_id in subject_ids:
            student_subjects[student_id].add(subject_id)

    conflicts = {subject_id: set() for subject_id in subject_ids}

    for enrolled_subjects in student_subjects.values():
        for subject_id in enrolled_subjects:
            conflicts[subject_id].update(
                enrolled_subjects - {subject_id}
            )

    assigned = {}

    # First assign the preferred slots to subjects with known codes.
    for subject_id, code, name in subjects:
        if code not in preferred_schedule:
            continue

        preferred_slot = preferred_schedule[code]

        if preferred_slot not in available_slots:
            raise ValueError(
                f"The preferred date or time for {name} is unavailable. "
                "Choose November 16–19, 2026, and select both daily "
                "time slots."
            )

        for other_id, other_slot in assigned.items():
            if other_id in conflicts[subject_id] and other_slot == preferred_slot:
                raise ValueError(
                    f"A clash would occur between {name} and "
                    f"{subject_by_id[other_id][2]}."
                )

        assigned[subject_id] = preferred_slot

    # Schedule any additional subjects without preferred slots.
    remaining = subject_ids - set(assigned)

    slots = sorted(available_slots)

    for subject_id in sorted(
        remaining,
        key=lambda sid: len(conflicts[sid]),
        reverse=True,
    ):
        for slot in slots:
            if all(
                assigned.get(other_id) != slot
                for other_id in conflicts[subject_id]
            ):
                assigned[subject_id] = slot
                break
        else:
            raise ValueError(
                f"Could not schedule {subject_by_id[subject_id][2]} "
                "without an examination clash. Add more dates or slots."
            )

    return [
        (subject_id, assigned[subject_id][0], assigned[subject_id][1])
        for subject_id in subject_ids
    ]
