'''Student Repository

    Data repository of courses, students, and instructors

    Author: Ming-Wei Hu
    Last Updated: November 16th, 2020

'''
# Imports
from datetime import datetime, timedelta
from typing import Iterator, Tuple, List, Dict, Set, IO, Any, Callable
from os.path import abspath, basename, join, isdir, isfile
from os import listdir
from prettytable import PrettyTable


# custom exception
class FileNotFound(Exception):
    ''' custom file not found exception'''

    def __init__(self, message, path):
        # construct exception and store erroneous path if given
        super().__init__(message)
        self.path = path


def file_reader(path: str, fields: int, sep: str = '\t', header: bool = False) -> Iterator[Tuple[str]]:
    ''' a generator yielding lines of file from path '''
    # read file from path
    try:
        file: IO = open(path)

    # handle file not found
    except FileNotFoundError:
        raise FileNotFound(f'Cannot open file from "{path}"!', path)

    # yield lines form a generator function
    with file:
        # loop through file line sequence
        line_no: int = 1
        for line in file:
            # remove change line and split by separator
            values: List[str] = line.strip().split(sep)

            # raise ValueError if fields count are incorrect
            if len(values) != fields:
                file_name: str = basename(path)
                raise ValueError(
                    f"'{file_name}' has {len(values)} fields on line {line_no} but expected {fields}")

            # ignore header line if necessary
            if line_no != 1 or not header:
                # transform List to Tuple
                yield tuple(values)

            # increment line number
            line_no += 1


def exception_containment(func):
    ''' decorator for containing exceptions '''
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        # catch and contain exceptions other than keyboard interruptions
        except KeyboardInterrupt:
            quit()

        except Exception as e:
            print(e)

    return inner_function


class Student:
    ''' student object for University '''

    def __init__(self, cwid: str, name: str, major: str) -> None:
        ''' initialize object with student data '''
        self.cwid: str = cwid
        self.name: str = name
        self.major: str = major
        # initialize letter grade Dict[course, grade] for courses
        self.letter_grades: Dict[Tuple[str], str] = {}

    def update_letter_grade(self, course_key: Tuple[str], letter_grade: str = ''):
        ''' update the letter grade of a course '''
        self.letter_grades[course_key] = letter_grade


class Instructor:
    ''' instructor object for University '''

    def __init__(self, cwid: str, name: str, department: str) -> None:
        ''' initialize object with instructor data '''
        self.cwid: str = cwid
        self.name: str = name
        self.department: str = department
        # initialize instructed course name set
        self.course_name_set: Set[str] = set()

    def add_course(self, course_name: str):
        ''' add an instructed course name '''
        self.course_name_set.add(course_name)


class Course:
    ''' course object for University '''

    def __init__(self, name: str, instructor_cwid: str) -> None:
        ''' initialize object with course data '''
        self.name: str = name
        self.instructor_cwid: str = instructor_cwid
        # initialize letter grade Dict[student, grade] for students
        self.letter_grades: Dict[str, str] = {}

    def update_letter_grade(self, student_cwid: str, letter_grade: str):
        ''' update the letter grade of a student '''
        self.letter_grades[student_cwid] = letter_grade


class UniversityFilesInvalid(Exception):
    ''' custom invalid files exception'''

    def __init__(self, message):
        super().__init__(message)


class UniversityDataInvalid(Exception):
    ''' custom invalid data exception'''

    def __init__(self, message):
        super().__init__(message)


class University:
    ''' university object as file data repository '''

    # constants for static file names to read from
    STUDENT_FILE_NAME: str = "students.txt"
    INSTRUCTOR_FILE_NAME: str = "instructors.txt"
    GRADE_FILE_NAME: str = "grades.txt"

    def __init__(self, directory: str) -> None:
        ''' initialize object with data file directory '''
        # validate directory
        self.directory: str = abspath(directory)
        if not isdir(self.directory):
            raise UniversityFilesInvalid(
                f'"{directory}" is not a valid directory.')

        # validate required files
        missing_files = str = ", ".join([f'"{file_name}"' for file_name in [
            University.STUDENT_FILE_NAME,
            University.INSTRUCTOR_FILE_NAME,
            University.GRADE_FILE_NAME,
        ] if not isfile(join(self.directory, file_name))])
        if missing_files:
            raise UniversityFilesInvalid(
                f'{missing_files} does not exist in "{directory}".')

        # data containers placeholders
        self.students: Dict[str, Student] = {}
        self.instructors: Dict[str, Instructor] = {}
        self.courses: Dict[Tuple[str], Course] = {}

        # read data from required files
        try:
            self.__parse_students()
            self.__parse_instructors()
            self.__parse_grades()
        
        # handle unmatched fields
        except ValueError as e:
            raise UniversityDataInvalid(f'{e}')


    # @exception_containment
    def __parse_students(self):
        ''' read data from students.txt '''

        # temp Dict
        students: Dict[str, Student] = {}
        path = join(self.directory, University.STUDENT_FILE_NAME)

        for data in file_reader(path, 3):
            if all(data):
                # read data tuple from file reader generator
                cwid, name, major = data

                # handle duplicate entries
                if cwid in students:
                    raise UniversityDataInvalid(
                        f'Duplicate student data: {cwid}.')

                students[cwid] = Student(cwid, name, major)

            # handle missing value from a data entry
            else:
                raise UniversityDataInvalid(
                    'Missing value(s) in student file.')

        # overwrite university students data with file data stored in temp
        self.students = students

    # @exception_containment
    def __parse_instructors(self):
        ''' read data from instructors.txt '''

        # temp Dict
        instructors: Dict[str, Instructor] = {}
        path = join(self.directory, University.INSTRUCTOR_FILE_NAME)

        for data in file_reader(path, 3):
            if all(data):
                # read data tuple from file reader generator
                cwid, name, department = data

                # handle duplicate entries
                if cwid in instructors:
                    raise UniversityDataInvalid(
                        f'Duplicate instructor data: {cwid}.')

                instructors[cwid] = Instructor(cwid, name, department)

            # handle missing value from a data entry
            else:
                raise UniversityDataInvalid(
                    'Missing value(s) in intructor file.')

        # overwrite university data with file data stored in temp
        self.instructors = instructors

    # @exception_containment
    def __parse_grades(self):
        ''' read data from grades.txt '''

        # temp Dict
        courses: Dict[Tuple[str], Course] = {}
        path = join(self.directory, University.GRADE_FILE_NAME)

        for data in file_reader(path, 4):
            if all(data):
                # read data tuple from file reader generator
                student_cwid, course_name, letter_grade, instructor_cwid = data
                # use course name and instructor as unique course identifier
                course_key: Tuple[str] = (course_name, instructor_cwid)

                # handle unknown student of grade
                if student_cwid not in self.students:
                    raise UniversityDataInvalid(
                        f'No student {student_cwid} for grade data.')

                # handle unknown instructor of grade
                if instructor_cwid not in self.instructors:
                    raise UniversityDataInvalid(
                        f'No instructor {instructor_cwid} for grade data.')

                # initialize course object on first grade entry
                if course_key not in courses:
                    courses[course_key] = Course(*course_key)

                # update grade data in course
                courses[course_key].update_letter_grade(
                    student_cwid, letter_grade)

                # udpate grade data of university student
                self.students[student_cwid].update_letter_grade(
                    course_key, letter_grade)

                # udpate university instructor's instructed courses
                self.instructors[instructor_cwid].add_course(course_name)

            # handle missing value from a data entry
            else:
                raise UniversityDataInvalid(
                    'Missing value(s) in intructor file.')

        # overwrite university course data with file data stored in temp
        self.courses = courses

    def pretty_print_student_summary(self):
        ''' print out student summary in pretty table '''
        field_names: List[str] = [
            'CWID',
            'Name',
            'Completed Courses',
        ]
        pt: PrettyTable = PrettyTable(field_names=field_names)

        # add rows from university students
        for cwid, student in self.students.items():
            pt.add_row([
                cwid,
                student.name,
                # get course names by sorted course keys from Student
                [course_name
                    for course_name, instructor_cwid
                    in sorted(student.letter_grades.keys())],
            ])

        # print
        print('Student Summary')
        print(pt)

    def pretty_print_instructor_summary(self):
        ''' print out instructor summary in pretty table '''
        field_names: List[str] = [
            'CWID',
            'Name',
            'Dept',
            'Course',
            'Students',
        ]
        pt: PrettyTable = PrettyTable(field_names=field_names)

        # add rows from university instructors
        for cwid, instructor in self.instructors.items():
            # add a row for each instructed course
            for course_name in instructor.course_name_set:
                # get Course from university courses
                course: Course = self.courses[(course_name, cwid)]
                pt.add_row([
                    cwid,
                    instructor.name,
                    instructor.department,
                    course_name,
                    # count students by course grades Dict
                    len(course.letter_grades.keys()),
                ])

        # print
        print('Instructor Summary')
        print(pt)


@exception_containment
def prompt_university_repo(dir: str = '') -> University:
    ''' create and display university repository '''
    # prompt for university data directory
    directory: str = dir if dir else input('Enter university data directory: ')
    # create University and read data
    university: University = University(directory)
    # print required information
    university.pretty_print_student_summary()
    university.pretty_print_instructor_summary()

    return university


def main() -> None:
    ''' loop and prompt for university repository '''
    while True:
        prompt_university_repo()


if __name__ == "__main__":
    main()
