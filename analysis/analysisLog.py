import os
from datetime import date

import pygal

log_folder_path = "./log/"
result_folder_path = "./result/"

if not os.path.exists(result_folder_path):
    os.makedirs(result_folder_path)


def analysis_overall(file_name):
    logFile = open(log_folder_path + '{0}.txt'.format(file_name), 'r')

    y_test_p = []
    y_test_r = []
    y_test_f = []
    for line in logFile.readlines():
        if "*** Test: " in line:
            items = line.split('; ')
            f = float(items[-1].split(': ')[1])
            r = float(items[-2].split(': ')[1])
            p = float(items[-3].split(': ')[1])
            y_test_f.append(f)
            y_test_r.append(r)
            y_test_p.append(p)

    line_chart = pygal.Line()
    line_chart.title = "Overall performance"
    # line_chart.x_labels = x
    line_chart.add("p", y_test_p)
    line_chart.add("r", y_test_r)
    line_chart.add("f", y_test_f)
    line_chart.render_to_file(result_folder_path + 'Overall_{0}.svg'.format(file_name))
    return y_test_p, y_test_r, y_test_f


def analysis_acc(file_name):
    logFile = open(log_folder_path + '{0}.txt'.format(file_name), 'r')

    index = 0
    x = []
    y_acc = []
    for line in logFile.readlines():
        if "Instance" in line:
            index += 1
            acc = line.split('=')[1].split('\n')[0]
            x.append(index)
            y_acc.append(float(acc))

    line_chart = pygal.Line()
    line_chart.title = "Acc Performance"
    # line_chart.x_labels = x
    line_chart.add("Acc", y_acc)
    line_chart.render_to_file(result_folder_path + 'Acc_{0}.svg'.format(file_name))
    return


def compare_logs(*file_names):
    p_chart = pygal.Line()
    p_chart.title = "Precious compare"

    r_chart = pygal.Line()
    r_chart.title = "Recall compare"

    f_chart = pygal.Line()
    f_chart.title = "F1 Score compare"

    for file_name in file_names:
        p, r, f = analysis_overall(file_name)
        p_chart.add(file_name, p)
        r_chart.add(file_name, r)
        f_chart.add(file_name, f)

    p_chart.render_to_file(
        result_folder_path + 'Compare_{0}_P_{1}.svg'.format(date.today().isoformat(), len(file_names)))
    r_chart.render_to_file(
        result_folder_path + 'Compare_{0}_R_{0}.svg'.format(date.today().isoformat(), len(file_names)))
    f_chart.render_to_file(
        result_folder_path + 'Compare_{0}_F_{0}.svg'.format(date.today().isoformat(), len(file_names)))
    return


def analysis(file_name):
    analysis_overall(file_name)
    analysis_acc(file_name)
    return


# analysis('2018-08-10')

compare_logs('2018-08-10')
