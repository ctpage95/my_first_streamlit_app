from turtle import color
import streamlit as st
import random
import altair as alt
import numpy as np
import pandas as pd

st.header('Homework 1')

st.markdown(
"**QUESTION 1**: In previous homeworks you created dataframes from random numbers.\n"
"Create a datframe where the x axis limit is 100 and the y values are random values.\n"
"Print the dataframe you create and use the following code block to help get you started"
)

st.code(
''' 
x_limit = 101

# List of values from 0 to 100 each value being 1 greater than the last
x_axis = np.arange(0, x_limit)

# Create a random array of data that we will use for our y values
y_data = np.random.randint(0, 1000, 101)

df = pd.DataFrame({'x': x_axis,'y': y_data})

st.write(df)''',language='python')

x_limit = 101

# List of values from 0 to 100 each value being 1 greater than the last
x_axis = np.arange(0, x_limit)

# Create a random array of data that we will use for our y values
y_data = np.random.randint(0, 1000, 101)

df = pd.DataFrame({'x': x_axis,'y': y_data})

st.write(df)



st.markdown(
"**QUESTION 2**: Using the dataframe you just created, create a basic scatterplot and Print it.\n"
"Use the following code block to help get you started."
)

st.code(
''' 
scatter = alt.Chart(df).mark_point().encode(x="x", y="y")

st.altair_chart(scatter, use_container_width=True)''',language='python')
scatter = alt.Chart(df).mark_point().encode(x="x", y="y")
st.altair_chart(scatter, use_container_width=True)




st.markdown(
"**QUESTION 3**: Lets make some edits to the chart by reading the documentation on Altair.\n"
"https://docs.streamlit.io/library/api-reference/charts/st.altair_chart.  "
"Make 5 changes to the graph, document the 5 changes you made using st.markdown(), and print the new scatterplot.  \n"
"To make the bullet points and learn more about st.markdown() refer to the following discussion.\n"
"https://discuss.streamlit.io/t/how-to-indent-bullet-point-list-items/28594/3"
)


st.code(
'''
    z = np.random.randint(1, 10, 101)
df = pd.DataFrame({'x': x_axis,'y': y_data, 'z': z})
df['Category'] = np.where(df['y']>=500, 'Category A', 'Category B')

selection = alt.selection_multi(fields=['Category'], bind='legend')
scatter2 = alt.Chart(df).mark_point().encode(
    x=alt.X('x', axis=alt.Axis(title='New X Axis'), 
        scale=alt.Scale(domain=(-10, 110))),
    y=alt.Y('y', axis=alt.Axis(title='New Y Axis'),
        scale=alt.Scale(domain=(-100, 1100))),
    color=alt.Color('Category', 
    scale=alt.Scale(scheme='dark2')),
    size='z',
    shape='Category',
    opacity= alt.condition(selection, alt.value(1), alt.value(0))
).add_selection(
    selection
).properties(
    title='Sample Title'
)
st.altair_chart(scatter2, use_container_width=True)
)
''', language='python')


z = np.random.randint(1, 10, 101)
df = pd.DataFrame({'x': x_axis,'y': y_data, 'z': z})
df['Category'] = np.where(df['y']>=500, 'Category A', 'Category B')

selection = alt.selection_multi(fields=['Category'], bind='legend')
scatter2 = alt.Chart(df).mark_point().encode(
    x=alt.X('x', axis=alt.Axis(title='New X Axis'), 
        scale=alt.Scale(domain=(-10, 110))),
    y=alt.Y('y', axis=alt.Axis(title='New Y Axis'),
        scale=alt.Scale(domain=(-100, 1100))),
    color=alt.Color('Category', 
        scale=alt.Scale(scheme='dark2')),
    size='z',
    shape='Category',
    opacity= alt.condition(selection, alt.value(1), alt.value(0))
).add_selection(
    selection
).properties(
    title='Sample Title'
)
st.altair_chart(scatter2, use_container_width=True)

st.markdown("The five changes I made were.....")
st.markdown("""
The 5 changes I made were:
- Change 1: Created two categories: Category A is y values >= 500, y values < 500 are Category B with color scheme
- Change 2: Created a z variables to adjust size
- Change 3: Changed the shape depending on category
- Change 4: Added toggleable filter for category to click and choose category to display
- Change 5: Changed the x and the y axis names and limits from the defaults
""")



st.markdown(
"**QUESTION 4**: Explore on your own!  Go visit https://altair-viz.github.io/gallery/index.html.\n "
"Pick a random visual, make two visual changes to it, document those changes, and plot the visual.  \n"
"You may need to pip install in our terminal for example pip install vega_datasets "
)

st.markdown(
"""
The 2 changes I made were:
- Change 1: Added a color scheme to the count scale to better visualize high/low counts
- Change 2: Slider filter added to be able to edit the range you want to look at
"""
)

st.markdown(
'''
## Cannot get the JSON file that feeds in the states background map in correctly
'''
)
airports = pd.read_csv("airports.csv")
states = alt.topo_feature("states.json", feature='states')

# US states background
background = alt.Chart(states).mark_geoshape(
    fill='lightgray',
    stroke='white'
).encode(
).properties(
    width=500,
    height=300
).project('albersUsa')

slider = alt.binding_range(min=0, max=300, step=5, name='cutoff: ')
selector = alt.selection_single(name="SelectorName", fields=['count'],
                                bind=slider, init={'count': 50})

points = alt.Chart(airports).transform_aggregate(
    latitude='mean(latitude)',
    longitude='mean(longitude)',
    count='count()',
    groupby=['state']
).mark_circle().encode(
    longitude='longitude:Q',
    latitude='latitude:Q',
    size=alt.Size('count:Q', title='Number of Airports'),
    color=alt.Color('count:Q',
            scale=alt.Scale(scheme="blueorange")),
    #opacity= alt.condition(
    #    "alt.datum['count:Q'] <= selector.cutoff",
    #    alt.value(1), alt.value(0)),
    tooltip=['state:N','count:Q']
).properties(
    title='Number of airports in US'
).add_selection(
    selector
).transform_filter(
    alt.datum.count < selector.count
)

background + points
