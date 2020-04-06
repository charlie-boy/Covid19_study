from bokeh.plotting import figure, output_file, show
from bokeh.layouts import layout, row, column
from bokeh.io import curdoc
import pandas as pd
from bokeh.models import ColumnDataSource, Select, HoverTool, Div, Legend, CheckboxGroup, FactorRange, VBar


state_info_url = 'https://covidtracking.com/api/v1/states/info.csv'
state_df = pd.read_csv(state_info_url)

states_fullname = list(state_df.name)
states_abbv = list(state_df.state)
state_name_dict = dict(zip(states_fullname,states_abbv))

## states population data"

population_data = pd.read_csv("Real_spread/population_data.csv")
state_population_dict = dict(zip(population_data.State,population_data.Pop))
total_us_population = sum(list(state_population_dict.values()))
############################

## states demography data"

demography_data = pd.read_csv("Real_spread/demography_data.csv", skiprows=2)
demography_age = list(demography_data.keys())[1:-2]
state_population_dict = dict(zip(demography_data.Location,population_data.Pop))
total_us_population = sum(list(state_population_dict.values()))
############################


daily_url = 'https://covidtracking.com/api/v1/states/daily.csv'
state = "Minnesota"
dataframe = pd.read_csv(daily_url)#("Real_spread/daily.csv")
gp = dataframe.groupby('state')
df = gp.get_group(state_name_dict[state])

date = df['date']
date = pd.to_datetime(date, format='%Y%m%d')
positive = df['positive']
#negative = df['negative']
recovered = df['recovered']
death = df['death']
positive_increase = df['positiveIncrease']
death_increase = df['deathIncrease']

source1 = ColumnDataSource(data={
    'x' : date,
    'y1' : positive,
    #'y2' : negative,
    'y3' : recovered,
    'y4' : death,
    'y5' : positive_increase,
    'y6' : death_increase
})

############################
#US Daily

us_daily_url = "https://covidtracking.com/api/us/daily.csv"
us_df = pd.read_csv(us_daily_url)
date_us = us_df['date']
date_us = pd.to_datetime(date_us, format='%Y%m%d')
positive_us = us_df['positive']*state_population_dict[state]/total_us_population
#negative_us = us_df['negative']*state_population_dict[state]/total_us_population
recovered_us = us_df['recovered']*state_population_dict[state]/total_us_population
death_us = us_df['death']*state_population_dict[state]/total_us_population
positive_increase_us = us_df['positiveIncrease']*state_population_dict[state]/total_us_population
death_increase_us = us_df['deathIncrease']*state_population_dict[state]/total_us_population

#############################

source2 = ColumnDataSource(data={
    'x' : date_us,
    'y1' : positive_us,
    #'y2' : negative_us,
    'y3' : recovered_us,
    'y4' : death_us,
    'y5' : positive_increase_us,
    'y6' : death_increase_us
})

output_file('index.html')
plot=figure(
    title='Covid-19 spread',
    x_axis_label = 'Days',
    y_axis_label = 'People',
    x_axis_type='datetime',
)
line_positive = plot.line('x','y1',source=source1, color='red', alpha=0.5,line_width=4)
#line_negative = plot.line('x','y2',source=source1, color='navy', alpha=0.5, legend='Negative',line_width=4)
#line_recovered = plot.line('x','y3',source=source1, color='green', alpha=0.5, legend='Recovered',line_width=4)
point_recovered = plot.circle('x','y3', source=source1, size=10, color="green", alpha=0.5)
line_death = plot.line('x','y4',source=source1, color='black', alpha=0.5,line_width=4)
point_positive_increase = plot.circle('x','y5', source=source1, size=10, color="navy", alpha=0.5)
point_death_increase = plot.circle('x','y6', source=source1, size=10, color="pink", alpha=0.5)

line_positive_us = plot.line('x','y1',source=source2, color='red', alpha=0.5,line_width=2)
#line_negative_us = plot.line('x','y2',source=source2, color='navy', alpha=0.5, legend='Negative',line_width=2)
#line_recovered_us = plot.line('x','y3',source=source2, color='green', alpha=0.5, legend='Recovered',line_width=2)
point_recovered_us = plot.circle('x','y3', source=source2, size=5, color="green", alpha=0.5)
line_death_us = plot.line('x','y4',source=source2, color='black', alpha=0.5,line_width=2)
point_positive_increase_us = plot.circle('x','y5', source=source2, size=5, color="navy", alpha=0.5)
point_death_increase_us = plot.circle('x','y6', source=source2, size=5, color="pink", alpha=0.5)

lines={0:(line_positive,line_positive_us), 1:(point_recovered,point_recovered_us), 2:(line_death,line_death_us),
       3:(point_positive_increase,point_positive_increase_us), 4:(point_death_increase,point_death_increase_us)}


legend = Legend(items=[
    ("positive"   , [line_positive, line_positive_us]),
    ("recovered" , [point_recovered, point_recovered_us]),
    ("death" , [line_death, line_death_us]),
    ("positive increase" , [point_positive_increase, point_positive_increase_us]),
    ("death increase" , [point_death_increase, point_death_increase_us]),

], location="center")

plot.add_layout(legend, 'right')

plot.add_tools(HoverTool(renderers=[line_positive, line_positive_us], tooltips=[('positive',"@y1{0,0}"),("Date", "@x{%F}")],formatters={'x': 'datetime'}))
plot.add_tools(HoverTool(renderers=[point_recovered, point_recovered_us], tooltips=[('recovered',"@y3{0,0}"),("Date", "@x{%F}")],formatters={'x': 'datetime'}))
plot.add_tools(HoverTool(renderers=[line_death, line_death_us], tooltips=[('death',"@y4{0,0}"),("Date", "@x{%F}")],formatters={'x': 'datetime'}))
plot.add_tools(HoverTool(renderers=[point_positive_increase, point_positive_increase_us], tooltips=[('positive_increase',"@y5{0,0}"),("Date", "@x{%F}")],formatters={'x': 'datetime'}))
plot.add_tools(HoverTool(renderers=[point_death_increase, point_death_increase_us], tooltips=[('death_increase',"@y6{0,0}"),("Date", "@x{%F}")],formatters={'x': 'datetime'}))


#source = ColumnDataSource(demography_data.loc[demography_data['Location'] == state])
source_bar = ColumnDataSource(data={
    'x' : demography_age,
    'y' : list(demography_data.loc[demography_data['Location'] == state].values[0][1:-2])
})
plot2=figure(
    title='Agewise distribution of the state',
    x_axis_label = 'Age of the Population',
    y_axis_label = 'Percentage of population',
    x_range=FactorRange(factors=source_bar.data['x']),
    plot_width=480, plot_height=400,
    y_range=(0, 1)
)
#plot2.vbar(x=demography_age, top=list(demography_data.loc[demography_data['Location'] == state].values[0][1:-2]), width=0.7)
glyph = VBar(x='x', top='y', bottom=0, width=.8, fill_color="#6599ed")
plot2.add_glyph(source_bar, glyph)

print(list(demography_data.loc[demography_data['Location'] == state].values[0][1:-2]))


div_head = Div(text="""<h2>US vs states covid-19 spread plots</h2>""", width=500, height=50)
div_explain = Div(text="""<h3>US plots(thinner lines and smaller dots) are normalized according to the population of the compared state</h3>""", width=300, height=50)
div_us_pop = Div(text="""<br><br><br>Total population of US: """+f"{total_us_population:,d}", width=300, height=50)
div_state_pop = Div(text="""<br>Total population of """+state+" : "+f"{state_population_dict[state]:,d}", width=300, height=50)
checkbox_group = CheckboxGroup(labels=["positive", "recovered", "death", "positive increase", "death increase"], active=[0,1,2,3,4])
select_state = Select(title="Select State", value="Minnesota", options=states_fullname) #list(list(gp.groups.keys())))

def callbackselect_state(attr, old, new):
    try:
        div_state_pop.text = """<br>Total population of """+select_state.value+": "+f"{state_population_dict[select_state.value]:,d}"
    except:
        div_state_pop.text = """<br>Total population of """ + select_state.value + ": Not Available"
    try:
        #plot2.vbar(x=demography_age, top=list(demography_data.loc[demography_data['Location'] == select_state.value].values[0][1:-2]), width=0.7)
        source_bar.data={
            'x': demography_age,
            'y': list(demography_data.loc[demography_data['Location'] == select_state.value].values[0][1:-2])
        }
        glyph = VBar(x='x', top='y', bottom=0, width=.8, fill_color="#6599ed")
        plot2.add_glyph(source_bar, glyph)
    except:
        #plot2.vbar(x=demography_age, top=[0,0,0,0,0,0], width=0.7)
        source_bar.data = {
            'x': demography_age,
            'y': [0,0,0,0,0,0]
        }
        glyph = VBar(x='x', top='y', bottom=0, width=.8, fill_color="#6599ed")
        plot2.add_glyph(source_bar, glyph)
    df = gp.get_group(state_name_dict[select_state.value])

    date = df['date']
    date = pd.to_datetime(date, format='%Y%m%d')
    positive = df['positive']
    negative = df['negative']
    recovered = df['recovered']
    death = df['death']
    positive_increase = df['positiveIncrease']
    death_increase = df['deathIncrease']

    source1.data={
        'x': date,
        'y1': positive,
        # 'y2' : negative,
        'y3': recovered,
        'y4': death,
        'y5' : positive_increase,
        'y6' : death_increase
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
select_state.on_change('value', callbackselect_state)

#show(plot)
text_details = column(checkbox_group, div_explain, div_us_pop, div_state_pop)
col = column(select_state,text_details)
body = row(col, plot, plot2)
layout = column(div_head,body)
curdoc().add_root(layout)