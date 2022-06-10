import requests as rq
import pandas as pd

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
            f'https://api.census.gov/data/timeseries/poverty/histpov2?get={query}&time=2020&RACE={self.race}').json()

    def health_insurance(self):
        return rq.get(
            f'https://api.census.gov/data/timeseries/healthins/sahie?get=NIC_PT,NUI_PT,NAME&for=us:*&time=2017&RACECAT={self.healthquery}').json()

    @st.cache
    def generateData(self):
        stats = ['FAM', 'FAMPOV', 'FEMHH', 'FEMHHPOV', 'POP', 'POV']
        self.data['Annual Payroll'] = self.businessData()[1][0]
        self.policeShootings()
        for i in stats:
            pover = self.poverty(i)
            self.data[pover[0][0]] = int(pover[1][0])

    def businessData(self):
        return rq.get(
            f'https://api.census.gov/data/2016/ase/csa?get=PAYANN,RCPPDEMP&for=us:*&RACE_GROUP={self.businessquery}').json()

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
import streamlit as st