'''Student Repository

    Data repository of courses, students, and instructors

    Author: Ming-Wei Hu
    Last Updated: November 16th, 2020

'''
# Imports
from datetime import datetime, timedelta
from typing import Iterator, Tuple, List, Dict, Set, IO, Any, Callable, Optional
from decimal import Decimal, ROUND_HALF_UP
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

        except (UniversityFilesInvalid, UniversityDataInvalid) as e:
            print(e)

    return inner_function


LETTER_GRADE_MINIMUM = 'C'
LETTER_GRADE_VALUE = {
    'A': Decimal('4.00'),
    'A-': Decimal('3.75'),
    'B+': Decimal('3.25'),
    'B': Decimal('3.00'),
    'B-': Decimal('2.75'),
    'C+': Decimal('2.25'),
    'C': Decimal('2.00'),
    'C-': Decimal('0.00'),
    'D+': Decimal('0.00'),
    'D': Decimal('0.00'),
    'D-': Decimal('0.00'),
    'F': Decimal('0.00'),
}


class Student:
    ''' student object for University '''

    def __init__(self, cwid: str, name: str, major: str) -> None:
        ''' initialize object with student data '''
        self.cwid: str = cwid
        self.name: str = name
        self.major: str = major
        # initialize course record Dict[course_name, (instructor_grade)] for courses
        self.courses_by_name: Dict[str, List[Tuple[str]]] = {}

    def add_course(self, course_name: str, instructor_cwid: str, letter_grade: str):
        ''' add a record to course of name '''
        # add to dict if first time taking the course
        if course_name not in self.courses_by_name:
            self.courses_by_name[course_name] = []

        self.courses_by_name[course_name].append(
            (instructor_cwid, letter_grade))

    def get_latest_passing_grade(self, course_name: str) -> Optional[str]:
        ''' get latest passing grade'''
        # never taken the course
        if course_name not in self.courses_by_name:
            return None

        course_records: List[Tuple[str]] = self.courses_by_name[course_name]
        # get latest passed grade of course
        for instructor_cwid, letter_grade in reversed(course_records):
            if LETTER_GRADE_VALUE[letter_grade] >= LETTER_GRADE_VALUE[LETTER_GRADE_MINIMUM]:
                return letter_grade

        # no passing grade
        return None

    def is_course_completed(self, course_name: str) -> bool:
        ''' check if course of name is completed '''
        return self.get_latest_passing_grade(course_name) != None

    def get_completed_course_names(self) -> List[str]:
        ''' get completed course names '''
        return sorted([
            course_name
            for course_name in self.courses_by_name.keys()
            if self.is_course_completed(course_name)
        ])

    def get_gpa(self) -> Decimal:
        ''' get average GPA '''
        scores: List[Decimal] = []

        # get all course grades for counting
        # for course_records in self.courses_by_name.values():
        #     for instructor_cwid, letter_grade in course_records:
        #         scores.append(LETTER_GRADE_VALUE[letter_grade])

        # get passed course grades for counting (at most one for each course)
        for course_name in reversed(self.courses_by_name.keys()):
            # get latest passed grade for counting
            latest_letter_grade: str = self.get_latest_passing_grade(
                course_name)
            if latest_letter_grade != None:
                scores.append(LETTER_GRADE_VALUE[latest_letter_grade])

        # no completed courses
        if not scores:
            return Decimal('0.00')

        # get mean of confidence occurances
        else:
            return sum(scores) / len(scores)

    def get_gpa_display(self) -> str:
        ''' rounded GPA string display '''
        gpa: Decimal = self.get_gpa()
        # round up Decimal object to percision 2
        rounded_gpa: Decimal = gpa.quantize(
            Decimal('.01'), rounding=ROUND_HALF_UP)
        gpa_str: str = f'{rounded_gpa}'
        return gpa_str[:-1] if gpa_str[-1] == '0' else gpa_str


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


class Major:
    ''' major object for University '''

    def __init__(self, name: str) -> None:
        ''' initialize object with course data '''
        self.name: str = name
        # initialize course containers
        self.required_course_name_set: Set[str] = set()
        self.elective_course_name_set: Set[str] = set()

    def has_course(self, course_name: str):
        ''' check if the course is included in this major '''
        return course_name in self.required_course_name_set \
            or course_name in self.elective_course_name_set

    def add_required_course_name(self, course_name: str):
        ''' add a required course name '''
        self.required_course_name_set.add(course_name)

    def add_elective_course_name(self, course_name: str):
        ''' add an elective course name '''
        self.elective_course_name_set.add(course_name)


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
    MAJOR_FILE_NAME: str = "majors.txt"

    def __init__(self, directory: str) -> None:
        ''' initialize object with data file directory '''
        # validate directory
        self.directory: str = abspath(directory)
        if not isdir(self.directory):
            raise UniversityFilesInvalid(
                f'"{directory}" is not a valid directory.')

        # validate required files
        missing_files = str = ", ".join([f'"{file_name}"' for file_name in [
            University.MAJOR_FILE_NAME,
            University.STUDENT_FILE_NAME,
            University.INSTRUCTOR_FILE_NAME,
            University.GRADE_FILE_NAME,
        ] if not isfile(join(self.directory, file_name))])
        if missing_files:
            raise UniversityFilesInvalid(
                f'{missing_files} does not exist in "{directory}".')

        # data containers placeholders
        self.major: Dict[str, Major] = {}
        self.students: Dict[str, Student] = {}
        self.instructors: Dict[str, Instructor] = {}
        self.courses: Dict[Tuple[str], Course] = {}

        # read data from required files
        try:
            self.__parse_majors()
            self.__parse_students()
            self.__parse_instructors()
            self.__parse_grades()

        # handle unmatched fields
        except ValueError as e:
            raise UniversityDataInvalid(f'{e}')

    def __parse_majors(self):
        ''' read data from majors.txt '''

        # temp Dict
        majors: Dict[str, Major] = {}
        path = join(self.directory, University.MAJOR_FILE_NAME)

        for data in file_reader(path, 3, header=True):
            if all(data):
                # read data tuple from file reader generator
                name, r_or_e, course_name = data

                if name not in majors:
                    majors[name] = Major(name)

                major: Major = majors[name]

                if major.has_course(course_name):
                    # handle duplicate major course entries
                    raise UniversityDataInvalid(
                        f'Duplicate course data of "{name}": "{course_name}".')

                elif r_or_e == 'R':
                    majors[name].add_required_course_name(course_name)
                elif r_or_e == 'E':
                    majors[name].add_elective_course_name(course_name)

                else:
                    # handle unknown course type entries
                    raise UniversityDataInvalid(
                        f'Invalid Required/Elective type for "{course_name}" of "{name}".')

            # handle missing value from a data entry
            else:
                raise UniversityDataInvalid(
                    'Missing value(s) in majors file.')

        # overwrite university students data with file data stored in temp
        self.majors = majors

    def __parse_students(self):
        ''' read data from students.txt '''

        # temp Dict
        students: Dict[str, Student] = {}
        path = join(self.directory, University.STUDENT_FILE_NAME)

        for data in file_reader(path, 3, ';', True):
            if all(data):
                # read data tuple from file reader generator
                cwid, name, major_name = data

                # handle unknown major of University
                if major_name not in self.majors:
                    raise UniversityDataInvalid(
                        f'Unknown major {major_name} for student {cwid}.')

                # handle duplicate entries
                if cwid in students:
                    raise UniversityDataInvalid(
                        f'Duplicate student data: {cwid}.')

                students[cwid] = Student(cwid, name, major_name)

            # handle missing value from a data entry
            else:
                raise UniversityDataInvalid(
                    'Missing value(s) in students file.')

        # overwrite university students data with file data stored in temp
        self.students = students

    def __parse_instructors(self):
        ''' read data from instructors.txt '''

        # temp Dict
        instructors: Dict[str, Instructor] = {}
        path = join(self.directory, University.INSTRUCTOR_FILE_NAME)

        for data in file_reader(path, 3, '|', True):
            if all(data):
                # read data tuple from file reader generator
                cwid, name, department = data

                # handle unknown major/department of University
                if department not in self.majors:
                    raise UniversityDataInvalid(
                        f'Unknown department {department} for instructor {cwid}.')

                # handle duplicate entries
                if cwid in instructors:
                    raise UniversityDataInvalid(
                        f'Duplicate instructor data: {cwid}.')

                instructors[cwid] = Instructor(cwid, name, department)

            # handle missing value from a data entry
            else:
                raise UniversityDataInvalid(
                    'Missing value(s) in intructors file.')

        # overwrite university data with file data stored in temp
        self.instructors = instructors

    def __parse_grades(self):
        ''' read data from grades.txt '''

        # temp Dict
        courses: Dict[Tuple[str], Course] = {}
        path = join(self.directory, University.GRADE_FILE_NAME)

        for data in file_reader(path, 4, '|', True):
            if all(data):
                # read data tuple from file reader generator
                student_cwid, course_name, letter_grade, instructor_cwid = data
                # use course name and instructor as unique course identifier
                course_key: Tuple[str] = (course_name, instructor_cwid)

                # handle unknown student of grade
                if student_cwid not in self.students:
                    raise UniversityDataInvalid(
                        f'Unknown student {student_cwid} for grade data.')

                # handle unknown instructor of grade
                if instructor_cwid not in self.instructors:
                    raise UniversityDataInvalid(
                        f'Unknown instructor {instructor_cwid} for grade data.')

                # initialize course object on first grade entry
                if course_key not in courses:
                    courses[course_key] = Course(*course_key)

                # update grade data in course
                courses[course_key].update_letter_grade(
                    student_cwid, letter_grade)

                # udpate grade data of university student
                self.students[student_cwid].add_course(
                    course_name, instructor_cwid, letter_grade)

                # udpate university instructor's instructed courses
                self.instructors[instructor_cwid].add_course(course_name)

            # handle missing value from a data entry
            else:
                raise UniversityDataInvalid(
                    'Missing value(s) in intructors file.')

        # overwrite university course data with file data stored in temp
        self.courses = courses

    def pretty_print_major_summary(self):
        ''' print out major summary in pretty table '''
        field_names: List[str] = [
            'Major',
            'Required Course',
            'Electives',
        ]
        pt: PrettyTable = PrettyTable(field_names=field_names)

        # add rows from university instructors
        for name, major in self.majors.items():
            pt.add_row([
                name,
                sorted(major.required_course_name_set),
                sorted(major.elective_course_name_set),
            ])

        # print
        print('Major Summary')
        print(pt)

    def pretty_print_student_summary(self):
        ''' print out student summary in pretty table '''
        field_names: List[str] = [
            'CWID',
            'Name',
            'Major',
            'Completed Courses',
            'Remaing Required',
            'Remaing Electives',
            'GPA',
        ]
        pt: PrettyTable = PrettyTable(field_names=field_names)

        # add rows from university students
        for cwid, student in self.students.items():
            # get major object of student
            major: Major = self.majors[student.major]
            # get sorted course names from Student
            completed_courses: List[str] = sorted(
                student.get_completed_course_names())
            # check if any elective completed
            elective_done: bool = any([
                course_name in major.elective_course_name_set
                for course_name in completed_courses
            ])

            pt.add_row([
                cwid,
                student.name,
                major.name,
                completed_courses,
                # filter major courses by checking if course is completed
                [
                    course_name
                    for course_name in major.required_course_name_set
                    if not student.is_course_completed(course_name)
                ],
                # [] if no more elective required to graduate
                [] if elective_done else [
                    course_name
                    for course_name in major.elective_course_name_set
                    if not student.is_course_completed(course_name)
                ],
                student.get_gpa_display()
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
    university.pretty_print_major_summary()
    university.pretty_print_student_summary()
    university.pretty_print_instructor_summary()

    return university


def main() -> None:
    ''' loop and prompt for university repository '''
    while True:
        prompt_university_repo()


if __name__ == "__main__":
    main()
