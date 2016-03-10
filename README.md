# Data Science Change the World

Jee Hyun Kim & TJ Kim

## Repository Guidelines

### Ipython Notebooks

new_data_csv_book.ipynb: Ipython notebook with walkthrough and documentation through taking initial data csv downloaded from collegescorecard, and filtering out data columns we deem unuseful. Output is "new_college.csv" file, with filtered out columns.

alg_finalized_1_1.ipynb : Ipython notebook with walkthrough and documentation on algorithms used to filter out colleges through user preference input.

### Py Files

college.py: Equivalent to alg_finalized_1_1 except put into a py file. This allows other py files to import it and use it. Holds algorithms that filters colleges out based upon user input.

college_gui.py: Uses Tkinter library to build a graphic user interface for users to to input their preferences and information. This file is imported by college_map for final using.

college_map.py: Uses Bokeh library to generate map with schools printed onto map of US. Calls upon college.py and college_gui.py to generate the map.

### PDF Files

ChangetheWorldProposal.pdf: Initial Project Proposal that outlines what we want to accomplish for this project