-- the most frequent grade for SSW 810 across all students
select grades.Grade from grades
where grades.Course = 'SSW 810'
group by grades.Course
order by count(*) desc limit 1;