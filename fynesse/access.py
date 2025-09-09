"""
Access module for the fynesse framework.

This module handles data access functionality including:
- Data loading from various sources (web, local files, databases)
- Legal compliance (intellectual property, privacy rights)
- Ethical considerations for data usage
- Error handling for access issues

Legal and ethical considerations are paramount in data access.
Ensure compliance with e.g. .GDPR, intellectual property laws, and ethical guidelines.

Best Practice on Implementation
===============================

1. BASIC ERROR HANDLING:
   - Use try/except blocks to catch common errors
   - Provide helpful error messages for debugging
   - Log important events for troubleshooting

2. WHERE TO ADD ERROR HANDLING:
   - File not found errors when loading data
   - Network errors when downloading from web
   - Permission errors when accessing files
   - Data format errors when parsing files

3. SIMPLE LOGGING:
   - Use print() statements for basic logging
   - Log when operations start and complete
   - Log errors with context information
   - Log data summary information

4. EXAMPLE PATTERNS:
   
   Basic error handling:
   try:
       df = pd.read_csv('data.csv')
   except FileNotFoundError:
       print("Error: Could not find data.csv file")
       return None
   
   With logging:
   print("Loading data from data.csv...")
   try:
       df = pd.read_csv('data.csv')
       print(f"Successfully loaded {len(df)} rows of data")
       return df
   except FileNotFoundError:
       print("Error: Could not find data.csv file")
       return None
"""

from typing import Any, Union
import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd
import logging
# Set up basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def data() -> Union[pd.DataFrame, None]:
    """
    Read the data from the web or local file, returning structured format such as a data frame.

    IMPLEMENTATION GUIDE
    ====================

    1. REPLACE THIS FUNCTION WITH YOUR ACTUAL DATA LOADING CODE:
       - Load data from your specific sources
       - Handle common errors (file not found, network issues)
       - Validate that data loaded correctly
       - Return the data in a useful format

    2. ADD ERROR HANDLING:
       - Use try/except blocks for file operations
       - Check if data is empty or corrupted
       - Provide helpful error messages

    3. ADD BASIC LOGGING:
       - Log when you start loading data
       - Log success with data summary
       - Log errors with context

    4. EXAMPLE IMPLEMENTATION:
       try:
           print("Loading data from data.csv...")
           df = pd.read_csv('data.csv')
           print(f"Successfully loaded {len(df)} rows, {len(df.columns)} columns")
           return df
       except FileNotFoundError:
           print("Error: data.csv file not found")
           return None
       except Exception as e:
           print(f"Error loading data: {e}")
           return None

    Returns:
        DataFrame or other structured data format
    """
    logger.info("Starting data access operation")

    try:
        # IMPLEMENTATION: Replace this with your actual data loading code
        # Example: Load data from a CSV file
        logger.info("Loading data from data.csv")
        df = pd.read_csv("data.csv")

        # Basic validation
        if df.empty:
            logger.warning("Loaded data is empty")
            return None

        logger.info(
            f"Successfully loaded data: {len(df)} rows, {len(df.columns)} columns"
        )
        return df

    except FileNotFoundError:
        logger.error("Data file not found: data.csv")
        print("Error: Could not find data.csv file. Please check the file path.")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading data: {e}")
        print(f"Error loading data: {e}")
        return None
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
    lon_degree_size = box_size_km / 111.0 

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
