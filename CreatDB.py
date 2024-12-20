import sqlite3


def import_data():
    cn = sqlite3.connect('data/questions.db')

    sql = '''INSERT INTO questions ("question","option_a","option_b",
    "option_c", "option_d", "correct_answer", "level") VALUES (?,?,?,?,?,?,?)'''

    cur = cn.cursor()

    with open("data/Questions.txt", "r") as f:
       for line in f:
            r = line.strip().split("\t")
            cur.execute(sql, (r[0],r[1],r[2],r[3],r[4],int(r[5]),int(r[6])))

    cn.commit()
    cn.close()

import_data()