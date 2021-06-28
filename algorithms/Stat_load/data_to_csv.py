import datetime as dt

months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

first_contest_starts = dt.datetime(2020, 9, 12, 17, 0, 0)
first_contest_ends = dt.datetime(2020, 9, 18, 23, 55, 0)
contest_count = 13
period = 7
contest_time = []
for i in range(contest_count):
    t1 = first_contest_starts + dt.timedelta(days=(i * period))
    t2 = first_contest_ends + dt.timedelta(days=(i * period))
    delta = t2 - t1
    duration = delta.days * 24 * 3600 + delta.seconds
    contest_time.append([t1, t2, duration])
    print(t1, t2, delta, duration)
    print(delta.days, delta.seconds)


output_filename = "temp_for_import.csv"
fout = open(output_filename, 'w')
print("contest_num,contest_starts,contest_ends,duration,submission_id,submission_time,passed_time,nickname,task,lang,verdict,test_num,tm,mm", file=fout)


for contest_num in range(1, contest_count + 1):
    input_filename = "content_submissions/all_data_" + str(contest_num) + ".txt"
    fin = open(input_filename)

    i = 0
    for line in fin:
        cells = line.replace("\xa0", "\t").strip().split('\t')
        submission_id = str(contest_num * 1000000 + i)
        datetime = cells[1]
        year, month, day = datetime[7:11], str(months[datetime[0:3]]), datetime[4:6]
        hour, minute = datetime[12:14], datetime[15:17]
        nickname = cells[2]
        task = cells[3]
        lang = cells[4]
        verdict = cells[5]
        tm = cells[6]
        mm = cells[8]
        test_num = "0"

        submission_time = dt.datetime(int(year), int(month), int(day), int(hour), int(minute), 0)
        passed_time = submission_time - contest_time[contest_num - 1][0]
        passed_seconds = str(passed_time.days * 24 * 3600 + passed_time.seconds)

        submission_time_str = submission_time.strftime("%Y-%m-%d %H:%M:%S")
        contest_starts_str = contest_time[contest_num - 1][0].strftime("%Y-%m-%d %H:%M:%S")
        contest_ends_str = contest_time[contest_num - 1][1].strftime("%Y-%m-%d %H:%M:%S")
        duration = contest_time[contest_num - 1][2]

        if " " in verdict:
            if verdict == "Compilation error":
                test_num = "-1"
            else:
                verdict_list = verdict.split(" ")
                test_num = verdict_list[-1]
                verdict = " ".join(verdict_list[:-1])

        cell_list = [str(contest_num), contest_starts_str, contest_ends_str, str(duration),
                     submission_id, submission_time_str, passed_seconds,
                     nickname, task, lang, verdict, test_num, tm, mm]
        row = ",".join(cell_list)
        print(row)
        print(row, file=fout)
        i += 1
    fin.close()


fout.close()
