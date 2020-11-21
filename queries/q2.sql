-- the total number of students by major
select students.Major, count(*) as NumberOfStudents
from students group by students.Major;