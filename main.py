import pandas as pd

from bokeh.embed import json_item
from bokeh.layouts import layout, gridplot
from bokeh.models import HoverTool, ColumnDataSource, CustomJSHover, CategoricalColorMapper
from bokeh.plotting import figure, show
from bokeh.models.widgets import Panel, Tabs, Select

dataframe = pd.read_csv("pokedex_(Update_05.20).csv")
datasetCDS = ColumnDataSource(data=dataframe)
total = dataframe["hp"] + dataframe["attack"] + dataframe["sp_attack"] + dataframe["defense"] + dataframe[
    "sp_defense"] + dataframe["speed"]

# adding total as a new column in datasetCDS
datasetCDS.data["total"] = total

dataframe['formPN'] = dataframe['pokedex_number'].apply(lambda x: '{0:0>3}'.format(x))
# creates the url to the images
dataframe['url'] = 'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/' + dataframe['formPN'].astype(
    str) + '.png'
dataframe['url'] = dataframe['url'].str.replace(' ', '-')
dataframe['url'] = dataframe['url'].str.lower()

datasetCDS.data["url"] = dataframe['url']

#dataframe.to_excel("test.xlsx")
sizeCoeff = 3

datasetCDS.data['hpSize'] = dataframe['hp'] / sizeCoeff
datasetCDS.data['attackSize'] = dataframe['attack'] / sizeCoeff
datasetCDS.data['sp_attackSize'] = dataframe['sp_attack'] / sizeCoeff
datasetCDS.data['defenseSize'] = dataframe['defense'] / sizeCoeff
datasetCDS.data['sp_defenseSize'] = dataframe['sp_defense'] / sizeCoeff
datasetCDS.data['speedSize'] = dataframe['speed'] / sizeCoeff

TOOLTIPS = """
    <div style="width: 150px;>
        <div style="display: grid;">
            <span style="font-size: 17px; font-weight: bold;">@name</span></div>
        <div style="display: grid;"><span style="font-size: 14px; font-weight: bold;">Pokedex: @pokedex_number</span></div>
        </div style="display: grid;">
        <div style="position: bottom;">

        <div style="display: grid; margin-bottom: 2%;">
            <img src="@url" height="142" alt="@name" width="100%"
                style=" float:right; margin: 0px;"
                border="1">
            </img>
        </div>
        <div style="position: relative; text-align: center; font-size: 10px; vertical-align: bottom;">
        <div style="width:13%;height:@hpSize;border:1px solid #000;display: inline-block;vertical-align: bottom; background-color: lightblue;">@hp</div>
          <div style="width:13%;height:@attackSize;border:1px solid #000;display: inline-block;vertical-align: bottom; background-color: lightblue;">@attack</div>
          <div style="width:13%;height:@sp_attackSize;border:1px solid #000;display: inline-block;vertical-align: bottom; background-color: lightblue;">@sp_attack</div>
          <div style="width:13%;height:@defenseSize;border:1px solid #000;display: inline-block;vertical-align: bottom; background-color: lightblue;">@defense</div>
          <div style="width:13%;height:@sp_defenseSize;border:1px solid #000;display: inline-block;vertical-align: bottom; background-color: lightblue;">@sp_defense</div>
          <div style="width:13%;height:@speedSize;border:1px solid #000;display: inline-block;vertical-align: bottom; background-color: lightblue;">@speed</div>
        </div>
    </div>
"""
types = ["Fairy", "Steel", "Dark", "Dragon", "Ghost", "Rock", "Bug", "Psychic",
         "Flying", "Ground", "Poison", "Fighting", "Ice", "Grass", "Electric",
         "Water", "Fire", "Normal"]
colors = ["#EAA3DC", "#B8B8D0", "#765747", "#7636F6", "#745797", "#BF9F38", "#A5B82B",
          "#FF4980", "#AC8FEF", "#E9C26E", "#AF399D", "#D51C0D", "#7FDADA", "#55CA59",
          "#FFCE2E", "#5591F0", "#FF7919", "#A9A879"]
color_mapper = CategoricalColorMapper(
    palette=colors,
    factors=types)


def color(type):
    for j in range(len(types)):
        if type == types[j]:
            return colors[j]


php = figure(x_axis_label="total", y_axis_label="hp", tooltips=TOOLTIPS, active_scroll="wheel_zoom")
php.circle(x="total", y="hp", source=datasetCDS,alpha=0.2, hover_alpha=1, color={'field': 'type_1', 'transform': color_mapper},
           size=5)
tab1 = Panel(child=php, title="hp")

patt = figure(x_axis_label="total", y_axis_label="attack", tooltips=TOOLTIPS, active_scroll="wheel_zoom")
patt.circle(x="total", y="attack", source=datasetCDS,alpha=0.2, hover_alpha=1, color={'field': 'type_1', 'transform': color_mapper}, size=5)
tab2 = Panel(child=patt, title="attack")

pspa = figure(x_axis_label="total", y_axis_label="sp_attack", tooltips=TOOLTIPS, active_scroll="wheel_zoom")
pspa.circle(x="total", y="sp_attack", source=datasetCDS,alpha=0.2, hover_alpha=1, color={'field': 'type_1', 'transform': color_mapper}, size=5)
tab3 = Panel(child=pspa, title="sp_attack")

pdef = figure(x_axis_label="total", y_axis_label="defense", tooltips=TOOLTIPS, active_scroll="wheel_zoom")
pdef.circle(x="total", y="defense", source=datasetCDS,alpha=0.2, hover_alpha=1, color={'field': 'type_1', 'transform': color_mapper}, size=5)
tab4 = Panel(child=pdef, title="defense")

pspd = figure(x_axis_label="total", y_axis_label="sp_defense", tooltips=TOOLTIPS, active_scroll="wheel_zoom")
pspd.circle(x="total", y="sp_defense", source=datasetCDS,alpha=0.2, hover_alpha=1, color={'field': 'type_1', 'transform': color_mapper}, size=5)
tab5 = Panel(child=pspd, title="sp_defense")

pspe = figure(x_axis_label="total", y_axis_label="speed", tooltips=TOOLTIPS, active_scroll="wheel_zoom")
pspe.circle(x="total", y="speed", source=datasetCDS,alpha=0.2, hover_alpha=1, color={'field': 'type_1', 'transform': color_mapper}, size=5)
tab6 = Panel(child=pspe, title="speed")

tabs = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6])

lineFig = figure(tooltips=TOOLTIPS, active_scroll="wheel_zoom")

mult = [[0] * 6] * len(datasetCDS.data["index"])
colorRange=[""]*len(datasetCDS.data["index"])

for i in range(len(datasetCDS.data["index"])):
      mult[i]=[datasetCDS.data["hp"][i],
      datasetCDS.data["attack"][i],
      datasetCDS.data["sp_attack"][i],
      datasetCDS.data["defense"][i],
      datasetCDS.data["sp_defense"][i],
      datasetCDS.data["speed"][i]]

      colorRange[i]=color(datasetCDS.data['type_1'][i])

dataframe['names'] = [["1", "2", "3", "4", "5", "6"]] * len(datasetCDS.data["index"])
datasetCDS.data['names'] = dataframe['names']

dataframe['mult'] = mult
datasetCDS.data['mult'] = dataframe['mult']

datasetCDS.data['color'] = colorRange

lineFig.multi_line(xs="names", ys="mult", source=datasetCDS, color="color", alpha=0.1,hover_alpha=1)

p = gridplot([[tabs, lineFig]], toolbar_location=None)

# show result
show(p)
