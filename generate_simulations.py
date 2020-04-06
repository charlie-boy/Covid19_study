from bokeh.plotting import figure, output_file, show
from bokeh.layouts import layout, row, column
from bokeh.io import curdoc
import pandas as pd
from bokeh.models import ColumnDataSource, Select, Button, CheckboxGroup, Div
from sklearn.metrics import r2_score

###################################### US real data ###########################################

us_daily_url = "https://covidtracking.com/api/us/daily.csv"
us_df = pd.read_csv(us_daily_url)
date_us = us_df['date']
date_us = pd.to_datetime(date_us, format='%Y%m%d')
infected_us = us_df['positive']#*state_population_dict[state]/total_us_population
#negative_us = us_df['negative']#*state_population_dict[state]/total_us_population
recovered_us = us_df['recovered']#*state_population_dict[state]/total_us_population
dead_us = us_df['death']#*state_population_dict[state]/total_us_population
daily_infected_us = us_df['positiveIncrease']#*state_population_dict[state]/total_us_population
daily_dead_us = us_df['deathIncrease']#*state_population_dict[state]/total_us_population

################################################################################################

df = pd.read_csv('simulations/start_17/no_quarantine/No_Quarantine_Mean.csv')#, skiprows=1)
day = df['Day']
susceptible = df['Susceptible']
infected = df['Infected']
recovered = df['Recovered']
dead = df['Dead']
hospitalized = df['Hospitalized']
daily_infected = df['Daily Infected']
daily_dead = df['Daily Dead']

source_1 = ColumnDataSource(data={
    'x' : day,
    'y1' : infected,
    'y2' : susceptible,
    'y3' : recovered,
    'y4' : dead,
    'y5' : hospitalized,
    'y6' : daily_infected,
    'y7' : daily_dead
})

source_2 = ColumnDataSource(data={
    'x' : day,
    'y1' : infected,
    'y2' : susceptible,
    'y3' : recovered,
    'y4' : dead,
    'y5' : hospitalized,
    'y6' : daily_infected,
    'y7' : daily_dead
})

output_file('index.html')
plot=figure(
    title='Covid-19 SIR model',
    x_axis_label = 'Days',
    y_axis_label = 'People',
    x_range=(0, 60),
    y_range=(0, 100010)
)
line_Infected_1 = plot.line('x','y1',source=source_1, color='red', alpha=0.5, legend='Infected',line_width=3)
line_Susceptible_1 = plot.line('x','y2',source=source_1, color='navy', alpha=0.5, legend='Susceptible',line_width=3)
lineRecovered_1 = plot.line('x','y3',source=source_1, color='green', alpha=0.5, legend='Recovered',line_width=3)
line_Dead_1 = plot.line('x','y4',source=source_1, color='black', alpha=0.5, legend='Dead',line_width=3)
line_Hospitalized_1 = plot.line('x','y2',source=source_1, color='pink', alpha=0.5, legend='Hospitalized',line_width=3)
line_Daily_Infected_1 = plot.line('x','y3',source=source_1, color='yellow', alpha=0.5, legend='Daily Infected',line_width=3)
line_Daily_Dead_1 = plot.line('x','y4',source=source_1, color='orange', alpha=0.5, legend='Daily Dead',line_width=3)

line_Infected_2 = plot.line('x','y1',source=source_2, color='red', alpha=0.5, legend='Infected',line_width=2)
line_Susceptible_2 = plot.line('x','y2',source=source_2, color='navy', alpha=0.5, legend='Susceptible',line_width=2)
lineRecovered_2 = plot.line('x','y3',source=source_2, color='green', alpha=0.5, legend='Recovered',line_width=2)
line_Dead_2 = plot.line('x','y4',source=source_2, color='black', alpha=0.5, legend='Dead',line_width=2)
line_Hospitalized_2 = plot.line('x','y2',source=source_2, color='pink', alpha=0.5, legend='Hospitalized',line_width=2)
line_Daily_Infected_2 = plot.line('x','y3',source=source_2, color='yellow', alpha=0.5, legend='Daily Infected',line_width=2)
line_Daily_Dead_2 = plot.line('x','y4',source=source_2, color='orange', alpha=0.5, legend='Daily Dead',line_width=2)

lines={0:(line_Infected_1, line_Infected_2), 1:(line_Susceptible_1, line_Susceptible_2),
       2:(lineRecovered_1, lineRecovered_2), 3:(line_Dead_1, line_Dead_2),
       4:(line_Hospitalized_1, line_Hospitalized_2), 5:(line_Daily_Infected_1, line_Daily_Infected_2),
       6:(line_Daily_Dead_1, line_Daily_Dead_2)}

# Dimensions
quarantine_policy = {'No Quarantine': 'no_quarantine', 'Quarantine':'quarantine'}#'Random Quarantine': 'Rand','HyperSocial Qurarantine': 'Hyper'}
quarantine_object = {'People': 'People', 'Location':'Location', 'Both':'Both'}
quarantine_object_type = {'Hypersocial':'Hyper', 'Random':'Random'}
quarantine_percentile = {'1%': '1', '2%': '2', '5%': '5', '10%': '10'}
quarantine_start = {'17':'start_17'}
quarantine_period = {'14':'14 Days','28':'28 Days','42':'42 Days'}


head = Div(text="""<h1>Compare models to analyze spread of Covid-19</h1>""", width=1000, height=40)

checkbox_div = Div(text="""<h3>Select plot lines you want to see</h3>""", width=500, height=40)
checkbox_group = CheckboxGroup(labels=["Infected", "Susceptible", "Recovered", "Dead", "Hospitalized", "Daily_Infected", "Daily_Dead"], active=list(range(7)))

##################################### R square values #################################################
rev_infected_us_val = infected_us.values[::-1]
start_i = 0
for i in range(len(infected.values)-1):
    if rev_infected_us_val[0] >= infected.values[i] and rev_infected_us_val[0] <= infected.values[i+1]:
        start_i = i
infected_r2 = r2_score(infected_us.values[::-1], infected.values[start_i:len(infected_us)+start_i])
dead_r2 = r2_score(dead_us.values[::-1], dead.values[start_i:len(dead_us)+start_i])
r_square_div = Div(text="""<br><h3>R-Square value between current US stats and policies(Model 1) over generated data</h3><br>Infected r2 score = """
                        +str(infected_r2)+"<br>Dead r2 score = "+str(dead_r2), width=500, height=200)
#########################################################################################################

## Model 1 initial model
div_model_1 = Div(text="""<h3>Model 1</h3>""", width=100, height=30)
select_policy_model_1 = Select(title="Quarantine policy", value="No Quarantine", options=list(quarantine_policy.keys()))
select_object_model_1 = Select(title="Quarantine object", value="People", options=[])#list(quarantine_object.keys()))
select_object_type_model_1 = Select(title="Quarantine object type", value="Hypersocial", options=[])#list(quarantine_object_type.keys()))
select_percentile_model_1 = Select(title="Quarantine percentile", value="1%", options=[])#list(quarantine_percentile.keys()))
select_start_model_1 = Select(title="Quarantine start day", value="17", options=[])
select_period_model_1 = Select(title="Quarantine period", value="14", options=[])
button_model_1 = Button(label='Plot model 1')

## Model 2 initial model
div_model_2 = Div(text="""<h3>Model 2</h3>""", width=100, height=30)
select_policy_model_2 = Select(title="Quarantine policy", value="No Quarantine", options=list(quarantine_policy.keys()))
select_object_model_2 = Select(title="Quarantine object", value="People", options=[])#list(quarantine_object.keys()))
select_object_type_model_2 = Select(title="Quarantine object type", value="Hypersocial", options=[])#list(quarantine_object_type.keys()))
select_percentile_model_2 = Select(title="Quarantine percentile", value="1%", options=[])#list(quarantine_percentile.keys()))
select_start_model_2 = Select(title="Quarantine start day", value="17", options=[])
select_period_model_2 = Select(title="Quarantine period", value="14", options=[])
button_model_2 = Button(label='Plot model 2')

##############################
# Model 1 callback functions #
##############################

def callback_select_policy_model_1(attr, old, new):
    #global q_policy1
    #q_policy1 = quarantine_policy[new]
    if select_policy_model_1.value == 'No Quarantine':
        select_object_model_1.options = []
        select_object_type_model_1.options = []
        select_percentile_model_1.options = []
        select_start_model_1.options = []
        select_period_model_1.options = []
    else:
        select_object_model_1.options = list(quarantine_object.keys())
        select_object_type_model_1.options = list(quarantine_object_type.keys())
        select_percentile_model_1.options = list(quarantine_percentile.keys())
        select_start_model_1.options = list(quarantine_start.keys())
        select_period_model_1.options = list(quarantine_period.keys())

def callback_select_object_model_1(attr, old, new):
    pass

def callback_select_object_type_model_1(attr, old, new):
    pass

def callback_select_percentile_model_1(attr, old, new):
    pass

def callback_select_start_model_1(attr, old, new):
    pass

def callback_select_period_model_1(attr, old, new):
    pass

def update_model_1():
    if select_policy_model_1.value == 'No Quarantine':
        df = pd.read_csv('simulations/start_17/no_quarantine/No_Quarantine_Mean.csv')
    else:
        df = pd.read_csv('simulations/'+quarantine_start[select_start_model_1.value] + '/' \
                                    +quarantine_policy[select_policy_model_1.value] + '/' \
                                    +quarantine_object[select_object_model_1.value] + '/' \
                                    +quarantine_period[select_period_model_1.value] + '/' \
                                    +quarantine_percentile[select_percentile_model_1.value] + '_ ' \
                                    +quarantine_object_type[select_object_type_model_1.value] + ' Quarantine_Mean.csv')
    day = df['Day']
    susceptible = df['Susceptible']
    infected = df['Infected']
    recovered = df['Recovered']
    dead = df['Dead']
    hospitalized = df['Hospitalized']
    daily_infected = df['Daily Infected']
    daily_dead = df['Daily Dead']

    source_1.data={
        'x' : day,
        'y1' : infected,
        'y2' : susceptible,
        'y3' : recovered,
        'y4' : dead,
        'y5' : hospitalized,
        'y6' : daily_infected,
        'y7' : daily_dead
    }

    rev_infected_us_val = infected_us.values[::-1]
    start_i = 0
    for i in range(len(infected.values) - 1):
        if rev_infected_us_val[0] >= infected.values[i] and rev_infected_us_val[0] <= infected.values[i + 1]:
            start_i = i
    infected_r2 = r2_score(infected_us.values[::-1], infected.values[start_i:len(infected_us) + start_i])
    dead_r2 = r2_score(dead_us.values[::-1], dead.values[start_i:len(dead_us) + start_i])
    r_square_div.text="""<br><h3>R-Square value between current US stats and policies(Model 1) over generated data</h3><br>Infected r2 score = """\
                      + str(infected_r2) + "<br>Dead r2 score = " + str(dead_r2)


##############################
# Model 2 callback functions #
##############################

def callback_select_policy_model_2(attr, old, new):
    # global q_policy2
    # q_policy2 = quarantine_policy[new]
    if select_policy_model_2.value == 'No Quarantine':
        select_object_model_2.options = []
        select_object_type_model_2.options = []
        select_percentile_model_2.options = []
        select_start_model_2.options = []
        select_period_model_2.options = []
    else:
        select_object_model_2.options = list(quarantine_object.keys())
        select_object_type_model_2.options = list(quarantine_object_type.keys())
        select_percentile_model_2.options = list(quarantine_percentile.keys())
        select_start_model_2.options = list(quarantine_start.keys())
        select_period_model_2.options = list(quarantine_period.keys())


def callback_select_object_model_2(attr, old, new):
    pass


def callback_select_object_type_model_2(attr, old, new):
    pass


def callback_select_percentile_model_2(attr, old, new):
    pass


def callback_select_start_model_2(attr, old, new):
    pass


def callback_select_period_model_2(attr, old, new):
    pass


def update_model_2():
    if select_policy_model_2.value == 'No Quarantine':
        df = pd.read_csv('simulations/start_17/no_quarantine/No_Quarantine_Mean.csv')
    else:
        df = pd.read_csv('simulations/' + quarantine_start[select_start_model_2.value] + '/' \
                     +quarantine_policy[select_policy_model_2.value] + '/' \
                     +quarantine_object[select_object_model_2.value] + '/' \
                     +quarantine_period[select_period_model_2.value] + '/' \
                     +quarantine_percentile[select_percentile_model_2.value] + '_ ' \
                     +quarantine_object_type[select_object_type_model_2.value] + ' Quarantine_Mean.csv')
    day = df['Day']
    susceptible = df['Susceptible']
    infected = df['Infected']
    recovered = df['Recovered']
    dead = df['Dead']
    hospitalized = df['Hospitalized']
    daily_infected = df['Daily Infected']
    daily_dead = df['Daily Dead']

    source_2.data = {
        'x': day,
        'y1': infected,
        'y2': susceptible,
        'y3': recovered,
        'y4': dead,
        'y5': hospitalized,
        'y6': daily_infected,
        'y7': daily_dead
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

## Model 1 selections
select_policy_model_1.on_change('value', callback_select_policy_model_1)
select_object_model_1.on_change('value', callback_select_object_model_1)
select_object_type_model_1.on_change('value', callback_select_object_type_model_1)
select_percentile_model_1.on_change('value', callback_select_percentile_model_1)
select_start_model_1.on_change('value', callback_select_start_model_1)
select_period_model_1.on_change('value', callback_select_period_model_1)
button_model_1.on_click(update_model_1)

## Model 2 selections
select_policy_model_2.on_change('value', callback_select_policy_model_2)
select_object_model_2.on_change('value', callback_select_object_model_2)
select_object_type_model_2.on_change('value', callback_select_object_type_model_2)
select_percentile_model_2.on_change('value', callback_select_percentile_model_2)
select_start_model_2.on_change('value', callback_select_start_model_2)
select_period_model_2.on_change('value', callback_select_period_model_2)
button_model_2.on_click(update_model_2)

#col1 = column(checkbox_group, para, para1, select1a, select1b, button1)
#col2 = column(col1, para2, select2a, select2b, button2)
#layout = row(col2, plot)
left = column(div_model_1, select_policy_model_1, select_object_model_1, select_object_type_model_1,
              select_percentile_model_1, select_start_model_1, select_period_model_1, button_model_1, r_square_div)
right = column(div_model_2, select_policy_model_2, select_object_model_2, select_object_type_model_2,
              select_percentile_model_2, select_start_model_2, select_period_model_2, button_model_2)
center = column(checkbox_div, checkbox_group, plot)
body = row(left, center, right)
layout = column(head, body)

curdoc().add_root(layout)