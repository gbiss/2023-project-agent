from agent import Student, exchange_contribution, marginal_contribution
from agent.constraint import (
    CoursePreferrenceConstraint,
    CourseSectionConstraint,
    CourseTimeConstraint,
    LinearConstraint,
)
from agent.feature import Course, Section, Slot
from agent.item import ScheduleItem
from agent.valuation import ConstraintSatifactionValuation, StudentValuation


def test_exchange_contribution(
    course_valuation: ConstraintSatifactionValuation, all_items: list[ScheduleItem]
):
    assert (
        exchange_contribution(
            course_valuation, [all_items[0]], all_items[0], all_items[1]
        )
        == True
    )

    assert (
        exchange_contribution(
            course_valuation, [all_items[0], all_items[2]], all_items[2], all_items[1]
        )
        == False
    )


def test_marginal_contribution(
    course_valuation: ConstraintSatifactionValuation, all_items: list[ScheduleItem]
):
    assert marginal_contribution(course_valuation, [all_items[0]], all_items[1]) == 0
    assert marginal_contribution(course_valuation, [all_items[0]], all_items[2]) == 1


def test_student():
    course = Course(["250", "301", "611"])
    slot = Slot(["10am", "12pm", "2pm"])
    section = Section([1, 2, 3])
    features = [course, slot, section]
    items = [
        ScheduleItem(features, ["250", "10am", 1]),
        ScheduleItem(features, ["250", "12pm", 2]),
        ScheduleItem(features, ["301", "12pm", 1]),
        ScheduleItem(features, ["301", "2pm", 2]),
        ScheduleItem(features, ["611", "2pm", 1]),
    ]
    preferred_constr = CoursePreferrenceConstraint.from_course_lists(
        [["250", "301", "611"]], [2], course
    )
    course_time_constr = CourseTimeConstraint.mutually_exclusive_slots(
        items, course, slot
    )
    course_sect_constr = CourseSectionConstraint.one_section_per_course(
        items, course, section
    )
    student = Student(
        StudentValuation([preferred_constr, course_time_constr, course_sect_constr])
    )

    # two non-conflicting courses
    assert student.value([items[0], items[2]]) == 2
    # two courses at the same time
    assert student.value([items[1], items[2]]) == 1
    # two sections of the same course
    assert student.value([items[0], items[1]]) == 1
