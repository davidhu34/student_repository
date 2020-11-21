-- name, cwid, and the total courses taken of each student 
select students.Name, students.CWID, count(*) as CourseTaken
from students join grades on students.CWID = grades.StudentCWID
group by students.CWID;