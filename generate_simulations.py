from bokeh.plotting import figure, output_file, show
from bokeh.layouts import layout, row, column
from bokeh.io import curdoc
import pandas as pd
from bokeh.models import ColumnDataSource, Select, Button, CheckboxGroup, Div

df = pd.read_csv('Simulations/1_percentile/NoQuar0.csv', skiprows=1)
day = df['Day']
susceptible = df['Susceptible']
infected = df['Infected']
recovered = df['Recovered']
dead = df['Dead']

source1 = ColumnDataSource(data={
    'x' : day,
    'y1' : infected,
    'y2' : susceptible,
    'y3' : recovered,
    'y4' : dead
})

source2 = ColumnDataSource(data={
    'x' : day,
    'y1' : infected,
    'y2' : susceptible,
    'y3' : recovered,
    'y4' : dead
})

output_file('index.html')
plot=figure(
    title='Covid-19 SIR model',
    x_axis_label = 'Days',
    y_axis_label = 'People',
    x_range=(0, 60),
    y_range=(0, 100010)
)
lineInfected1 = plot.line('x','y1',source=source1, color='red', alpha=0.5, legend='Infected',line_width=2)
lineSusceptible1 = plot.line('x','y2',source=source1, color='navy', alpha=0.5, legend='Susceptible',line_width=2)
lineRecovered1 = plot.line('x','y3',source=source1, color='green', alpha=0.5, legend='Recovered',line_width=2)
lineDead1 = plot.line('x','y4',source=source1, color='black', alpha=0.5, legend='Dead',line_width=2)

lineInfected2 = plot.line('x','y1',source=source2, color='red', alpha=0.5, legend='Infected',line_width=2)
lineSusceptible2 = plot.line('x','y2',source=source2, color='navy', alpha=0.5, legend='Susceptible',line_width=2)
lineRecovered2 = plot.line('x','y3',source=source2, color='green', alpha=0.5, legend='Recovered',line_width=2)
lineDead2 = plot.line('x','y4',source=source2, color='black', alpha=0.5, legend='Dead',line_width=2)

lines={0:(lineInfected1,lineInfected2), 1:(lineSusceptible1,lineSusceptible2), 2:(lineRecovered1,lineRecovered2), 3:(lineDead1,lineDead2)}

#plot.line('x', 'y', source=source ,legend='Infected',line_width=2)

quarantine_percentile = {"1%": "1_percentile", "2%": "2_percentile", "5%": "5_percentile", "10%": "10_percentile"}
quarantine_policy = {'No Quarantine': 'No', 'Random Quarantine': 'Rand','HyperSocial Qurarantine': 'Hyper'}

q_policy1 = 'No'
q_percentile1 = '1_percentile'
q_policy2 = 'No'
q_percentile2 = '1_percentile'


checkbox_group = CheckboxGroup(labels=["Infected", "Susceptible", "Recovered", "Dead"], active=[0,1,2,3])

para = Div(text="""<h2>Compare 2 models:</h2>""", width=200, height=20)

para1 = Div(text="""<h3>Model 1</h3>""", width=100, height=30)
select1a = Select(title="Quarantine policy", value="No Quarantine", options=list(quarantine_policy.keys()))
select1b = Select(title="Quarantine percentile", value="1%", options=list(quarantine_percentile.keys()))
button1 = Button(label='PLot model 1')

para2 = Div(text="""<h3>Model 2</h3>""", width=100, height=30)
select2a = Select(title="Quarantine policy", value="No Quarantine", options=list(quarantine_policy.keys()))
select2b = Select(title="Quarantine percentile", value="1%", options=list(quarantine_percentile.keys()))
button2 = Button(label='PLot model 2')

def callbackselect1a(attr, old, new):
    global q_policy1
    q_policy1 = quarantine_policy[new]

def callbackselect1b(attr, old, new):
    global q_percentile1
    q_percentile1 = quarantine_percentile[new]

def callbackselect2a(attr, old, new):
    global q_policy2
    q_policy2 = quarantine_policy[new]

def callbackselect2b(attr, old, new):
    global q_percentile2
    q_percentile2 = quarantine_percentile[new]

def update1():
    df = pd.read_csv('Simulations/'+q_percentile1+'/'+q_policy1+'Quar0.csv', skiprows=1)
    day = df['Day']
    susceptible = df['Susceptible']
    infected = df['Infected']
    recovered = df['Recovered']
    dead = df['Dead']
    source1.data={
        'x' : day,
        'y1' : infected,
        'y2' : susceptible,
        'y3' : recovered,
        'y4' : dead
    }

def update2():
    df = pd.read_csv('Simulations/'+q_percentile2+'/'+q_policy2+'Quar0.csv', skiprows=1)
    day = df['Day']
    susceptible = df['Susceptible']
    infected = df['Infected']
    recovered = df['Recovered']
    dead = df['Dead']
    source2.data={
        'x' : day,
        'y1' : infected,
        'y2' : susceptible,
        'y3' : recovered,
        'y4' : dead
    }

def update_plots(new):
    switch = checkbox_group.active
    for x in range(0, len(lines)):
        if x in switch:
            lines[x][0].visible = True
            lines[x][1].visible = True
        else:
            lines[x][0].visible = False
            lines[x][1].visible = False

checkbox_group.on_click(update_plots)

select1a.on_change('value', callbackselect1a)
select1b.on_change('value', callbackselect1b)
button1.on_click(update1)

select2a.on_change('value', callbackselect2a)
select2b.on_change('value', callbackselect2b)
button2.on_click(update2)

col1 = column(checkbox_group, para, para1, select1a, select1b, button1)
col2 = column(col1, para2, select2a, select2b, button2)
layout = row(col2, plot)
curdoc().add_root(layout)