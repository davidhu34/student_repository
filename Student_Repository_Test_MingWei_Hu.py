"""Student_Repository (Tests)

    Data repository of courses, students, and instructors (Tests)

    Author: Ming-Wei Hu
    Last Updated: November 21th, 2020

"""
# imports
from unittest import TestCase, main
from typing import List, Tuple, Dict, Set, Any

from Student_Repository_MingWei_Hu import University, Student, Instructor, Course, Major
from Student_Repository_MingWei_Hu import UniversityFilesInvalid, UniversityDataInvalid


class StudentTest(TestCase):
    def test_student(self):
        ''' testing Student '''
        test_cwid: str = '12345'
        test_name: str = 'Harper, J'
        test_major: str = 'ABC'
        s: Student = Student(test_cwid, test_name, test_major)
        self.assertEqual(test_cwid, s.cwid)
        self.assertEqual(test_name, s.name)
        self.assertEqual(test_major, s.major)

        test_course_instructor_cwid_1: str = '54321'
        test_course_instructor_cwid_2: str = '98765'
        test_course_name_1: str = 'ABC 123'
        test_course_name_2: str = 'EFG 456'
        test_letter_grade_1: str = 'A+'
        test_letter_grade_2: str = 'D'
        test_letter_grade_3: str = 'C'
        s.add_course(
            test_course_name_1, test_course_instructor_cwid_1, test_letter_grade_1)
        s.add_course(
            test_course_name_2, test_course_instructor_cwid_2, test_letter_grade_2)
        s.add_course(
            test_course_name_2, test_course_instructor_cwid_1, test_letter_grade_3)

        expected_courses_by_name: Dict[str, Tuple[str]] = {
            f'{test_course_name_1}': [(test_course_instructor_cwid_1, test_letter_grade_1)],
            f'{test_course_name_2}': [
                (test_course_instructor_cwid_2, test_letter_grade_2),
                (test_course_instructor_cwid_1, test_letter_grade_3),
            ],
        }
        self.assertDictEqual(expected_courses_by_name, s.courses_by_name)


class InstructorTest(TestCase):
    def test_instructor(self):
        ''' testing Instructor '''
        test_cwid: str = '54321'
        test_name: str = 'Scott, M'
        test_department: str = 'DMPC'
        ins: Instructor = Instructor(test_cwid, test_name, test_department)
        self.assertEqual(test_cwid, ins.cwid)
        self.assertEqual(test_name, ins.name)
        self.assertEqual(test_department, ins.department)

        test_course_name_1: str = 'ABC 123'
        test_course_name_2: str = 'EFG 456'
        ins.add_course(test_course_name_1)
        ins.add_course(test_course_name_2)

        expected_course_name_set: Set[str] = {
            test_course_name_1, test_course_name_2}
        self.assertSetEqual(expected_course_name_set, ins.course_name_set)


class CourseTest(TestCase):
    def test_course(self):
        ''' testing Course '''
        test_name: str = 'ABC 123'
        test_instructor_cwid: str = '54321'
        c: Course = Course(test_name, test_instructor_cwid)
        self.assertEqual(test_name, c.name)
        self.assertEqual(test_instructor_cwid, c.instructor_cwid)

        test_course_student_cwid_1: str = '12345'
        test_course_student_cwid_2: str = '56789'
        test_letter_grade_1: str = 'A+'
        test_letter_grade_2: str = 'F'
        test_letter_grade_3: str = 'A'
        c.add_letter_grade(test_course_student_cwid_1, test_letter_grade_1)
        c.add_letter_grade(test_course_student_cwid_2, test_letter_grade_2)
        c.add_letter_grade(test_course_student_cwid_2, test_letter_grade_3)

        expected_letter_grades: Dict[str, List[str]] = {
            f'{test_course_student_cwid_1}': [test_letter_grade_1],
            f'{test_course_student_cwid_2}': [test_letter_grade_2, test_letter_grade_3],
        }
        self.assertDictEqual(expected_letter_grades, c.student_grades)


class MajorTest(TestCase):
    def test_major(self):
        ''' testing Major '''
        test_name: str = 'DMPC'
        m: Major = Major(test_name)
        self.assertEqual(test_name, m.name)

        test_required_course_name_1: str = 'ABC 123'
        test_required_course_name_2: str = 'ABC 456'
        test_elective_course_name_1: str = 'EFG 123'
        test_elective_course_name_2: str = 'EFG 456'
        m.add_required_course_name(test_required_course_name_1)
        m.add_required_course_name(test_required_course_name_2)
        m.add_elective_course_name(test_elective_course_name_1)
        m.add_elective_course_name(test_elective_course_name_2)

        expected_required_course_name_set: Set[str] = {
            test_required_course_name_1, test_required_course_name_2}
        expected_elective_course_name_set: Set[str] = {
            test_elective_course_name_1, test_elective_course_name_2}
        self.assertSetEqual(expected_elective_course_name_set,
                            m.elective_course_name_set)
        self.assertSetEqual(expected_required_course_name_set,
                            m.required_course_name_set)


class UniversityTest(TestCase):
    def test_university(self):
        ''' testing University '''
        # test using data under ./test_suites/basic_university
        # instantiate University
        basic: University = University('./test_suites/basic_university')

        # test majors

        majors_data: Set[Tuple[str]] = set()
        for name, major in basic.majors.items():
            for course_name in major.required_course_name_set:
                majors_data.add((name, 'R', course_name))

            for course_name in major.elective_course_name_set:
                majors_data.add((name, 'E', course_name))

        test_basic_majors_data: List[Tuple[str]] = [
            ('SFEN', 'R', 'SSW 540'),
            ('SFEN', 'R', 'SSW 810'),
            ('SFEN', 'R', 'SSW 555'),
            ('SFEN', 'E', 'CS 501'),
            ('SFEN', 'E', 'CS 546'),
            ('CS', 'R', 'CS 570'),
            ('CS', 'R', 'CS 546'),
            ('CS', 'E', 'SSW 810'),
            ('CS', 'E', 'SSW 565'),
        ]
        self.assertSetEqual(majors_data, set(test_basic_majors_data))

        # test students
        students_data: Set[Tuple[str]] = set([
            (cwid, student.name, student.major)
            for cwid, student in basic.students.items()
        ])
        test_basic_students_data: List[Tuple[str]] = [
            ('10103', 'Jobs, S', 'SFEN'),
            ('10115', 'Bezos, J', 'SFEN'),
            ('10183', 'Musk, E', 'SFEN'),
            ('11714', 'Gates, B', 'CS'),
        ]
        self.assertSetEqual(students_data, set(test_basic_students_data))

        # test instructors
        instructors_data: Set[Tuple[str]] = set([
            (cwid, instructor.name, instructor.department)
            for cwid, instructor in basic.instructors.items()
        ])
        test_basic_instructors_data: List[Tuple[str]] = [
            ('98764', 'Cohen, R', 'SFEN'),
            ('98763', 'Rowland, J', 'SFEN'),
            ('98762', 'Hawking, S', 'CS'),
        ]
        self.assertSetEqual(instructors_data, set(
            test_basic_instructors_data))

        # test grades (and courses)
        test_basic_grades_data: List[Tuple[str]] = [
            ('10103', 'SSW 810', 'A-', '98763'),
            ('10103', 'CS 501', 'B', '98762'),
            ('10115', 'SSW 810', 'A', '98763'),
            ('10115', 'CS 546', 'F', '98762'),
            ('10183', 'SSW 555', 'A', '98763'),
            ('10183', 'SSW 810', 'A', '98763'),
            ('11714', 'SSW 810', 'B-', '98763'),
            ('11714', 'CS 546', 'A', '98764'),
            ('11714', 'CS 570', 'A-', '98762'),
        ]

        grades_data_by_course: Set[Tuple[str]] = set()
        for course_key, course in basic.courses.items():
            for student_cwid, letter_grades in course.student_grades.items():
                for letter_grade in letter_grades:
                    grades_data_by_course.add(
                        (student_cwid, course_key[0], letter_grade, course_key[1]))

        self.assertSetEqual(grades_data_by_course,
                            set(test_basic_grades_data))

        grades_data_by_students: Set[Tuple[str]] = set()
        for student_cwid, student in basic.students.items():
            for course_name, course_records in student.courses_by_name.items():
                for instructor_cwid, letter_grade in course_records:
                    grades_data_by_students.add(
                        (student_cwid, course_name, letter_grade, instructor_cwid))

        self.assertSetEqual(grades_data_by_students,
                            set(test_basic_grades_data))

        # test completed courses and gpa
        expected_basic_student_completed_courses: Dict[str, List[str]] = {
            '10103': ['CS 501', 'SSW 810'],
            '10115': ['SSW 810'],
            '10183': ['SSW 555', 'SSW 810'],
            '11714': ['CS 546', 'CS 570', 'SSW 810'],
        }
        for cwid in expected_basic_student_completed_courses.keys():
            self.assertListEqual(expected_basic_student_completed_courses[cwid],
                                 basic.students[cwid].get_completed_course_names())

        expected_basic_student_gpa_display: Dict[str, str] = {
            '10103': '3.38',
            '10115': '2.0',
            '10183': '4.0',
            '11714': '3.5',
        }
        for cwid in expected_basic_student_completed_courses.keys():
            self.assertEqual(expected_basic_student_gpa_display[cwid],
                             basic.students[cwid].get_gpa_display())

        # test db student grades summary
        expected_student_grades_rows: Set[List[Any]] = set([
            ('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
            ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'),
            ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
            ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'),
            ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'),
            ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
            ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'),
            ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'),
            ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J'),
        ])
        self.assertSetEqual(expected_student_grades_rows, set(
            [tuple(l) for l in University.student_grades_db('student_repository.db')]))

        # test directory exceptions
        self.assertRaises(UniversityFilesInvalid, University,
                          './test_suites/no_such_university')
        self.assertRaises(UniversityFilesInvalid,
                          University, './test_suites/empty_university')
        self.assertRaises(UniversityFilesInvalid,
                          University, './test_suites/incomplete_university')

        # test invalid data exceptions
        self.assertRaises(UniversityDataInvalid, University,
                          './test_suites/missing_values_university')
        self.assertRaises(UniversityDataInvalid, University,
                          './test_suites/wrong_student_grades_university')
        self.assertRaises(UniversityDataInvalid, University,
                          './test_suites/wrong_instructor_grades_university')
        self.assertRaises(UniversityDataInvalid, University,
                          './test_suites/wrong_fields_grades_university')
        self.assertRaises(UniversityDataInvalid, University,
                          './test_suites/wrong_major_student_university')
        self.assertRaises(UniversityDataInvalid, University,
                          './test_suites/wrong_department_instructor_university')

        # test invalid db
        self.assertRaises(UniversityFilesInvalid, University.student_grades_db,
                          './no_such_db.db')
        self.assertRaises(UniversityFilesInvalid, University.student_grades_db,
                          './not_a_db')


if __name__ == "__main__":
    main(exit=False, verbosity=2)
