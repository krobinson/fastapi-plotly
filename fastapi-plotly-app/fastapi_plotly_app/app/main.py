from fastapi import FastAPI
import uvicorn
import plotly.express as px
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union

app = FastAPI(
    title='World Metrics DS API',
    description='Visualize world metrics from Gapminder data',
    docs_url='/'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dataframe = px.data.gapminder().rename(columns={
    'year': 'Year', 
    'lifeExp': 'Life Expectancy', 
    'pop': 'Population', 
    'gdpPercap': 'GDP Per Capita'
})

@app.get('/api/worldviz')
async def worldviz(metric, country):
    """
    Visualize world metrics from Gapminder data

    ### Query Parameters
    - `metric`: 'Life Expectancy', 'Population', or 'GDP Per Capita'
    - `country`: [country name](https://www.gapminder.org/data/geo/), case sensitive

    ### Response
    JSON string to render with react-plotly.js
    """
    subset = dataframe[dataframe.country == country]
    fig = px.line(subset, x='Year', y=metric, title=f'{metric} in {country}')
    return fig.to_json()

if __name__ == '__main__':
    uvicorn.run(app)