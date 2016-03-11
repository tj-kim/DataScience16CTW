""" 
Uses Bokeh library to generate map with schools printed onto map of US.
"""

# Imports
from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.us_states import data as states
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.models import ColumnDataSource, Circle, HoverTool, CustomJS
from bokeh.palettes import BuGn9
from bokeh.palettes import Blues9
from random import randint
import college as c

# Deleting Hawaii and Alaska from states data to make concise
del states["HI"]
del states["AK"]

EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")

# Determining Shades of green used to color states
colors = ['#00441b', '#006d2c', '#238b45', '#41ae76']

# Extracting Latitude and Longitude data from states
state_xs = [states[code]["lons"] for code in states]
state_ys = [states[code]["lats"] for code in states]

def build_map(collegelist):
    """
    Adapted from Bokeh US Map States example
    Generate Map of US with States division
    Color in states
    """
    p = figure(title="College Choice Map", toolbar_location="above",
               plot_width=1100, plot_height=700)

    p.patches(state_xs, state_ys, fill_alpha=0.5,
              line_color="#884444", line_width=2, line_alpha=0.3,
              fill_color = colors*12)

    p.background_fill_color = Blues9[7]

    # Eliminate X and Y grid lines in map for aesthetic purposes
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    # Importing college shown based upon filtered list via user input
    source = c.college_dict(collegelist)

    # Generating Small dots to indicate College Location
    circle = Circle(x="lon", y="lat", size=10, fill_color="firebrick", fill_alpha=0.8, line_color=None)
    visible = Circle(x="lon", y="lat", size=10, fill_color="blue", fill_alpha=1, line_color=None)
    cr = p.add_glyph(source, circle, selection_glyph = visible, nonselection_glyph = circle)

    # Display information when mouse hovers over the dots of colleges
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
     
    p.add_tools(hover)


    output_file("collegelist.html", title="collegelist.py example")

    show(p)