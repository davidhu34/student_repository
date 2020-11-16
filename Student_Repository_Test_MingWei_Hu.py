"""Student_Repository (Tests)

    Data repository of courses, students, and instructors (Tests)

    Author: Ming-Wei Hu
    Last Updated: November 16th, 2020

"""
# imports
from unittest import TestCase, main
from typing import List, Tuple, Dict, Set

from Student_Repository_MingWei_Hu import University, Student, Instructor, Course
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
        test_letter_grade_2: str = 'B'
        s.update_letter_grade(
            (test_course_instructor_cwid_1, test_course_name_1), test_letter_grade_1)
        s.update_letter_grade(
            (test_course_instructor_cwid_2, test_course_name_2), test_letter_grade_2)

        expected_letter_grades: Dict[Tuple[str], str] = {
            (test_course_instructor_cwid_1, test_course_name_1): test_letter_grade_1,
            (test_course_instructor_cwid_2, test_course_name_2): test_letter_grade_2,
        }
        self.assertDictEqual(expected_letter_grades, s.letter_grades)


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
        test_letter_grade_2: str = 'A'
        c.update_letter_grade(test_course_student_cwid_1, test_letter_grade_1)
        c.update_letter_grade(test_course_student_cwid_2, test_letter_grade_2)

        expected_letter_grades: Dict[str, str] = {
            f'{test_course_student_cwid_1}': test_letter_grade_1,
            f'{test_course_student_cwid_2}': test_letter_grade_2,
        }
        self.assertDictEqual(expected_letter_grades, c.letter_grades)


class UniversityTest(TestCase):
    def test_university(self):
        ''' testing University '''
        # test using data under ./stevens
        # instantiate University
        stevens: University = University('./stevens')

        # test students
        students_data: Set[Tuple[str]] = set([
            (cwid, student.name, student.major)
            for cwid, student in stevens.students.items()
        ])
        test_stevens_students_data: List[Tuple[str]] = [
            ('10103', 'Baldwin, C', 'SFEN'),
            ('10115', 'Wyatt, X', 'SFEN'),
            ('10172', 'Forbes, I', 'SFEN'),
            ('10175', 'Erickson, D', 'SFEN'),
            ('10183', 'Chapman, O', 'SFEN'),
            ('11399', 'Cordova, I', 'SYEN'),
            ('11461', 'Wright, U', 'SYEN'),
            ('11658', 'Kelly, P', 'SYEN'),
            ('11714', 'Morton, A', 'SYEN'),
            ('11788', 'Fuller, E', 'SYEN'),
        ]
        self.assertSetEqual(students_data, set(test_stevens_students_data))

        # test instructors
        instructors_data: Set[Tuple[str]] = set([
            (cwid, instructor.name, instructor.department)
            for cwid, instructor in stevens.instructors.items()
        ])
        test_stevens_instructors_data: List[Tuple[str]] = [
            ('98765', 'Einstein, A', 'SFEN'),
            ('98764', 'Feynman, R', 'SFEN'),
            ('98763', 'Newton, I', 'SFEN'),
            ('98762', 'Hawking, S', 'SYEN'),
            ('98761', 'Edison, A', 'SYEN'),
            ('98760', 'Darwin, C', 'SYEN'),
        ]
        self.assertSetEqual(instructors_data, set(
            test_stevens_instructors_data))

        # test grades (and courses)
        test_stevens_grades_data: List[Tuple[str]] = [
            ('10103', 'SSW 567', 'A', '98765'),
            ('10103', 'SSW 564', 'A-', '98764'),
            ('10103', 'SSW 687', 'B', '98764'),
            ('10103', 'CS 501', 'B', '98764'),
            ('10115', 'SSW 567', 'A', '98765'),
            ('10115', 'SSW 564', 'B+', '98764'),
            ('10115', 'SSW 687', 'A', '98764'),
            ('10115', 'CS 545', 'A', '98764'),
            ('10172', 'SSW 555', 'A', '98763'),
            ('10172', 'SSW 567', 'A-', '98765'),
            ('10175', 'SSW 567', 'A', '98765'),
            ('10175', 'SSW 564', 'A', '98764'),
            ('10175', 'SSW 687', 'B-', '98764'),
            ('10183', 'SSW 689', 'A', '98763'),
            ('11399', 'SSW 540', 'B', '98765'),
            ('11461', 'SYS 800', 'A', '98760'),
            ('11461', 'SYS 750', 'A-', '98760'),
            ('11461', 'SYS 611', 'A', '98760'),
            ('11658', 'SSW 540', 'F', '98765'),
            ('11714', 'SYS 611', 'A', '98760'),
            ('11714', 'SYS 645', 'C', '98760'),
            ('11788', 'SSW 540', 'A', '98765'),
        ]

        grades_data_by_course: Set[Tuple[str]] = set()
        [
            [
                grades_data_by_course.add(
                    (student_cwid, course_key[0], letter_grade, course_key[1]))
                for student_cwid, letter_grade in course.letter_grades.items()
            ]
            for course_key, course in stevens.courses.items()
        ]
        self.assertSetEqual(grades_data_by_course,
                            set(test_stevens_grades_data))

        grades_data_by_students: Set[Tuple[str]] = set()
        [
            [
                grades_data_by_students.add(
                    (student_cwid, course_key[0], letter_grade, course_key[1]))
                for course_key, letter_grade in student.letter_grades.items()
            ]
            for student_cwid, student in stevens.students.items()
        ]
        self.assertSetEqual(grades_data_by_students,
                            set(test_stevens_grades_data))

        # test directory exceptions
        self.assertRaises(UniversityFilesInvalid, University, './no_stevens')
        self.assertRaises(UniversityFilesInvalid,
                          University, './empty_stevens')
        self.assertRaises(UniversityFilesInvalid,
                          University, './incomplete_stevens')
        self.assertRaises(UniversityDataInvalid, University,
                          './missing_values_stevens')
        self.assertRaises(UniversityDataInvalid, University,
                          './wrong_student_grades_stevens')
        self.assertRaises(UniversityDataInvalid, University,
                          './wrong_instructor_grades_stevens')
        self.assertRaises(UniversityDataInvalid, University,
                          './wrong_fields_grades_stevens')


if __name__ == "__main__":
    main(exit=False, verbosity=2)
