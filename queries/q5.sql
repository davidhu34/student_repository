-- student grades summary
select students.Name, students.CWID, grades.Course, grades.Grade, instructors.Name
from grades
join instructors on instructors.CWID = grades.InstructorCWID
join students on students.CWID = grades.StudentCWID
order by students.Name;