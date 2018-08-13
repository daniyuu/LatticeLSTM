import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='daniyuu', api_key='6iHnQZtDeTu9vNgIbipd')

logFile = open('./log/2018-08-10.txt', 'r')

index = 0
x = []
y = []
for line in logFile.readlines():
    if "Instance" in line:
        index += 1
        acc = line.split('=')[1].split('\n')[0]
        x.append(index)
        y.append(acc)
        # print(acc)
        # print(line)
print(x)
print(y)
print(len(x))
print(len(y))

trace = go.Scatter(x=x, y=y, mode='line', name='acc')

data = [trace]
py.plot(data, filename="acc line chat", auto_open=True)
