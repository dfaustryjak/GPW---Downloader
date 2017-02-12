import wget
import os
import datetime
import re
from datetime import date, timedelta


def extract_beetween_td(current_line):
    current_line = current_line.split(">")[1].strip()
    current_line = current_line.rsplit('<', 1)[0]
    return current_line


def read_parse_insert(file_name):
    print("START PARSING . . . ")
    print("I just get file " + file_name)
    counter = 0
    f = open(file_name, 'r+')
    print("====================")
    while 1:
        lines = f.readlines()
        if not lines:
            break
        line_iter = iter(lines)
        for line in line_iter:
            check_if_exist = line.__contains__('Brak danych')
            if check_if_exist:
                return 0

            check_if_action_exist = line.__contains__('<td class="left">')
            if check_if_action_exist:
                name = extract_beetween_td(line)
                print("name " +  name)

                shortcut = line_iter.__next__()
                shortcut = extract_beetween_td(shortcut)
                print("shortcut " + shortcut)


                currency = line_iter.__next__()
                currency = extract_beetween_td(currency)
                print("currency " + currency)

                open_value = line_iter.__next__()
                open_value = extract_beetween_td(open_value)


                max = line_iter.__next__()
                max = extract_beetween_td(max)


                min = line_iter.__next__()
                min = extract_beetween_td(min)



                close = line_iter.__next__()
                close = extract_beetween_td(close)


                if(open_value == '0,00'):
                    print("Revert Values")
                    open_value=close
                    max=close
                    min=close


                print("open " + open_value)
                print("max " + max)
                print("min " + min)
                print("close " + close)
                print("====================")

    f.close()
    return 1

def Downloader():

    print("===== BEGIN =====")
    now = datetime.datetime.now()

    lim = '1991-04-16'
    end_date = now.strftime("%Y-%m-%d")


    #change it if you wat read actions from custom data
    history_reader = 0

    condition = 1
    counter_for_date = 1





    current_date = end_date
    while(condition):
        if history_reader:
            print("= = = = = P A R S I N G  = = = = = " + str(current_date))

            #print("End date we have - > " + str(end_date) + " Start date we have -> " + str(start_date))
            file_url = 'https://www.gpw.pl/notowania_archiwalne_full?type=10&date='+str(current_date)
            #file_url = 'https://www.gpw.pl/notowania_archiwalne_full?type=10&date=1991-04-24'
            local_file = str(current_date) + "_gpw_info.txt"
            file_name = wget.download(file_url, local_file)
            result = read_parse_insert(local_file)
            if result == 1:
                print("Read - ok Parse - ok Insert - ok , I can delete files")
                os.remove(local_file)
                current_date = date.today() - timedelta(counter_for_date)
                counter_for_date+=1
            if result == 0:
                print("Cannot find anything, delete tmp file")
                os.remove(local_file)
                current_date = date.today() - timedelta(counter_for_date)
                counter_for_date+=1
            if str(current_date) < lim:
                print("I cannot download anything")
                condition=false

        else:
            print("Enter date manualy")
            print("Date format: YYYY-MM-DD")
            current_date  = input('Enter your input:')
            file_url = 'https://www.gpw.pl/notowania_archiwalne_full?type=10&date=' + str(current_date)
            local_file = str(current_date) + "_gpw_info.txt"
            file_name = wget.download(file_url, local_file)
            result = read_parse_insert(local_file)
            if result == 1:
                print("Read - ok Parse - ok Insert - ok , I can delete files")
                os.remove(local_file)
                break
            if result == 0:
                print("Cannot find anything, delete tmp file")
                os.remove(local_file)
                break




Downloader()