from bokeh.plotting import figure, show, output_file
#from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.us_states import data as states
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.models import ColumnDataSource, Circle, HoverTool, CustomJS
from random import randint
import college as c

from bokeh.palettes import BuGn9
from bokeh.palettes import Blues9

del states["HI"]
del states["AK"]

EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")

state_xs = [states[code]["lons"] for code in states]
state_ys = [states[code]["lats"] for code in states]

#county_xs=[counties[code]["lons"] for code in counties if counties[code]["state"] not in EXCLUDED]
#county_ys=[counties[code]["lats"] for code in counties if counties[code]["state"] not in EXCLUDED]

colors = ['#00441b', '#006d2c', '#238b45', '#41ae76']

# state_colors = []
# for state_id in states:
#     if states[state_id]["state"] in EXCLUDED:
#         continue
#     try:
#         rate = unemployment[state_id]
#         idx = int(rate/6)
#         state_colors.append(colors[idx])
#     except KeyError:
#         state_colors.append("black")   

def build_map(collegelist):
    p = figure(title="College Choice Map", toolbar_location="above",
               plot_width=1100, plot_height=700)

    # p.patches(county_xs, county_ys,
    #         fill_color="#D4B9DA", fill_alpha=0.7, 
    #         line_color="white", line_width=0.0)

    p.patches(state_xs, state_ys, fill_alpha=0.5,
              line_color="#884444", line_width=2, line_alpha=0.3,
              fill_color = colors*12)

    p.background_fill_color = Blues9[7]

    # change just some things about the x-grid and y grid
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    source = c.college_dict(collegelist)

    circle = Circle(x="lon", y="lat", size=10, fill_color="firebrick", fill_alpha=0.8, line_color=None)
    visible = Circle(x="lon", y="lat", size=10, fill_color="blue", fill_alpha=1, line_color=None)
    # invisible = Circle(x="lon", y="lat", size=10, fill_color="firebrick", fill_alpha=0.5, line_color=None)
    cr = p.add_glyph(source, circle, selection_glyph = visible, nonselection_glyph = circle)


    hover = HoverTool(
            tooltips="""
            <div>
                <div>
                    <span style="font-size: 17px; font-weight: bold;">@name</span>
                </div>
                <div>
                    <span style="font-size: 14px;">@state</span>
                    <span style="font-size: 13px;">@city</span>
                </div>
                <div>
                    <span style="font-size: 13px;">Admission Rate</span>
                    <span style="font-size: 13px; color: #696;">@adm</span>
                </div>
                <div>
                    <span style="font-size: 13px;">@url</span>
                </div>                
            </div>
            """,
            callback = CustomJS(args={'source': source}, code="source.set('selected', cb_data['index']);"),
            renderers = [cr]
            )

    # hover = HoverTool(
    #         tooltips=[
    #             ("College", "@name"),
    #             ("url", "@url"),
    #         ],
    #         callback = CustomJS(args={'source': source}, code="source.set('selected', cb_data['index']);"),
    #         renderers = [cr]
    #     )
     
    p.add_tools(hover)


    output_file("collegelist.html", title="collegelist.py example")

    show(p)

# collegeslist = c.get_result(
#     vr = 800, 
#     wr = 800, 
#     mt = 800, 
#     div = "does not matter", 
#     pubprv = 'both', 
#     maxcost = 2000000, 
#     majstr = "engineering", 
#     pop = 1000, 
#     popchoice = "less than")
# print collegeslist
# build_map(collegeslist)