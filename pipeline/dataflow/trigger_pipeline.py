import os
import mysql
import mysql.connector
import csv

def run_duplicates_job():
    os.system('mvn compile exec:java   -Dexec.mainClass=com.example.Duplicates')


def get_duplicates_output():
    os.system('gsutil cp gs://duplicates/outputs/* duplicates-output/')


def put_database_input_to_bucket():
    os.system('gsutil cp database-input/question-id.csv gs://duplicates')


def get_database_inputs():
    connection = mysql.connector.connect(user='root', passwd='', host='127.0.0.1', db='scalica')
    cursor = connection.cursor()
    query = "SELECT text,id FROM micro_question;"

    with open('database-input/question-id.csv', 'wb') as question_id_csv:
        writer = csv.writer(question_id_csv, delimiter=',')

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            for row in results:
                writer.writerow(row)

        except:
            print "Unable to fetch data"


def put_duplicate_answers_in_db():
    connection = mysql.connector.connect(user='root', passwd='', host='127.0.0.1', db='scalica')
    cursor = connection.cursor()
    query = 'UPDATE micro_question SET duplicate_of_id = {original_id} WHERE id = {duplicate_id};'

    with open('duplicates-output/duplicates.csv') as duplicates_csv:
        reader = csv.reader(duplicates_csv, delimiter=',')
        for row in reader:
            if len(row) < 2:
                continue

            if len(row) > 2: # question is a duplicate
                duplicate_question_ids = map(int, row[1:])
                duplicate_question_ids.sort()

                original_id = duplicate_question_ids[0]
                duplicate_ids = duplicate_question_ids[1:]

                for duplicate_id in duplicate_ids:
                    try:
                        cursor.execute(query.format(original_id=original_id, duplicate_id=duplicate_id))
                        connection.commit()

                        print query.format(original_id=original_id, duplicate_id=duplicate_id)
                        print "SUCCESS {duplicate_id}".format(duplicate_id=duplicate_id)
                    except:
                        print "FAIL {duplicate_id}".format(duplicate_id=duplicate_id)
                        connection.rollback()

    connection.close()


def main():
    get_database_inputs()
    put_database_input_to_bucket()
    run_duplicates_job()
    get_duplicates_output()
    put_duplicate_answers_in_db()

main()
