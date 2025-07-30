# Imports libraries
import pandas as pd  # used to import the dataset

from bokeh.events import ButtonClick
from bokeh.io import curdoc
from bokeh.layouts import layout, gridplot, row, column
from bokeh.models import (
    ColumnDataSource, CategoricalColorMapper, CheckboxButtonGroup, CDSView, BooleanFilter, Div,
    BoxSelectTool, LassoSelectTool, Panel, Tabs, Button, RadioButtonGroup
)
from bokeh.plotting import figure
import urllib.request

# Load in database with pandas
dataframe = pd.read_csv("pokedex_(Update_05.20).csv")
# Load in the database with bokeh
datasetCDS = ColumnDataSource(data=dataframe)

# Adds all stats to a total for the axis
total = dataframe["hp"] + dataframe["attack"] + dataframe["sp_attack"] + dataframe["defense"] + dataframe[
    "sp_defense"] + dataframe["speed"]

# Adding total as a new column in datasetCDS
datasetCDS.data["total"] = total

# Stores Pokédex number as "001" instead of "1" in formPN
dataframe['formPN'] = dataframe['pokedex_number'].apply(lambda x: '{0:0>3}'.format(x))
datasetCDS.data["formPN"] = dataframe['formPN']
datasetCDS.data["gen"] = dataframe['name']
for x in range(len(datasetCDS.data["index"])):
    datasetCDS.data["gen"][x] = str(datasetCDS.data["generation"][x])

# Creates the url to the images
def image(url):
    request = urllib.request.Request(url)
    request.get_method = lambda: 'HEAD'
    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False

# uncomment "if image(url):" and tab line below it to run the url checker to make sure every pokemon has an image. It
# will take a lot longer to load.
urlvar = [""] * len(datasetCDS.data["index"])
datasetCDS.data["url"] = urlvar
for x in range(len(datasetCDS.data["index"])):
    datasetCDS.data['url'][x] = 'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/' + \
                                datasetCDS.data['formPN'][x] + '.png'

    if datasetCDS.data['pokedex_number'][x] == datasetCDS.data['pokedex_number'][x - 1]:
        url = 'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/' + datasetCDS.data['formPN'][x] + '_f2.png'
        # if image(url):
        datasetCDS.data['url'][x] = url

    if datasetCDS.data['pokedex_number'][x] == datasetCDS.data['pokedex_number'][x - 2]:
        url = 'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/' + datasetCDS.data['formPN'][x] + '_f3.png'
        # if image(url):
        datasetCDS.data['url'][x] = url

    if datasetCDS.data['pokedex_number'][x] == datasetCDS.data['pokedex_number'][x - 3]:
        # url = 'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/' + datasetCDS.data['formPN'][x] + '_f4.png'
        # if image(url):
        datasetCDS.data['url'][x] = url

# Reads the data from each stat from the database and scales them to a coefficient
sizeCoeff = 2
datasetCDS.data['hpSize'] = dataframe['hp'] / sizeCoeff
datasetCDS.data['attackSize'] = dataframe['attack'] / sizeCoeff
datasetCDS.data['sp_attackSize'] = dataframe['sp_attack'] / sizeCoeff
datasetCDS.data['defenseSize'] = dataframe['defense'] / sizeCoeff
datasetCDS.data['sp_defenseSize'] = dataframe['sp_defense'] / sizeCoeff
datasetCDS.data['speedSize'] = dataframe['speed'] / sizeCoeff

# HTML and CSS to the hovering function
TOOLTIPS = """
    <div style="width: 150px;">
        <div style="display: grid;">
            <span style="font-size: 17px; font-weight: bold;">@name</span></div>
            <div style="display: grid;"><span style="font-size: 14px; font-weight: bold;">Pokédex: @pokedex_number</span></div>
        </div style="display: grid;">

        <div style="display: grid; margin-bottom: 2%;">
            <img src="@url" height="100%" alt="@name" width="100%"
                style=" float:right; margin: 0px;"
                border="1">
            </img>
        </div>
        <div id="" style="position: relative; text-align: center; font-size: 10px; vertical-align: bottom; ">
        
          <div style="display: inline-block;vertical-align: bottom;">@hp         <div 
          style="width:30px;height:@hpSize;        border:1px solid #000;background-color: lightblue;"></div>HP</div> 
          <div style="display: inline-block;vertical-align: bottom;">@attack     <div 
          style="width:30px;height:@attackSize;    border:1px solid #000;background-color: 
          lightblue;"></div>Atk</div> <div style="display: inline-block;vertical-align: bottom;">@sp_attack  <div 
          style="width:30px;height:@sp_attackSize; border:1px solid #000;background-color: 
          lightblue;"></div>Sp.Atk</div> <div style="display: inline-block;vertical-align: bottom;">@defense    <div 
          style="width:30px;height:@defenseSize;   border:1px solid #000;background-color: 
          lightblue;"></div>Def</div> <div style="display: inline-block;vertical-align: bottom;">@sp_defense <div 
          style="width:30px;height:@sp_defenseSize;border:1px solid #000;background-color: 
          lightblue;"></div>Sp.Def</div> <div style="display: inline-block;vertical-align: bottom;">@speed      <div 
          style="width:30px;height:@speedSize;     border:1px solid #000;background-color: lightblue;"></div>Spe</div> 

        </div>
    </div>
"""
# The existing types and their correlated color and maps them together
types = ["Fairy", "Steel", "Dark", "Dragon", "Ghost", "Rock", "Bug", "Psychic",
         "Flying", "Ground", "Poison", "Fighting", "Ice", "Grass", "Electric",
         "Water", "Fire", "Normal"]
colors = ["#EAA3DC", "#B8B8D0", "#765747", "#7636F6", "#745797", "#BF9F38", "#A5B82B",
          "#FF4980", "#AC8FEF", "#E9C26E", "#AF399D", "#D51C0D", "#7FDADA", "#55CA59",
          "#FFCE2E", "#5591F0", "#FF7919", "#A9A879"]
color_mapper = CategoricalColorMapper(
    palette=colors,
    factors=types)

# color column in the dataset return a hexcode
def color(type):
    for j in range(len(types)):
        if type == types[j]:
            return colors[j]

# interaction options with the plots
options = dict(tools="pan,wheel_zoom,lasso_select,box_select,reset")

# the first view when opening the page (Bokeh 3.x+)
from bokeh.models import BooleanFilter
view = CDSView(filter=BooleanFilter([True] * len(datasetCDS.data["index"])))

# Code for the scatter plot, labels and tabs
php = figure(x_axis_label="Total", y_axis_label="HP", tooltips=TOOLTIPS, active_scroll="wheel_zoom", **options)
php.scatter(x="total", y="hp", source=datasetCDS, alpha=0.3, hover_alpha=1,
           color={'field': 'type_1', 'transform': color_mapper}, size=5, name="circle", view=view)
tab1 = ("HP", php)

patt = figure(x_axis_label="Total", y_axis_label="Attack", tooltips=TOOLTIPS, active_scroll="wheel_zoom", **options)
patt.scatter(x="total", y="attack", source=datasetCDS, alpha=0.3, hover_alpha=1,
            color={'field': 'type_1', 'transform': color_mapper}, size=5, name="circle", view=view)
tab2 = ("Attack", patt)

pspa = figure(x_axis_label="Total", y_axis_label="Special Attack", tooltips=TOOLTIPS, active_scroll="wheel_zoom",
              **options)
pspa.scatter(x="total", y="sp_attack", source=datasetCDS, alpha=0.3, hover_alpha=1,
            color={'field': 'type_1', 'transform': color_mapper}, size=5, name="circle", view=view)
tab3 = ("Special Attack", pspa)

pdef = figure(x_axis_label="Total", y_axis_label="Defense", tooltips=TOOLTIPS, active_scroll="wheel_zoom", **options)
pdef.scatter(x="total", y="defense", source=datasetCDS, alpha=0.3, hover_alpha=1,
            color={'field': 'type_1', 'transform': color_mapper}, size=5, name="circle", view=view)
tab4 = ("Defense", pdef)

pspd = figure(x_axis_label="Total", y_axis_label="Special Defense", tooltips=TOOLTIPS, active_scroll="wheel_zoom",
              **options)
pspd.scatter(x="total", y="sp_defense", source=datasetCDS, alpha=0.3, hover_alpha=1,
            color={'field': 'type_1', 'transform': color_mapper}, size=5, name="circle", view=view)
tab5 = ("Special Defense", pspd)

pspe = figure(x_axis_label="Total", y_axis_label="Speed", tooltips=TOOLTIPS, active_scroll="wheel_zoom", **options)
pspe.scatter(x="total", y="speed", source=datasetCDS, alpha=0.3, hover_alpha=1,
            color={'field': 'type_1', 'transform': color_mapper}, size=5, name="circle", view=view)
tab6 = ("Speed", pspe)

tabs = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6])

# Code for the parallel coordinates figure
lineFig = figure(tooltips=TOOLTIPS, active_scroll="wheel_zoom", **options)

# parallel coordinates plot with color
mult = [[0] * 6 for _ in range(len(datasetCDS.data["index"]))]
colorRange = [""] * len(datasetCDS.data["index"])

for i in range(len(datasetCDS.data["index"])):
    mult[i] = [datasetCDS.data["hp"][i],
               datasetCDS.data["attack"][i],
               datasetCDS.data["sp_attack"][i],
               datasetCDS.data["defense"][i],
               datasetCDS.data["sp_defense"][i],
               datasetCDS.data["speed"][i]]

    colorRange[i] = color(datasetCDS.data['type_1'][i])

# creating more dataframes in the dataset for the multiline
dataframe['names'] = [["1", "2", "3", "4", "5", "6"]] * len(datasetCDS.data["index"])
datasetCDS.data['names'] = dataframe['names']

dataframe['mult'] = mult
datasetCDS.data['mult'] = dataframe['mult']

datasetCDS.data['color'] = colorRange

# adding all the lines to the figure
lineFig.multi_line("names", "mult", source=datasetCDS, color="color", alpha=0.3, hover_alpha=1, view=view,
                   name="circle")

# show the plots in a grid pattern
gp = gridplot([[tabs, lineFig]], toolbar_location="below")

# array to see which gen is active
genList = [0] * 8

# functions to change the array on button press
def gen1(in_active):
    genList[0] = 1 if in_active else 0
def gen2(in_active):
    genList[1] = 2 if in_active else 0
def gen3(in_active):
    genList[2] = 3 if in_active else 0
def gen4(in_active):
    genList[3] = 4 if in_active else 0
def gen5(in_active):
    genList[4] = 5 if in_active else 0
def gen6(in_active):
    genList[5] = 6 if in_active else 0
def gen7(in_active):
    genList[6] = 7 if in_active else 0
def gen8(in_active):
    genList[7] = 8 if in_active else 0

# array for the types
typeList = [""] * 18

# functions to change the array on button press
def Fairy(in_active):    typeList[0] = "Fairy" if in_active else ""
def Steel(in_active):    typeList[1] = "Steel" if in_active else ""
def Dark(in_active):     typeList[2] = "Dark" if in_active else ""
def Dragon(in_active):   typeList[3] = "Dragon" if in_active else ""
def Ghost(in_active):    typeList[4] = "Ghost" if in_active else ""
def Rock(in_active):     typeList[5] = "Rock" if in_active else ""
def Bug(in_active):      typeList[6] = "Bug" if in_active else ""
def Psychic(in_active):  typeList[7] = "Psychic" if in_active else ""
def Flying(in_active):   typeList[8] = "Flying" if in_active else ""
def Ground(in_active):   typeList[9] = "Ground" if in_active else ""
def Poison(in_active):   typeList[10] = "Poison" if in_active else ""
def Fighting(in_active): typeList[11] = "Fighting" if in_active else ""
def Ice(in_active):      typeList[12] = "Ice" if in_active else ""
def Grass(in_active):    typeList[13] = "Grass" if in_active else ""
def Electric(in_active): typeList[14] = "Electric" if in_active else ""
def Water(in_active):    typeList[15] = "Water" if in_active else ""
def Fire(in_active):     typeList[16] = "Fire" if in_active else ""
def Normal(in_active):   typeList[17] = "Normal" if in_active else ""

statusList = [""] * 4
def isNormal(in_active): statusList[0] = "Normal" if in_active else ""
def isSub(in_active):    statusList[1] = "Sub Legendary" if in_active else ""
def isLegend(in_active): statusList[2] = "Legendary" if in_active else ""
def isMyth(in_active):   statusList[3] = "Mythical" if in_active else ""

gen_list = [gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8]

booleans = [False] * len(datasetCDS.data["index"])

# on button click run this
def generation(attr, old, new):
    last_clicked_ID = list(set(old) ^ set(new))[0]
    last_clicked_button_stuff = gen_list[last_clicked_ID]
    in_active = last_clicked_ID in new
    last_clicked_button_stuff(in_active)

    for i in range(len(datasetCDS.data["index"])):
        if datasetCDS.data['generation'][i] in genList and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and \
                datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        elif genList == [0] * 8 and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and \
                datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        elif datasetCDS.data['generation'][i] in genList and typeList == [""] * 18 and datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        elif datasetCDS.data['generation'][i] in genList and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and statusList == [""] * 4:
            booleans[i] = True
        elif genList == [0] * 8 and typeList == [""] * 18 and datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        elif genList == [0] * 8 and (datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and statusList == [""] * 4:
            booleans[i] = True
        elif datasetCDS.data['generation'][i] in genList and typeList == [""] * 18 and statusList == [""] * 4:
            booleans[i] = True
        else:
            booleans[i] = False

    new_view = CDSView(filter=BooleanFilter(booleans))
    php.select(name='circle')[0].view = new_view
    patt.select(name='circle')[0].view = new_view
    pspa.select(name='circle')[0].view = new_view
    pdef.select(name='circle')[0].view = new_view
    pspd.select(name='circle')[0].view = new_view
    pspe.select(name='circle')[0].view = new_view
    lineFig.select(name='circle')[0].view = new_view

GENS = ["1", "2", "3", "4", "5", "6", "7", "8"]
gens = CheckboxButtonGroup(labels=GENS, active=[])
gens.on_change('active', generation)

type_list = [Fairy, Steel, Dark, Dragon, Ghost, Rock, Bug, Psychic, Flying, Ground, Poison, Fighting, Ice, Grass,
             Electric, Water, Fire, Normal]

def typing(attr, old, new):
    last_clicked_ID = list(set(old) ^ set(new))[0]
    last_clicked_button_stuff = type_list[last_clicked_ID]
    in_active = last_clicked_ID in new
    last_clicked_button_stuff(in_active)

    for i in range(len(datasetCDS.data["index"])):
        if datasetCDS.data['generation'][i] in genList and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and \
                datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        elif genList == [0] * 8 and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and \
                datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        elif datasetCDS.data['generation'][i] in genList and typeList == [""] * 18 and datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        elif datasetCDS.data['generation'][i] in genList and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and statusList == [""] * 4:
            booleans[i] = True
        elif genList == [0] * 8 and typeList == [""] * 18 and datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        elif genList == [0] * 8 and (datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and statusList == [""] * 4:
            booleans[i] = True
        elif datasetCDS.data['generation'][i] in genList and typeList == [""] * 18 and statusList == [""] * 4:
            booleans[i] = True
        else:
            booleans[i] = False

    new_view = CDSView(filter=BooleanFilter(booleans))
    php.select(name='circle')[0].view = new_view
    patt.select(name='circle')[0].view = new_view
    pspa.select(name='circle')[0].view = new_view
    pdef.select(name='circle')[0].view = new_view
    pspd.select(name='circle')[0].view = new_view
    pspe.select(name='circle')[0].view = new_view
    lineFig.select(name='circle')[0].view = new_view

TYPES = ["Fairy", "Steel", "Dark", "Dragon", "Ghost", "Rock", "Bug", "Psychic",
         "Flying", "Ground", "Poison", "Fighting", "Ice", "Grass", "Electric",
         "Water", "Fire", "Normal"]
types = CheckboxButtonGroup(labels=TYPES, active=[])
types.on_change('active', typing)

status_list = [isNormal, isSub, isLegend, isMyth]

def whatSatus(attr, old, new):
    last_clicked_ID = list(set(old) ^ set(new))[0]
    last_clicked_button_stuff = status_list[last_clicked_ID]
    in_active = last_clicked_ID in new
    last_clicked_button_stuff(in_active)

    for i in range(len(datasetCDS.data["index"])):
        if datasetCDS.data['generation'][i] in genList and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and \
                datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        elif genList == [0] * 8 and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and \
                datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        elif datasetCDS.data['generation'][i] in genList and typeList == [""] * 18 and datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        elif datasetCDS.data['generation'][i] in genList and (
                datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and statusList == [""] * 4:
            booleans[i] = True
        elif genList == [0] * 8 and typeList == [""] * 18 and datasetCDS.data['status'][i] in statusList:
            booleans[i] = True
        elif genList == [0] * 8 and (datasetCDS.data['type_1'][i] in typeList or datasetCDS.data['type_2'][i] in typeList) and statusList == [""] * 4:
            booleans[i] = True
        elif datasetCDS.data['generation'][i] in genList and typeList == [""] * 18 and statusList == [""] * 4:
            booleans[i] = True
        else:
            booleans[i] = False

    new_view = CDSView(filter=BooleanFilter(booleans))
    php.select(name='circle')[0].view = new_view
    patt.select(name='circle')[0].view = new_view
    pspa.select(name='circle')[0].view = new_view
    pdef.select(name='circle')[0].view = new_view
    pspd.select(name='circle')[0].view = new_view
    pspe.select(name='circle')[0].view = new_view
    lineFig.select(name='circle')[0].view = new_view

STATUS = ["Normal", "Sub Legendary", "Legendary", "Mythical"]
status = CheckboxButtonGroup(labels=STATUS, active=[])
status.on_change('active', whatSatus)

typeDiv = Div(text="<b>Types</b>")
genDiv = Div(text="<b>Generation</b>")
statusDiv = Div(text="<b>Status</b>")

lower = row(column(genDiv, gens), column(statusDiv, status))
options_col = column(typeDiv, types, lower)
main_layout = column(gp, options_col)

doc = curdoc()
doc.title = 'PokeChart'
doc.add_root(main_layout)

# in terminal: bokeh serve --show main.py
#on file directory to be able to use the filtering functions
