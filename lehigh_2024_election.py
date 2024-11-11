"""
Lehigh County 2024 Election Results
https://www.lehighcounty.org/departments/voter-registration/election-results
"""

import string
import re

import streamlit as st
import pandas as pd

st.title("Lehigh County 2024 Election Results")

@st.cache_data
def load_data():
	"""
	Load raw precinct level results from downloaded CSV

	Returns
	-------

	"""

	data = pd.read_csv("Precincts_8.csv")

	municipalities = []
	for precinct in list(data['Precinct']):
		#TODO: Add striping whitespaces and punctuation to regex pattern
		municipalities.append(re.match(r"\D+",precinct).group(0).rstrip(string.whitespace).rstrip(string.punctuation))

	data['Municipality'] = municipalities

	return data, municipalities

raw_data, municipalities=load_data()

contests = ["Presidential Electors", "United States Senator", "Attorney General", 
			"Auditor General", "State Treasurer", "Representative in Congress", "Representative in the General Assembly"]


st.image("static/Lehigh-Commissioner-Districts.png", caption="Image credit: https://lehighdemocrats.org/faq-lehigh-county-government/")


#TODO Add grouped county level data and voter turnout data

st.subheader("Grouped Municipal Level Data")
st.text("Sort columns by clicking on their headers")
muni_to_filter = st.selectbox("Pick one municipality", set(municipalities))
contest_to_filter = st.selectbox("Pick one contest", contests)
data = raw_data[(raw_data['Municipality']==muni_to_filter) & raw_data['Contest Name'].str.contains(contest_to_filter)]
agg_data = data.groupby(['Municipality', 'Contest Name', 'Candidate Name']).sum('Votes').reset_index()
st.dataframe(agg_data, use_container_width=True, hide_index = True)
st.bar_chart(agg_data, x = "Candidate Name", y="Votes", horizontal=True)

st.subheader('Raw Precinct Level Data')
st.text("Sort columns by clicking on their headers")
st.download_button("Download file", raw_data.to_csv())
st.dataframe(raw_data, use_container_width=True)

