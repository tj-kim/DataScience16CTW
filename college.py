############################################################################
# Imports
############################################################################

import pandas as pd
from bokeh.models import ColumnDataSource

college = pd.read_csv('new_college.csv')
dictionary = pd.read_csv('CollegeScorecard_Raw_Data/CollegeScorecardDataDictionary-09-12-2015.csv')

############################################################################
#Global Variables
############################################################################

allcollegelist = []
for i in range(len(college)):
    allcollegelist.append(i)

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
    pref = 'low' or 'medium', or 'high'
    """
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
    Preference:
        both = 0
        public = 1
        private = 2
    """
    output_list = []
    if preference == 0: # Both Types
        output_list = collegelist
    if preference == 1: # Public College
        for i in collegelist:
            if str(college['NPT4_PUB'][i]) != 'nan':
                output_list.append(i)
    if preference == 2: # Private College
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
    if option == 'more':
        for i in collegelist:
            if college['UGDS'][i] > popul:
                if i not in filteredlist:
                    filteredlist.append(i)
    if option == 'less':
        for i in collegelist:
            if college['UGDS'][i] < popul:
                if i not in filteredlist:
                    filteredlist.append(i)
    
    return filteredlist

def get_result(vr = 600, wr = 600, mt = 600):
    filteredlist = []
    college_list = sat(vr,wr,mt,allcollegelist)
    # college_list = diversity("low", college_list)
    # college_list = public_private(college_list, 2)
    # college_list = cost(college_list, 20000)
    # college_list = major("engineering; english",college_list)
    # college_list = pref_popul(10000, college_list, 'less')
    for i in college_list:
        filteredlist.append(college['INSTNM'][i])
    return college_list

def college_dict(collegelist):
    latlist = []
    lonlist = []
    namelist = []
    urllist = []
    for collegeid in collegelist:
        latlist.append(college.LATITUDE[collegeid])
        lonlist.append(college.LONGITUDE[collegeid])
        namelist.append(college.INSTNM[collegeid])
        urllist.append(college.INSTURL[collegeid])

    source = ColumnDataSource(
        data=dict(
            lat=latlist,
            lon=lonlist,
            name=namelist,
            url=urllist
        )
    )
    return source