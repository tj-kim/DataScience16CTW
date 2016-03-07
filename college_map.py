from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.us_states import data as states
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.models import ColumnDataSource, Circle, HoverTool, CustomJS
import college as c


del states["HI"]
del states["AK"]

EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")

state_xs = [states[code]["lons"] for code in states]
state_ys = [states[code]["lats"] for code in states]

county_xs=[counties[code]["lons"] for code in counties if counties[code]["state"] not in EXCLUDED]
county_ys=[counties[code]["lats"] for code in counties if counties[code]["state"] not in EXCLUDED]

# colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]

# county_colors = []
# for county_id in counties:
#     if counties[county_id]["state"] in EXCLUDED:
#         continue
#     try:
#         rate = unemployment[county_id]
#         idx = int(rate/6)
#         county_colors.append(colors[idx])
#     except KeyError:
#         county_colors.append("black")   


p = figure(title="College Choice Map", toolbar_location="above",
           plot_width=1100, plot_height=700)

p.patches(county_xs, county_ys,
          fill_color="#D4B9DA", fill_alpha=0.7, 
          line_color="white", line_width=0.0)

p.patches(state_xs, state_ys, fill_alpha=0.0,
          line_color="#884444", line_width=2, line_alpha=0.3)




collegelist = c.get_result(800,800,800)
source = c.college_dict(collegelist)

circle = Circle(x="lon", y="lat", size=10, fill_color="firebrick", fill_alpha=0.8, line_color=None)
visible = Circle(x="lon", y="lat", size=10, fill_color="blue", fill_alpha=1, line_color=None)
# invisible = Circle(x="lon", y="lat", size=10, fill_color="firebrick", fill_alpha=0.5, line_color=None)
cr = p.add_glyph(source, circle, selection_glyph = visible, nonselection_glyph = circle)


hover = HoverTool(
        tooltips="""
        <div>
            <div>
                <img
                    src="@url" height="42" alt="@url" width="42"
                    style="float: left; margin: 0px 15px 15px 0px;"
                    border="2"
                ></img>
            </div>
            <div>
                <span style="font-size: 17px; font-weight: bold;">@name</span>
                <span style="font-size: 15px; color: #966;">[$index]</span>
            </div>
            <div>
                <a 
                    href="@url" target="_blank"
                >School Website</a>
            </div>
            <div>
                <span style="font-size: 15px;">Location</span>
                <span style="font-size: 10px; color: #696;">($x, $y)</span>
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