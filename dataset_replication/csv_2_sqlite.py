def create_connection(db_file):
    import sqlite3
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn


def read_csv(file):
    import csv
    import sys

    maxInt = sys.maxsize

    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

    header = []
    raw_file = []
    with open(file, encoding="utf8") as f:
        reader = csv.reader(f, quotechar='"', delimiter=',',
                            quoting=csv.QUOTE_ALL)
        for fr in reader:
            raw_file.append(fr)
    header = raw_file[0]

    data = []
    for row in raw_file[1:]:
        j = 0
        dic_row = {}
        current_col = ""
        for i in header:
            new_col = i
            if current_col == i:
                new_col = i + "_" + str(j)
            try:
                dic_row[new_col] = row[j]
            except IndexError:
                dic_row[new_col] = ""
            j += 1

            current_col = i
        data.append(dic_row)

    return data


def load_cvs_folder(folder=""):
    import os

    content = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".csv"):
                content.extend(read_csv(folder + "/" + file))

    return content


def make_JOS_dataset(content=[]):
    cases = []
    for raw_case in content:
        case = {"id": "", "corpus": "", "actual_effort": 0.0, "expert_estimated_effort": 0.0, "features": ""}
        log_work_counter = 0
        comment_counter = 0
        for key in raw_case.keys():
            if "summary" == key.lower(): case["corpus"] = "\n".join([case["corpus"], raw_case[key]])
            if "description" == key.lower(): case["corpus"] = "\n".join([case["corpus"], raw_case[key]])
            if "issue key" == key.lower(): case["id"] = raw_case[key]
            try:
                if "time spent" == key.lower(): case["actual_effort"] = float(raw_case[key])
            except Exception:
                print(e)
            if "original estimate" == key.lower() and raw_case[key] != "": case["expert_estimated_effort"] = float(
                raw_case[key])
            if "log work" in key.lower() and raw_case[key] != "": log_work_counter += 1
            if "comment" in key.lower() and raw_case[key] != "": comment_counter += 1
        if "\n" == case["corpus"][:1]: case["corpus"] = case["corpus"][1:]
        case["features"] = ";".join(["num_comments:" + str(comment_counter), "num_logs:" + str(log_work_counter)])
        if "apache" in raw_case["Project description"].lower() or "apache" in raw_case["Project url"].lower():
            case["reference"] = "https://issues.apache.org/jira/browse/" + case["id"]
        if "jboss" in raw_case["Project description"].lower() or "jboss" in raw_case["Project url"].lower():
            case["reference"] = "https://issues.redhat.com/browse/" + case["id"]
        if "spring" in raw_case["Project description"].lower() or "spring" in raw_case["Project url"].lower():
            case["reference"] = "https://jira.spring.io/browse/" + case["id"]
        cases.append(case)
    return cases


def db_inseration(db, content=[]):
    conn = create_connection(db)
    cur = conn.cursor()

    # create table `case` if not exist
    cur.execute('''CREATE TABLE IF NOT EXISTS "case" (
			"id"	TEXT NOT NULL UNIQUE,
			"corpus"	TEXT,
			"features"	TEXT,
			"expert_estimated_effort"	NUMERIC,
			"actual_effort"	NUMERIC,
			"reference"	TEXT
		)''')


    for case in content:
        sql = "insert into `case`( `" + "`,`".join(case.keys()) + "`) values(" + ",".join(
            ["?" for i in case.values()]) + ")"
        cur.execute(sql, [i for i in case.values()])
    conn.commit()

if __name__ == "__main__":
    from datetime import date
    today = date.today()
    today_date = today.strftime("%d%m%Y")

    folder = input("What is the folder full path that contains CSV files:\n")
    content = load_cvs_folder(folder)

    dataset = make_JOS_dataset(content)
    db_inseration("D:\\JOS_original_"+today_date+".sqlite3", dataset)
