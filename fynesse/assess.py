from typing import Any, Union
import pandas as pd
import logging

from .config import *
from . import access

# Set up logging
logger = logging.getLogger(__name__)

"""These are the types of import we might expect in this file
import pandas
import bokeh
import seaborn
import matplotlib.pyplot as plt
import sklearn.decomposition as decomposition
import sklearn.feature_extraction"""

"""Place commands in this file to assess the data you have downloaded.
How are missing values encoded, how are outliers encoded? What do columns represent,
makes rure they are correctly labeled. How is the data indexed. Crete visualisation
routines to assess the data (e.g. in bokeh). Ensure that date formats are correct
and correctly timezoned."""


def data() -> Union[pd.DataFrame, Any]:
    """
    Load the data from access and ensure missing values are correctly encoded as well as
    indices correct, column names informative, date and times correctly formatted.
    Return a structured data structure such as a data frame.

    IMPLEMENTATION GUIDE FOR STUDENTS:
    ==================================

    1. REPLACE THIS FUNCTION WITH YOUR DATA ASSESSMENT CODE:
       - Load data using the access module
       - Check for missing values and handle them appropriately
       - Validate data types and formats
       - Clean and prepare data for analysis

    2. ADD ERROR HANDLING:
       - Handle cases where access.data() returns None
       - Check for data quality issues
       - Validate data structure and content

    3. ADD BASIC LOGGING:
       - Log data quality issues found
       - Log cleaning operations performed
       - Log final data summary

    4. EXAMPLE IMPLEMENTATION:
       df = access.data()
       if df is None:
           print("Error: No data available from access module")
           return None

       print(f"Assessing data quality for {len(df)} rows...")
       # Your data assessment code here
       return df
    """
    logger.info("Starting data assessment")

    # Load data from access module
    df = access.data()

    # Check if data was loaded successfully
    if df is None:
        logger.error("No data available from access module")
        print("Error: Could not load data from access module")
        return None

    logger.info(f"Assessing data quality for {len(df)} rows, {len(df.columns)} columns")

    try:
        # STUDENT IMPLEMENTATION: Add your data assessment code here

        # Example: Check for missing values
        missing_counts = df.isnull().sum()
        if missing_counts.sum() > 0:
            logger.info(f"Found missing values: {missing_counts.to_dict()}")
            print(f"Missing values found: {missing_counts.sum()} total")

        # Example: Check data types
        logger.info(f"Data types: {df.dtypes.to_dict()}")

        # Example: Basic data cleaning (students should customize this)
        # Remove completely empty rows
        df_cleaned = df.dropna(how="all")
        if len(df_cleaned) < len(df):
            logger.info(f"Removed {len(df) - len(df_cleaned)} completely empty rows")

        logger.info(f"Data assessment completed. Final shape: {df_cleaned.shape}")
        return df_cleaned

    except Exception as e:
        logger.error(f"Error during data assessment: {e}")
        print(f"Error assessing data: {e}")
        return None


def query(data: Union[pd.DataFrame, Any]) -> str:
    """Request user input for some aspect of the data."""
    raise NotImplementedError


def view(data: Union[pd.DataFrame, Any]) -> None:
    """Provide a view of the data that allows the user to verify some aspect of its quality."""
    raise NotImplementedError


def labelled(data: Union[pd.DataFrame, Any]) -> Union[pd.DataFrame, Any]:
    """Provide a labelled set of data ready for supervised learning."""
    raise NotImplementedError
import osmnx as ox
import matplotlib.pyplot as plt
import warnings
import math

warnings.filterwarnings("ignore", category=FutureWarning, module='osmnx')

def plot_city_map(place_name, latitude, longitude, box_size_km=2, tags=None):
    """
    Visualizes the street network, buildings, and points of interest for a given location.

    Parameters
    ----------
    place_name : str
        The name of the place to visualize.
    latitude : float
        Latitude of the center point.
    longitude : float
        Longitude of the center point.
    box_size_km : float
        Size of the bounding box in kilometers.
    tags : dict
        A dictionary of OpenStreetMap tags to include as points of interest.
    """
    # Construct bbox from lat/lon and box_size
    lat_degree_size = box_size_km / 111.0
    lon_degree_size = box_size_km / (111.0 * math.cos(math.radians(latitude)))

    north = latitude + lat_degree_size / 2
    south = latitude - lat_degree_size / 2
    west = longitude - lon_degree_size / 2
    east = longitude + lon_degree_size / 2
    bbox = (west, south, east, north)

    try:
        # Get graph from location
        graph = ox.graph_from_bbox(bbox, network_type='drive') # Specify network_type
        # City area
        area = ox.geocode_to_gdf(place_name)
        # Street network
        nodes, edges = ox.graph_to_gdfs(graph)
        # Buildings
        buildings = ox.features_from_bbox(bbox, tags={"building": True})
        # POIs
        if tags is None:
            # Use default tags if none are provided
            tags = {
                "amenity": True,
                "buildings": True,
                "historic": True,
                "leisure": True,
                "shop": True,
                "tourism": True,
                "religion": True,
                "memorial": True
            }
        pois = ox.features_from_bbox(bbox, tags=tags)

        fig, ax = plt.subplots(figsize=(8,8))
        area.plot(ax=ax, color="tan", alpha=0.5)
        buildings.plot(ax=ax, facecolor="gray", edgecolor="gray")
        edges.plot(ax=ax, linewidth=1, edgecolor="black", alpha=0.3)
        nodes.plot(ax=ax, color="black", markersize=1, alpha=0.3)
        if not pois.empty:
            pois.plot(ax=ax, color="green", markersize=5, alpha=1)
        ax.set_xlim(west, east)
        ax.set_ylim(south, north)
        ax.set_title(place_name, fontsize=14)
        plt.show()
    except Exception as e:
        print(f"An error occurred while plotting the map: {e}")
        print(f"Could not plot map for {place_name} at ({latitude}, {longitude}) with box size {box_size_km} km.")
