import streamlit as st
import requests as rq
#from RacialData import RacialData
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare
import plotly.express as px
import pandas as pd
st.set_page_config(page_title='English Site', layout='wide' )

class RacialData:
    def __init__(self, race):
        self.race = race
        self.raceD = {'1': 'All Races', '2': 'White Alone', '7': 'Black Alone', '10': 'Asian Alone', '12': 'Hispanic'}
        self.raceDescription = self.raceD[race]
        self.businesstranslate = {'1': '00', '2': '30', '7': '40', '10': '60', '12': '80'}
        self.businessquery = self.businesstranslate[self.race]
        self.shootingtranslate = {'1': 'All', '7': 'Black', '2': 'White', '10': 'Asian', '12': 'Hispanic'}
        self.shootingquery = self.shootingtranslate[self.race]
        self.data = {}

    def poverty(self, query):
        return rq.get(
            f'https://api.census.gov/data/timeseries/poverty/histpov2?get={query}&time=2020&RACE={self.race}&key=6eaab5fb7daa4ffc66a8621cafec7e8a929ec1f7').json()

    def generateData(self):
        stats = ['FAM', 'FAMPOV', 'FEMHH', 'FEMHHPOV', 'POP', 'POV']
        self.data['Annual Payroll'] = self.businessData()[1][0]
        self.policeShootings()
        for i in stats:
            pover = self.poverty(i)
            self.data[pover[0][0]] = int(pover[1][0])

    def businessData(self):
        return rq.get(
            f'https://api.census.gov/data/2016/ase/csa?get=PAYANN,RCPPDEMP&for=us:*&RACE_GROUP={self.businessquery}&key=6eaab5fb7daa4ffc66a8621cafec7e8a929ec1f7').json()

    def policeShootings(self):
        df = pd.read_csv('PoliceShootings.csv')
        if self.shootingquery != 1:
            df = df.loc[df["Victim's race"] == self.shootingquery]
            df.dropna()
        self.data['Total Shootings'] = len(df)
        self.data['Allegedly Armed'] = len(df.loc[df['Armed/Unarmed Status'] == 'Allegedly Armed'])
        self.data['Unarmed/Did Not Have Actual Weapon'] = len(
            df.loc[df['Armed/Unarmed Status'] == 'Unarmed/Did Not Have Actual Weapon'])
        self.data['Unclear'] = len(df.loc[df['Armed/Unarmed Status'] == 'Unclear'])

    def returnData(self):
        return self.data

st.markdown("""
<style>
.big-font {
    font-size:25px !important;
    color:blue;
}
.small-font {
    font-size:15px !important;
    color:#00FFFF;
    margin-left: 40px;
}
.text-font{
    font-size: 15px;
    color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">By the force of our demands, our determination and our numbers, we shall splinter the segregated South into a thousand pieces and put them back together in the image of God and democracy.</p>', unsafe_allow_html=True)
st.markdown('<p class="small-font">―John Lewis, March: Book Two</p>', unsafe_allow_html=True)
st.markdown('<p class="text-font">The late John Lewis awoke a nation of revolutionaries and activtists striving to foster equality. Despite empanicipation, hundreds of years later inequality and racism still persists. Institutional Racism prevents social mobility and contributes to an ever inequal proprtion of wealth and rights. <br> <br> However, with the advance of technology and data science, we now can take a different outlook on the use of "our numbers". Statistics have the power to objectively convey information and generate analysis surrounding issues prevalent in the status quo. </p>', unsafe_allow_html=True)
st.markdown('<p class="text-font">The purpose of this project is to analyze statistics relevant to the United States and its demographics, with the hope of being able to visualize these discrepancies. While perhaps an unusual approach, this project intends on focusing on people of color and generating <b> Empathy </b> through numbers and data. This project will go through various factors within society such as Education, Work and Policy Brutality. While there is much more research to be done, it is my hope that through this project I can shed light just on how disproportionate we as a society have begun, and how change must begin urgently. </p>', unsafe_allow_html=True)
st.markdown('<p class="text-font">As more people see this project, it is my hope that more data is passed along to add. This project is just a start- the power of numbers and data have often been underlooked for years without proper understanding of its potential.</p>', unsafe_allow_html=True)
st.markdown('<p class="small-font">      ―Arnav Hiray, arnavhiray@gmail.com</p>', unsafe_allow_html=True)

with st.expander('Basic Statistics Understanding'):
    st.write("This section will go over the basic statistical concepts needed to understand this project. Don't worry- it is simple.")
    st.subheader('Pie Plots')
    st.write("Pie Charts are a type of graph using a circular style of visualization to show proprtions and percentages. Each 'slice' represents a sub-category and its proportion. Each slice sums up to 100% ")
    st.image("https://gradecalculator.mes.fm/img/memes/people-who-understand-pie-charts.JPG")
    st.subheader('Statistical Significance')
    st.write('Statistical significance implies a result of an experiment or analysis is unlikely to have ocurred randomly. Such significance is important because is shows that an external factor was inolvoved which led to this result.')
    st.write('In our context, when an experiment result is deemed statistically significant, that implies some external factors led to said proportions. Specifically, these results demonstrate racial inequality and prejudice which influenced the proportions.')
    st.write('Whenever a p-value (probability of the occurence randomly occurring) is less than .05, we will consider it as statistically signficant')
    st.subheader('Hypothesis Testing')
    st.write("Hypothesis Testing is a way to test given data to identify if you have statistically signficant results. While you do not need to worry about the details, we will be using hypothesis testing in this project.")
    st.subheader('Chi Square')
    st.write("The Chi-Square test is a form of hypothesis testing focused on comparing observed values within data with 'expected values'.")
    st.write("This test is extremely useful for our purpose. In a perfect world, proportions should be balanced and equal. However, if a certain proportion (such as proprtions of police shootings) are so far away from the ideal proportion that the test is statistically signifianct, this would demonstrate the works of institutional racism and inequality. ")
    st.image("https://i.ytimg.com/vi/1Ldl5Zfcm1Y/hqdefault.jpg")

with st.spinner(text='In Progress'):
    total = RacialData('1')
    total.generateData()
    totalData = total.returnData()

    white = RacialData('2')
    white.generateData()
    whiteData = white.returnData()

    black = RacialData('7')
    black.generateData()
    blackData = black.returnData()

    asian = RacialData('10')
    asian.generateData()
    asianData = asian.returnData()

    hispanic = RacialData('12')
    hispanic.generateData()
    hispanicData = hispanic.returnData()
    rL = [whiteData, blackData, asianData, hispanicData]
    families = [i['FAM']/totalData['FAM'] for i in rL]
    population = [i['FAM'] for i in rL]
    families = [i/sum(families) * 100 for i in families]
    poverty = [i['FAMPOV']/i['FAM'] *100 for i in rL]
    mylabels = ["White", "Black", "Asian", 'Hispanic']
    rL = [whiteData, blackData, asianData, hispanicData]

with st.expander('Demographics and Poverty'):
    st.write("This section is focused on understanding the distribution of poverty throughout the demographics. While there are many ethnicities and subgroups, for the purpose of processing and analysing data, there are four distinct subgroups to analyze: White, Black, Asian, and Hispanic. ")
    totalFig = px.pie(pd.DataFrame(population), values=population, names=mylabels, title='Demographic Distribution (In Thousands)')
    st.plotly_chart(totalFig)
    st.write("Now let's take a look at the distribution of poverty.")
    totalPov = px.pie(pd.DataFrame(poverty), values=[i['FAMPOV']/i['FAM'] for i in rL], names=mylabels, title='Percentage in Poverty per Demographic (In Thousands)')
    st.plotly_chart(totalPov)
    st.write("Now this most certainly does not look similar to the prior plot. The distribution of poverty is clearly not equal. To confirm this observation, we can use the Chi-Square test.")
    totalPoverty = [round(sum([i['FAMPOV'] for i in rL]) / sum([i['FAM'] for i in rL]) * i['FAM']) for i in rL]

    col1, col2, = st.columns(2)
    col1.write('Expected Number of Families in Poverty per Demographic (In Thousands')
    col1.write([i for i in totalPoverty] )
    col2.write('Actual Number of Families in Poverty per Demographic (In Thousands)')
    col2.write([i['FAMPOV']  for i in rL])
    st.write()
    st.write('NOTE: When viewing raw data, each category is attributed to a number as follows {0 : White People, 1 : Black People, 2 : Asian People, 3 : Hispanic People}')
    st.write('Just looking at the above raw data makes it clear that there is a huge disparity between the expected values if everything was equal vs the real values. There are nearly **14.4 million** more families of color and minorities in poverty than the expected value. This is FAMILIES, not people.')
    st.write('Chi-Square Test')
    st.write(chisquare([i['FAMPOV'] for i in rL], [round(sum([i['FAMPOV'] for i in rL]) / sum([i['FAM'] for i in rL]) * i['FAM']) for i in rL] ))
    st.write('The p-value is so small, the programming module is not able to display the value. The p-value is less than .001. This is considered an extremely statistically signfificant event.')
    st.write('The conclusion is evident:')
    st.markdown('<p class="big-font">Such a distribution is not randomly possible.</p>', unsafe_allow_html=True)
    st.write('In other words, natural processes did not create such disparities within the United States. Purposeful, discriminatory, and institutional action was necessary ')

with st.expander('Police Brutality- Shootings'):
    st.write('Perhaps the most controversial and public situation of injustice in the media is that of police brutality. While the stories of many are known around the country and the world, let us look at the numbers.')
    st.write("Let's first provide an example of how statistics can be misleading. The following is a chart of the racial distribution of all police shootings within the last 5 (approximate) years. ")
    totalPov = px.pie(values=[i['Total Shootings'] for i in rL], names=mylabels,title='Shootings Per Race- Proportionate to Total Shootings')
    st.plotly_chart(totalPov)
    st.write("This pie clearly shows that most shootings happen to white people... but is that really true?")
    st.write("This demonstrates how statistics can be deceitful and why it is crucial statisticians properly analyze data. The catch is that the POPULATION of white people within the United States is significantly higher than other groups. Therefore, sheer cases is not adequate to conduct analysis. Rather. let's analyse the rate of shootings per total group population")
    groupPov = px.pie(values=[(i['Total Shootings']) / i['FAM'] for i in rL], names=mylabels,title='Total Shooting by Race proportionate to US Family Population')
    st.plotly_chart(groupPov)
    st.write('The pie chart shows the true overall proportion. However, hovering over each slice shows the number of police shooting per person.')
    st.write('Once again, the data is substantially different than what it should be. Do not let the color deceive you, the purple slice now represents BLACK folk. Police shootings of black people acconut for 53.4% of all shootings. In a perfect world, the pie plot would have 4 equal 25% slices- indicating equal rates.')
    st.write('However, to confirm our results let us once again conduct a Chi-Square test')
    st.write(chisquare([(i['Total Shootings']) for i in rL],
                       [int((i['FAM'] * sum([i['Total Shootings'] for i in rL]) / sum(i['FAM'] for i in rL))) for i in
                        rL]))
    st.write('That is an extremely small p-value. I did some math to see how improbable this is.')st.markdown('<p class="big-font">You would win the lottery (1 in 13983816) TWO times and flip a coin heads 8 times in a row before such a distribution naturally happens.</p>', unsafe_allow_html=True)
    st.write('However, let us dive a little deeper into whether those shot were unarmed or it is still unclear.')
    totalPov = px.pie(
        values=[(i['Unarmed/Did Not Have Actual Weapon'] + i['Unclear']) / i['Total Shootings'] for i in rL],
        names=mylabels, title='Unarmed + Unclear')
    st.plotly_chart(totalPov)
    st.write(
        chisquare([(i['Unarmed/Did Not Have Actual Weapon'] + i['Unclear']) / i['Total Shootings'] * 100 for i in rL],
                  f_exp=[25, 25, 25, 25]))
    st.write('Perhaps to many, this result may be surprising. Statistically speaking, there is no conclusive evidence in regards to having statistically exceptional inconclusive/unclear evidence.')
with st.expander('Payroll and Distribution of Wealth'):
    st.write('Another complex issue to understand, yet where injustice is evident, is that of literacy and educational attainment.')
    st.write('To better analyze this, I analyzed the distribution of education for each subgroup (ages 25+) in 2020.  ')
    df = pd.read_csv('literacy.csv')
    df = df.iloc[df.index[6:]]
    allRace = df['Unnamed: 2'].dropna().reset_index()
    allRace = pd.DataFrame(allRace['Unnamed: 2'].replace(['-'], 0))
    educationLabel = ['Elementary or High school, no diploma', 'Less than 1 year, no diploma',
                      '1st-4th grade, no diploma', '5th-6th grade, no diploma', '7th-8th grade, no diploma',
                      '9th grade, no diploma', '10th grade, no diploma', '11th grade, no diploma',
                      '12th grade, no diploma', 'Less than 1 year, GED', '5th-6th grade, GED', '7th-8th grade, GED',
                      '9th grade, GED', '10th grade, GED', '11th grade, GED', '12th grade, GED', 'High school diploma',
                      'Less than 1 year college, no degree', 'One year of college, no degree',
                      'Two years of college, no degree', 'Three years of college, no degree',
                      'Four or more years of college, no degree', "Less than 1 year college, vocational/associate's",
                      "One year of college, vocational/associate's", "Two years of college, vocational/associate's",
                      "Three years of college, vocational/associate's",
                      "Four or more years of college, vocational/associate's",
                      "Less than 1 year college, academic/associate's", "One year of college, academic/associate's",
                      "Two years of college, academic/associate's", "Three years of college, academic/associate's",
                      "Four or more years of college, academic/associate's", "Bachelor's degree", "Master's degree",
                      "Professional degree", "Doctorate degree"]
    payroll = px.pie(values=allRace['Unnamed: 2'], names=educationLabel, title='Literacy Distribution (Everyone in the United States)')
    payroll.update_traces(textposition='inside')
    payroll.update_layout(uniformtext_minsize=8)
    st.plotly_chart(payroll)
    st.write("Now let's look at the distribution of education within each subgroup.")
    white = df['Unnamed: 14'].dropna().reset_index()
    white = pd.DataFrame(white['Unnamed: 14'].replace(['-'], 0))
    payroll = px.pie(values=white['Unnamed: 14'], names=educationLabel, title='Literacy Among White People', color_discrete_sequence=px.colors.sequential.Turbo)
    payroll.update_traces(textposition='inside')
    payroll.update_layout(uniformtext_minsize=8)

    black = df['Unnamed: 18'].dropna().reset_index()
    black = pd.DataFrame(black['Unnamed: 18'].replace(['-'], 0))
    educationLabel = ['Elementary or High school, no diploma', 'Less than 1 year, no diploma',
                      '1st-4th grade, no diploma', '5th-6th grade, no diploma', '7th-8th grade, no diploma',
                      '9th grade, no diploma', '10th grade, no diploma', '11th grade, no diploma',
                      '12th grade, no diploma', 'Less than 1 year, GED', '5th-6th grade, GED', '7th-8th grade, GED',
                      '9th grade, GED', '10th grade, GED', '11th grade, GED', '12th grade, GED', 'High school diploma',
                      'Less than 1 year college, no degree', 'One year of college, no degree',
                      'Two years of college, no degree', 'Three years of college, no degree',
                      'Four or more years of college, no degree', "Less than 1 year college, vocational/associate's",
                      "One year of college, vocational/associate's", "Two years of college, vocational/associate's",
                      "Three years of college, vocational/associate's",
                      "Four or more years of college, vocational/associate's",
                      "Less than 1 year college, academic/associate's", "One year of college, academic/associate's",
                      "Two years of college, academic/associate's", "Three years of college, academic/associate's",
                      "Four or more years of college, academic/associate's", "Bachelor's degree", "Master's degree",
                      "Professional degree", "Doctorate degree"]
    payroll = px.pie(values=black['Unnamed: 18'], names=educationLabel, title='Literacy Among Black People', color_discrete_sequence=px.colors.sequential.Turbo)
    payroll.update_traces(textposition='inside')
    payroll.update_layout(uniformtext_minsize=8)
    st.plotly_chart(payroll)
    asian = df['Unnamed: 20'].dropna().reset_index()
    asian = pd.DataFrame(asian['Unnamed: 20'].replace(['-'], 0))
    educationLabel = ['Elementary or High school, no diploma', 'Less than 1 year, no diploma',
                      '1st-4th grade, no diploma', '5th-6th grade, no diploma', '7th-8th grade, no diploma',
                      '9th grade, no diploma', '10th grade, no diploma', '11th grade, no diploma',
                      '12th grade, no diploma', 'Less than 1 year, GED', '5th-6th grade, GED', '7th-8th grade, GED',
                      '9th grade, GED', '10th grade, GED', '11th grade, GED', '12th grade, GED', 'High school diploma',
                      'Less than 1 year college, no degree', 'One year of college, no degree',
                      'Two years of college, no degree', 'Three years of college, no degree',
                      'Four or more years of college, no degree', "Less than 1 year college, vocational/associate's",
                      "One year of college, vocational/associate's", "Two years of college, vocational/associate's",
                      "Three years of college, vocational/associate's",
                      "Four or more years of college, vocational/associate's",
                      "Less than 1 year college, academic/associate's", "One year of college, academic/associate's",
                      "Two years of college, academic/associate's", "Three years of college, academic/associate's",
                      "Four or more years of college, academic/associate's", "Bachelor's degree", "Master's degree",
                      "Professional degree", "Doctorate degree"]
    payroll = px.pie(values=asian['Unnamed: 20'], names=educationLabel, title='Literacy among Asian People', color_discrete_sequence=px.colors.sequential.Turbo)
    payroll.update_traces(textposition='inside')
    payroll.update_layout(uniformtext_minsize=8)
    st.plotly_chart(payroll)
    hispanic = df['Unnamed: 22'].dropna().reset_index()
    hispanic = pd.DataFrame(hispanic['Unnamed: 22'].replace(['-'], 0))
    educationLabel = ['Elementary or High school, no diploma', 'Less than 1 year, no diploma',
                      '1st-4th grade, no diploma', '5th-6th grade, no diploma', '7th-8th grade, no diploma',
                      '9th grade, no diploma', '10th grade, no diploma', '11th grade, no diploma',
                      '12th grade, no diploma', 'Less than 1 year, GED', '5th-6th grade, GED', '7th-8th grade, GED',
                      '9th grade, GED', '10th grade, GED', '11th grade, GED', '12th grade, GED', 'High school diploma',
                      'Less than 1 year college, no degree', 'One year of college, no degree',
                      'Two years of college, no degree', 'Three years of college, no degree',
                      'Four or more years of college, no degree', "Less than 1 year college, vocational/associate's",
                      "One year of college, vocational/associate's", "Two years of college, vocational/associate's",
                      "Three years of college, vocational/associate's",
                      "Four or more years of college, vocational/associate's",
                      "Less than 1 year college, academic/associate's", "One year of college, academic/associate's",
                      "Two years of college, academic/associate's", "Three years of college, academic/associate's",
                      "Four or more years of college, academic/associate's", "Bachelor's degree", "Master's degree",
                      "Professional degree", "Doctorate degree"]
    payroll = px.pie(values=hispanic['Unnamed: 22'], names=educationLabel, title='Literacy among Hispanic People',
                     color_discrete_sequence=px.colors.sequential.Turbo)
    payroll.update_traces(textposition='inside')
    payroll.update_layout(uniformtext_minsize=8)
    st.plotly_chart(payroll)
    st.write('While a Chi-Square test would be effective at generating conclusive results, the different distributions throughout the graph show different influences affecting education. Some of these factors may be cultural; however, educational disparities in regions where certain groups live as well as the general lack of resources contributes to the differences.')

st.markdown('<p class="text-font"> Think over any of the statistics you read or saw through this project. While we hear personal stories and individuals who are unjustly affected, it is key to understand the big picture in order to truly create reform on the institutional level. </p>', unsafe_allow_html=True)
with st.expander('Information and Content'):
    st.write('All data was collected from the US Census and can be found at https://www.census.gov/data/developers.html. All data used has been collected and reviewed in the last 5 years, assuring recency.')




