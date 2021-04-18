import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style
import seaborn as sns
import pycountry_convert as pc
import plotly.express as px
import plotly.graph_objects as go


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
#Goal:  Visualization World Happiness Report; is the people happy or not

# #load data
World_report_2021 = pd.read_csv("world-happiness-report-2021.csv")
# #overwiew the data
print(World_report_2021.info())
# any data is missing
print(World_report_2021.isnull().sum())
print(World_report_2021.describe())


#overwiew the data
# sort by Ladder score, Finland is first and Afghanistan is last
World_report_2021=World_report_2021.sort_values(by=["Ladder score"],ascending=False )
#create graph with top 10 and bottom 10
top10_country=World_report_2021.groupby("Country name")["Ladder score"].mean().sort_values(ascending=False)[:10]
bottom10_country=World_report_2021.groupby("Country name")["Ladder score"].mean().sort_values(ascending=False)[-10:]
TB10_country=top10_country.append(bottom10_country).reset_index()
plt.figure(figsize=(20,7))
sns.barplot(y="Country name",x="Ladder score",data=TB10_country,palette="Spectral" )
for x,y in enumerate(TB10_country["Ladder score"]):
    plt.text(y+0.05,x,str(float(y)))
sns.despine()
plt.show()

# #
# whats the differet in happy and unhappy country
# Separate the happy country or not
LS_median= World_report_2021["Ladder score"].median() #median in ladder score
World_report_2021["Happy_country"]=World_report_2021["Ladder score"].apply(lambda x:1 if x >=LS_median else 0)
happy=World_report_2021[World_report_2021["Happy_country"] ==1]
unhappy = World_report_2021[World_report_2021["Happy_country"] ==0]

# #create the graph
columns_list=['Logged GDP per capita','Social support',
                'Healthy life expectancy','Freedom to make life choices',
                'Generosity','Perceptions of corruption']
for col in columns_list:
    fig=sns.kdeplot(happy[col], shade=True,color="r",alpha=0.3)
    fig=sns.kdeplot(unhappy[col], shade=True,color="g",alpha=0.3)
    fig.get_yaxis().set_visible(False)
    for s in ["top", "right", "left"]:
        fig.spines[s].set_visible(False)
    plt.title("Happy country in red, unhappy country in green")
    plt.show()

#
# #Create map to clear where the happy country is
#Clean data
country_code = pc.map_country_name_to_country_alpha3()#set the country code
World_report_name=World_report_2021.set_index("Country name")
temp_data = pd.DataFrame(World_report_name['Ladder score']).reset_index() #only need the country name and ladder score
#found the country not in ISO3166, could be the name is different
Not_in_ISO3166=temp_data[temp_data["Country name"].isin(country_code)==False]  #country not in list

#Change the name to country code or delete
temp_data.loc[temp_data["Country name"] == "Taiwan Province of China", "Country name"]= "Taiwan, Province of China"
temp_data.loc[temp_data["Country name"] == "Hong Kong S.A.R. of China", "Country name"]= "Hong Kong"
temp_data.loc[temp_data["Country name"] == "Congo (Brazzaville)", "Country name"]= "Congo"
temp_data.loc[temp_data["Country name"] == "Palestinian Territories", "Country name"]= "Palestine, State of"
temp_data.drop(temp_data[temp_data["Country name"]=="Kosovo"].index,inplace=True) #Not part of the ISO 3166 standard
temp_data.drop(temp_data[temp_data["Country name"]=="North Cyprus"].index,inplace=True) #Not part of the ISO 3166 standard
temp_data['iso_alpha'] = temp_data['Country name'].apply(lambda x:pc.country_name_to_country_alpha3(x,))

# #create graph
fig=px.choropleth(temp_data, locations='iso_alpha',color='Ladder score',hover_name='Country name',color_continuous_scale=px.colors.diverging.Fall)
fig.update_layout(title_text='World map  Ladder score',geo_showframe=False,title_font_size=40)
fig.show()
# create graph in different way
# data = dict(type = 'choropleth',
#             locations = World_report_2021['Country name'].to_list(),
#             locationmode = 'country names',
#             colorscale= 'Spectral',
#             text= World_report_2021['Country name'].to_list(),
#             z=(World_report_2021['Logged GDP per capita']).to_list(),
#             colorbar = {'title':'Economic Production', 'len':250,'lenmode':'pixels' })
# col_map = go.Figure(data = [data])
# col_map.show()
#
# # most happy country in different regional
#clean data with country name, region and ladder scoure
new_report=World_report_2021[["Country name","Regional indicator","Ladder score"]]
# #ladder score in different country
fig = sns.kdeplot(new_report["Ladder score"],hue=new_report["Regional indicator"],fill=True)
fig.get_yaxis().set_visible(False)
for i in ["top", "right", "left"]:
        fig.spines[i].set_visible(False)
plt.show()
#
#

# most happy country in different regional
#country in Sub-Saharan Africa
Sub_Saharan_Africa=new_report.loc[new_report["Regional indicator"]=="Sub-Saharan Africa"].sort_values(by=["Ladder score"],ascending=False).reset_index(drop=True).loc[0]
#'Western Europe'
Western_Europe =new_report.loc[new_report["Regional indicator"]=="Western Europe"].sort_values(by=["Ladder score"],ascending=False).reset_index(drop=True).loc[0]
# 'North America and ANZ'
North_America_and_ANZ =new_report.loc[new_report["Regional indicator"]=="North America and ANZ"].sort_values(by=["Ladder score"],ascending=False).reset_index(drop=True).loc[0]
# 'Middle East and North Africa'
Middle_East_and_North_Africa =new_report.loc[new_report["Regional indicator"]=="Middle East and North Africa"].sort_values(by=["Ladder score"],ascending=False).reset_index(drop=True).loc[0]
#  'Latin America and Caribbean'
Latin_America_and_Caribbean =new_report.loc[new_report["Regional indicator"]=="Latin America and Caribbean"].sort_values(by=["Ladder score"],ascending=False).reset_index(drop=True).loc[0]
#  'Central and Eastern Europe'
Central_and_Eastern_Europe =new_report.loc[new_report["Regional indicator"]=="Central and Eastern Europe"].sort_values(by=["Ladder score"],ascending=False).reset_index(drop=True).loc[0]
#  'East Asia'
East_Asia =new_report.loc[new_report["Regional indicator"]=="East Asia"].sort_values(by=["Ladder score"],ascending=False).reset_index(drop=True).loc[0]
#  'Southeast Asia'
Southeast_Asia =new_report.loc[new_report["Regional indicator"]=="Southeast Asia"].sort_values(by=["Ladder score"],ascending=False).reset_index(drop=True).loc[0]
#  'Commonwealth of Independent States'
Commonwealth_of_Independent_States =new_report.loc[new_report["Regional indicator"]=="Commonwealth of Independent States"].sort_values(by=["Ladder score"],ascending=False).reset_index(drop=True).loc[0]
#  'South Asia'
South_Asia=new_report.loc[new_report["Regional indicator"]=="South Asia"].sort_values(by=["Ladder score"],ascending=False).reset_index(drop=True).loc[0]
#merge all the data
Merge_data=pd.DataFrame([South_Asia,Commonwealth_of_Independent_States,
                         East_Asia,Central_and_Eastern_Europe,
                         Latin_America_and_Caribbean,Middle_East_and_North_Africa,
                         North_America_and_ANZ,Western_Europe,
                         Sub_Saharan_Africa]).sort_values(by=["Ladder score"],ascending=False)
print(Merge_data)
