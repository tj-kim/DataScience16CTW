"""
Description:

Equivalent to alg_finalized_1_1 except put into a py file. This allows other py files to import it and use it. Holds algorithms that filters colleges out based upon user input.
"""


############################################################################
# Imports
############################################################################

import pandas as pd
from bokeh.models import ColumnDataSource

# Import filtered dataframe
college = pd.read_csv('new_college.csv')

# Import dictionary used for mapping major to description
dictionary = pd.read_csv('CollegeScorecard_Raw_Data/CollegeScorecardDataDictionary-09-12-2015.csv')

############################################################################
#Global Variables
############################################################################

# Creating allcollegelist for indexing, holds integer value from 0 to 7803, for each college
allcollegelist = []
for i in range(len(college)):
    allcollegelist.append(i)

# Below are categories used in college search algorithm and display
# They may not be used but are present here for reference

alg_categories = ['CONTROL', 
                  'SATVR25', 'SATVR75', 'SATMT25', 'SATMT75', 'SATWR25', 'SATWR75',
                  'NPT4_PUB', 'NPT4_PRIV']

alg_race = ['UGDS','UGDS_WHITE', 'UGDS_BLACK', 'UGDS_HISP', 'UGDS_ASIAN',
            'UGDS_AIAN', 'UGDS_NHPI', 'UGDS_2MOR', 'UGDS_NRA', 'UGDS_UNKN',
            'UGDS_WHITENH', 'UGDS_API', 'UGDS_API']

alg_majors = ['PCIP01', 'PCIP03', 'PCIP04', 'PCIP05', 'PCIP09', 'PCIP10', 'PCIP11',
              'PCIP12', 'PCIP13', 'PCIP14', 'PCIP15', 
              'PCIP16', 'PCIP19', 'PCIP22', 'PCIP23', 'PCIP24', 'PCIP25', 'PCIP26', 'PCIP27',
              'PCIP29', 'PCIP30', 'PCIP31', 'PCIP38', 'PCIP39', 'PCIP40', 'PCIP41', 'PCIP42',
              'PCIP43', 'PCIP44', 'PCIP45', 'PCIP46',
              'PCIP47', 'PCIP48', 'PCIP49', 'PCIP50', 'PCIP51', 'PCIP52', 'PCIP54']

disp_categories = ['OPEID','INSTNM','CITY','STABBR', 'INSTURL', 'HIGHDEG','ADM_RATE']



#creating a dictionary where the key is the major variable and the value is the label (name of the major)
dmajor = {}
for i in range(len(dictionary)):
    if str(dictionary.label[i]) != 'nan':
        dmajor[dictionary['VARIABLE NAME'][i]] = dictionary.label[i]

############################################################################
# Functions
############################################################################

def each_sat(score, column, collegelist, percentile):
    """
    Sub Function for section_sat
    determines which colleges the specific SAT subject is greater/less than
    Compares to one percentile at a time
    """
    filteredlist = []
    
    if percentile == 25:
        for i in collegelist:
            if score >= college[column][i]-50:
                filteredlist.append(i)
    
    if percentile == 75:
        for i in collegelist:
            if score <= college[column][i]+50:
                filteredlist.append(i)
        
    return filteredlist

def section_sat(score, section, collegelist):
    """
    Runs section but both percentiles
    section = 'VR' or 'WR' or 'MT'
    sub function of sat
    """
    column25 = 'SAT'+section+'25'
    column75 = 'SAT'+section+'75'
    
    list25 = each_sat(score, column25, collegelist, 25)
    list75 = each_sat(score, column75, list25, 75)
    
    return list75

def sat(vrscore, wrscore, mtscore, collegelist):
    """
    Gets SAT Score range of suited college
    vrscore: reading score (int)
    wrscore: writing score (int)
    mtscore: math score (int)
    collegelist (list)
    """
    listvr = section_sat(vrscore, 'VR', collegelist)
    listwr = section_sat(wrscore, 'WR', listvr)
    listmt = section_sat(mtscore, 'MT', listwr)
    
    return listmt

def diversity(pref, collegelist):
    """
    Takes user input in how much racial diversity they want at school
    pref = 'does not matter', low' or 'medium', or 'high'
    """
    if pref == 'does not matter':
        return collegelist

    r = alg_race[1:]
    high = []
    medium = collegelist[:]
    low = []
    for i in collegelist:
        highmarker = 1
        for race in r:
            if college[race][i] >= 0.6:
                if i not in low:
                    low.append(i)
                    medium.remove(i)
            if college[race][i] >= 0.35:
                highmarker = 0
        if highmarker == 1:
            high.append(i)
            medium.remove(i)
    if pref == 'high':
        return high
    if pref == 'medium':
        return medium
    if pref == 'low':
        return low

def public_private(collegelist, preference):
    """
    Outputs schools that users want either public, private, or both
    """
    output_list = []
    if preference == 'both': # Both Types
        output_list = collegelist
    if preference == 'public': # Public College
        for i in collegelist:
            if str(college['NPT4_PUB'][i]) != 'nan':
                output_list.append(i)
    if preference == 'private': # Private College
        for i in collegelist:
            if str(college['NPT4_PRIV'][i]) != 'nan':
                output_list.append(i)
    return output_list

def cost(collegelist, max_cost):
    """
    filters out based on how much people want to pay
    """
    output_list = []
    for i in collegelist:
        if college['NPT4_PUB'][i] < max_cost + 5000:
            output_list.append(i)
        if college['NPT4_PRIV'][i] < max_cost + 5000:
            output_list.append(i)
    return output_list

def each_major(searchstr, collegelist):
    """
    Analyses one major at a time to get college list
    """
    filteredlist = []
    for key in dmajor:
        if searchstr.lower() in dmajor[key].lower():
            for i in collegelist:
                if college[key][i] > 0.05:
                    if i not in filteredlist:
                        filteredlist.append(i)
                    
    return filteredlist

def major(search, collegelist):
    """
    Analyses many different majors and appends them
    Uses each_major
    """
    searchlst = search.split(';')
    filteredlist = []
    for searchstr in searchlst:
        searchlist = each_major(searchstr, collegelist)
        for i in searchlist:
            if i not in filteredlist:
                filteredlist.append(i)
    return filteredlist

def pref_popul(popul, collegelist, option):
    """
    option = 'more' or 'less'
    """
    filteredlist = []
    if option == 'more than':
        for i in collegelist:
            if college['UGDS'][i] > popul:
                if i not in filteredlist:
                    filteredlist.append(i)
    if option == 'less than':
        for i in collegelist:
            if college['UGDS'][i] < popul:
                if i not in filteredlist:
                    filteredlist.append(i)
    
    return filteredlist

def get_result(vr = 600, wr = 600, mt = 600, div = "medium", 
    pubprv = 'both', maxcost = 200000, majstr = "engineering; science",
    pop = 100000, popchoice = "less than"):

    """
    Utilizes all the college filtering algorithm functions above
    Key:
        vr, wr, mt, = sat score values inputed (integer)
        div = racial diversity at school (low, medium, high)
        pubprv = public or privat school, or include both (str)
        maxcost = maximum tuition (including scholarship subtraction) willing to pay
        majstr = type in desired majors separated by ';' (string)
        pop = desired population bench mark
        popchoice = indicates either greater/lesser than population bench mark (more, lesss) (string)

    Returns filtered version of allcollegelist with recommended colleges
    """
    college_list = sat(vr,wr,mt,allcollegelist)
    college_list = diversity(div, college_list)
    college_list = public_private(college_list, pubprv)
    college_list = cost(college_list, maxcost)
    college_list = major(majstr,college_list)
    college_list = pref_popul(pop, college_list, popchoice)
    
    return college_list

def college_dict(collegelist):
    """
    Creates lists for referencing recommended college labels
    Labels:
        School Location (latlist, lonlist)
        School Name (namelist)
        School Web Site (urllist)
        School Admission rate (admlist)
        School City (citylist)
        School statelist (stlist)
    """
    # Create empty holder lists for each label
    latlist = []
    lonlist = []
    namelist = []
    urllist = []
    admlist = []
    citylist = []
    stlist = []

    # add components into holder list
    for collegeid in collegelist:
        latlist.append(college.LATITUDE[collegeid])
        lonlist.append(college.LONGITUDE[collegeid])
        namelist.append(college.INSTNM[collegeid])
        urllist.append(college.INSTURL[collegeid])
        admlist.append(college.ADM_RATE[collegeid])
        citylist.append(college.CITY[collegeid])
        stlist.append(college.STABBR[collegeid])

    source = ColumnDataSource(
        data=dict(
            lat = latlist,
            lon = lonlist,
            name = namelist,
            url = urllist,
            adm = admlist,
            city = citylist,
            state = stlist
        )
    )
    return source