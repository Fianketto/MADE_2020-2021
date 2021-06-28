--посылки до полного решения
--VIEW
CREATE VIEW v_c1_c13_submissions_cp1251 as
select
	 a.*
	,case	when	a.submission_time > b.first_acc_time
				or	(a.submission_time = b.first_acc_time and a.submission_id < b.first_acc_id)
			then 1 else 0 end as after_solution
	,case	when a.passed_time < a.duration then 1 else 0 end as during_contest
	,case	when a.passed_time < a.duration - 3600 * 24 * 2 then 1 else 0 end as during_soft_deadline 
from c1_c13_submissions_cp1251 a 
left join
	(
		select
			 contest_num
			,nickname 
			,task
			,min(submission_time) as first_acc_time
			,max(submission_id) as first_acc_id
		from c1_c13_submissions_cp1251 ccsc 
		where verdict = "Accepted"
		group by 
			 contest_num
			,nickname 
			,task
	) b
on a.contest_num = b.contest_num and a.nickname = b.nickname and a.task = b.task


--0
select
	 count(*)
	,count(distinct nickname)
	,count(distinct task)
	,count(distinct contest_num)
from v_c1_c13_submissions_cp1251 ccsc

select distinct lang from v_c1_c13_submissions_cp1251 ccsc



--1
--Количество посылок в разбивке "во время контеста/эффективные"
select
	 contest_num
	,during_contest
	,during_soft_deadline
	,after_solution
	,verdict
	,count(*) as submit_count_total
from v_c1_c13_submissions_cp1251 ccsc 
group by
	 contest_num
	,during_contest
	,during_soft_deadline
	,after_solution
	,verdict
	
--2
--Основная разбивка посылок 
select
	 contest_num
	,lang
	,verdict 
	,test_num 
	,nickname 
	,task
	,during_contest
	,after_solution
	,count(*) as submit_count
from v_c1_c13_submissions_cp1251 ccsc
--where during_contest=1 and after_solution=0
group by
	 contest_num
	,lang
	,verdict 
	,test_num 
	,nickname 
	,task
	,during_contest
	,after_solution


--3
--кол-во попыток до полного решения
select
	 a.lang
	,a.task
	,a.contest_num
	,a.nickname
	,b.solution_exists
	,sum(case when verdict = "Accepted" then 0 else 1 end) as try_cnt
from v_c1_c13_submissions_cp1251 a
left join
	(
		select
			 lang
			,task
			,contest_num
			,nickname
			,max(case when verdict = "Accepted" then 1 else 0 end) as solution_exists
		from v_c1_c13_submissions_cp1251 
		where
				during_contest = 1
			and	after_solution = 0
		group by
			 lang
			,task
			,contest_num
			,nickname
		having
			max(case when verdict = "Accepted" then 1 else 0 end) = 1	
	) b
on
		a.lang = b.lang
	and a.task = b.task
	and a.contest_num = b.contest_num
	and a.nickname = b.nickname
where a.during_contest = 1 and a.after_solution = 0 and solution_exists = 1
group by
	 a.lang
	,a.task
	,a.contest_num
	,a.nickname
	,b.solution_exists
	
	
--4
--лучшая ловушка Григория
select
	 contest_num
	,task
	,verdict
	,test_num
	,count(*)
	,count(distinct nickname)
from v_c1_c13_submissions_cp1251 vccsc 
where during_contest = 1 and after_solution = 0 and verdict not in ('Accepted')
group by
	 contest_num
	,task
	,verdict
	,test_num
order by count(*) desc
	


--5
--распределение новых участников
select
	 contest_num
	,nickname
	,min(passed_time)
from v_c1_c13_submissions_cp1251 
where during_contest = 1 and after_solution = 0
group by 
	 contest_num
	,nickname	
	
	
--6
--распределение всех посылок
select
	 contest_num
	,nickname
	,passed_time
from v_c1_c13_submissions_cp1251 
where during_contest = 1 and after_solution = 0





--7 Успешность решения задач по контестам
select
	 contest_num
	,nickname
	,task
	,case when verdict = "Accepted" then 1 else 0 end as solved
	,count(*)
from v_c1_c13_submissions_cp1251 
where during_contest = 1 and after_solution = 0
group by 
	 contest_num
	,nickname
	,task
	,case when verdict = "Accepted" then 1 else 0 end
	
	
	

	
	
--8. Время решения
select
	 contest_num
	,task
	,nickname
	,contest_starts 
	,min(submission_time) as first_solution_time
from v_c1_c13_submissions_cp1251 vccsc 
where during_contest = 1 and verdict = "Accepted"
group by
	 contest_num
	,task
	,nickname
	,contest_starts
order by
	 contest_num
	,task
	,nickname
	
	

	
	

	
--прочее
	(
		select
			 lang
			,task
			,contest_num
			,nickname
			,max(case when verdict = "Accepted" then 1 else 0 end) as solution_exists
		from v_c1_c13_submissions_cp1251 
		where
				during_contest = 1
			and	after_solution = 0
		group by
			 lang
			,task
			,contest_num
			,nickname
		having
			max(case when verdict = "Accepted" then 1 else 0 end) = 1	
	) b
	

	

	
select contest_num, count(DISTINCT task)
from v_c1_c13_submissions_cp1251 
group by contest_num
select
	 case when passed_time < duration then 1 else 0 end as intime
	--,contest_num 
	,count(*)
from c1_c13_submissions_cp1251 ccsc 
group by
	 
	case when passed_time < duration then 1 else 0 end
	--,contest_num

 

	
	
select
	nickname, lang, count(*)
from c1_c13_submissions_cp1251 ccsc 
where passed_time < duration
and (nickname in ('Fianketto', 'IlyaPCP', 'dyakin.nikolay', 'munin.evgenii') )
group by nickname, lang
order by nickname desc, count(*) desc, lang 



select
	nickname, verdict, count(*)
from c1_c13_submissions_cp1251 ccsc 
where passed_time < duration
and (nickname in ('Fianketto', 'IlyaPCP', 'dyakin.nikolay', 'munin.evgenii') )
group by nickname, verdict
order by nickname desc, count(*) desc, verdict


select
	nickname
	,count(*)
	,case when nickname in ('Fianketto', 'IlyaPCP', 'dyakin.nikolay', 'munin.evgenii') then 1 else 0 end as we

from c1_c13_submissions_cp1251 ccsc 
where passed_time < duration
group by
	nickname
	,case when nickname in ('Fianketto', 'IlyaPCP', 'dyakin.nikolay', 'munin.evgenii') then 1 else 0 end
order by
	(case when nickname in ('Fianketto', 'IlyaPCP', 'dyakin.nikolay', 'munin.evgenii') then 1 else 0 end) desc
	,count(*) desc
	,nickname




select
	 contest_num
	,count(*) as submit_count_total
	,sum(case when passed_time < duration then 1 else 0 end) as submit_count_before_deadline
	,sum(case when passed_time < duration then after_solution else 0 end) as submit_count_wo_refactor
from v_c1_c13_submissions_cp1251 ccsc 
group by contest_num
order by contest_num





	