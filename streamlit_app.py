"""
Lehigh County 2024 Election Results
https://www.lehighcounty.org/departments/voter-registration/election-results
"""

import string
import re

import streamlit as st
import pandas as pd

# TODO: Add Northampton County 2024 Election Results
st.title("Lehigh County 2024 Election Results")

# TODO: Add app testing https://docs.streamlit.io/develop/concepts/app-testing/get-started

@st.cache_data
def load_data()->pd.DataFrame:
    """
    Load raw precinct level results

    Returns
    -------
    pd.DataFrame

    """

    # Row per precinct per candidate/choice per race
    data = pd.read_csv("https://www.livevoterturnout.com/ENR/lehighpaenr/8/Precincts_8.csv", skiprows=2)

    # TODO: Switch the relevent columnts to integers to run sums and sorts

    return data


raw_data = load_data()


municipalities = []
for precinct in list(raw_data["Precinct"]):
    # TODO: Add striping whitespaces and punctuation to regex pattern
    municipalities.append(
        re.match(r"\D+", precinct)
        .group(0)
        .rstrip(string.whitespace)
        .rstrip(string.punctuation)
    )

raw_data["Municipality"] = municipalities


# TODO: Display a map with with a scatterplot overlaid onto it using st.map: https://docs.streamlit.io/develop/api-reference/charts/st.map
st.image(
    "static/Lehigh-Commissioner-Districts.png",
    caption="Image credit: https://lehighdemocrats.org/faq-lehigh-county-government/",
)


contests = [
    "Presidential Electors",
    "United States Senator",
    "Attorney General",
    "Auditor General",
    "State Treasurer",
    "Representative in Congress",
    "Representative in the General Assembly",
]


st.subheader("Grouped Municipal Level Data")
# TODO: Add trends from 2016 to 2020 to 2024
# TODO: Did Democrats win any contests in munis that Trump won?
st.text("Sort columns by clicking on their headers")
muni_to_filter = st.selectbox("Pick one municipality", sorted(set(municipalities)))
contest_to_filter = st.selectbox("Pick one contest", contests)

data = raw_data[
    (raw_data["Municipality"] == muni_to_filter)
    & raw_data["Contest Name"].str.contains(contest_to_filter)
]

agg_data = (
    data.groupby(["Municipality", "Contest Name", "Candidate Name"])
    .sum("Votes")
    .reset_index()
)

agg_data['Percentage'] = [100*(votes / sum(agg_data['Votes'])) for votes in agg_data['Votes']]

st.dataframe(agg_data.sort_values('Votes',ascending=False), use_container_width=True, hide_index=True)

# TODO: Group precincts by school districts

st.subheader("Raw Precinct Level Data")
st.text("Sort columns by clicking on their headers")
st.download_button("Download file", raw_data.to_csv())
st.dataframe(raw_data, use_container_width=True)
