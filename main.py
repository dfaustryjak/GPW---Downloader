#!/usr/bin/env python
# -*- coding: utf8 -*-
import wget
import os
import datetime
import re
from datetime import date, timedelta
from mysql_insert import insert_to_database


def extract_beetween_td(current_line):
    current_line = current_line.split(">")[1].strip()
    current_line = current_line.rsplit('<', 1)[0]
    current_line = current_line.replace('&nbsp;', '')
    return current_line


def read_parse_insert(file_name,date):
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
                name = name.replace(".", "")
                # print("name " +  name)

                shortcut = line_iter.__next__()
                shortcut = extract_beetween_td(shortcut)
                # print("shortcut " + shortcut)


                currency = line_iter.__next__()
                currency = extract_beetween_td(currency)
                # print("currency " + currency)

                open_value = line_iter.__next__()
                open_value = extract_beetween_td(open_value)
                open_value = open_value.replace(",", ".")

                max = line_iter.__next__()
                max = extract_beetween_td(max)
                max = max.replace(",", ".")

                min = line_iter.__next__()
                min = extract_beetween_td(min)
                min = min.replace(",", ".")


                close = line_iter.__next__()
                close = extract_beetween_td(close)
                close = close.replace(",", ".")

                percent_change = line_iter.__next__()
                percent_change = extract_beetween_td(percent_change)
                percent_change = percent_change.replace(",", ".")

                volume = line_iter.__next__()
                volume = extract_beetween_td(volume)
                volume = volume.replace('&nbsp;','')
                volume = volume.replace(",", ".")

                transactions = line_iter.__next__()
                transactions = extract_beetween_td(transactions)
                transactions = transactions.replace('&nbsp;', '')
                transactions = transactions.replace(",", ".")

                value_of_trading = line_iter.__next__()
                value_of_trading = extract_beetween_td(value_of_trading)
                value_of_trading = value_of_trading.replace(",", ".")

                if(open_value == '0,00'):
                    # print("Revert Values")
                    open_value=close
                    max=close
                    min=close

                if(name == "DROP" or name == "OPONEO.PL"):
                    break

                insert_to_database(name,open_value,max,min,close,date,percent_change,volume,transactions,value_of_trading)
                # print("open " + open_value)
                # print("max " + max)
                # print("min " + min)
                # print("close " + close)
                # print("date " + date)
                # print("percent_change " + percent_change)
                # print("volume " + volume)
                # print("transactions " + transactions)
                # print("value_of_trading " + value_of_trading)
                # print("OK")
                # print(date)
                # print("====================")

    f.close()
    return 1

def Downloader():

    print("===== BEGIN =====")
    now = datetime.datetime.now()

    lim = '1991-04-16'
    end_date = now.strftime("%Y-%m-%d")


    #change it if you wat read actions from custom data
    history_reader = 1

    condition = 1
    counter_for_date = 1


    current_date = end_date
    while(condition):
        print("\n" * 80)
        if history_reader:
            print("= = = = = P A R S I N G  = = = = = " + str(current_date))

            #print("End date we have - > " + str(end_date) + " Start date we have -> " + str(start_date))
            file_url = 'https://www.gpw.pl/notowania_archiwalne_full?type=10&date='+str(current_date)
            #file_url = 'https://www.gpw.pl/notowania_archiwalne_full?type=10&date=1991-04-24'
            local_file = str(current_date) + "_gpw_info.txt"
            file_name = wget.download(file_url, local_file)
            result = read_parse_insert(local_file,str(current_date))
            if result == 1:
                print("Read - ok Parse - ok Insert - ok , I can delete files")
                os.remove(local_file)
                current_date = date.today() - timedelta(counter_for_date)
                counter_for_date+=1
                print("< - - - - - OK - - - - > ")
                print(str(current_date))
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


if __name__ == '__main__':
    Downloader()


