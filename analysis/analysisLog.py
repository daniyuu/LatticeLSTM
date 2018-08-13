import pygal


def analysis_acc(file_name):
    logFile = open('./log/{0}.txt'.format(file_name), 'r')

    index = 0
    x = []
    y = []
    for line in logFile.readlines():
        if "Instance" in line:
            index += 1
            acc = line.split('=')[1].split('\n')[0]
            x.append(index)
            y.append(float(acc))

    line_chart = pygal.Line()
    line_chart.title = "Lattice Acc"
    # line_chart.x_labels = x
    line_chart.add("Acc", y)
    line_chart.render_to_file('{0}.svg'.format(file_name))
    return
