#!/usr/bin/python3.10
# coding=utf-8
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
import sklearn.cluster 
import numpy as np
from sklearn.cluster import KMeans
from shapely.geometry import MultiPoint

def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """ Konvertovani dataframe do geopandas.GeoDataFrame se spravnym kodovani"""
    # Remove rows where position is not known
    df = df[df["d"].notna() & df["e"].notna()]

    # Change type of datetime field
    df["p2a"] = pd.to_datetime(df["p2a"])

    return geopandas.GeoDataFrame(
        df,
        geometry=geopandas.points_from_xy(df['d'], df['e']),
        crs='epsg:5514'
    )

def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    """ Vykresleni grafu s nehodami  """
    # Transform to WebMercator
    gdf = gdf.to_crs(epsg=3857)

    # Filter data for the selected region and by cause (accidents caused by wildlife)
    data = gdf[(gdf["region"] == "ZLK") & (gdf["p10"] == 4)]

    # Filter data for years 2021 and 2022
    data_2021 = data[data["p2a"].dt.year == 2021]
    data_2022 = data[data["p2a"].dt.year == 2022]
    data_2022_bounds = data_2021.total_bounds
    # data_2022.to_csv("data_2022")
    # data_2021.to_csv("data_2021")

    # Create subplots
    fig, ax = plt.subplots(1, 2, figsize=(13, 8))

    # Plot 2021 data
    ax[0].set_title('ZLK kraj (2021)')
    data_2021.plot(ax=ax[0], color='blue', markersize=5)
    ctx.add_basemap(ax[0], source=ctx.providers.OpenStreetMap.Mapnik)

    # Plot 2022 data
    ax[1].set_title('ZLK kraj (2022)')
    ax[1].set_xlim(left=data_2022_bounds[0], right=data_2022_bounds[2])
    ax[1].set_ylim(bottom=data_2022_bounds[1], top=data_2022_bounds[3])
    data_2022.plot(ax=ax[1], color='red', markersize=5)
    ctx.add_basemap(ax[1], source=ctx.providers.OpenStreetMap.Mapnik)

    # Turn off axis for both plots
    for a in ax:
        a.set_axis_off()

    plt.tight_layout()

    # Save the figure if a file location is provided
    if fig_location:
        plt.savefig(fig_location)

    # Show the figure if show_figure is True
    if show_figure:
        plt.show()

def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """
    # Transform to WebMercator
    gdf = gdf.to_crs(epsg=3857)

    # Filter data for a specific region and significant alcohol involvement
    data = gdf[(gdf["region"] == "ZLK") & (gdf["p11"] >= 4)].copy()
    # Filter data for year 2021
    data_2021 = data[data["p2a"].dt.year == 2021].copy()
    # Calculate bounds for the 2021 data
    data_2021_bounds = data_2021.total_bounds

    # Calculate padding
    padding_factor = 0.2  # Adjust this value for more or less padding
    x_padding = (padding_factor * (data_2021_bounds[2] - data_2021_bounds[0]))
    y_padding = (padding_factor * (data_2021_bounds[3] - data_2021_bounds[1]))

    # Use the bounds of the 2021 data for clustering
    coords = np.dstack([data.geometry.x, data.geometry.y]).reshape(-1, 2)
    db = sklearn.cluster.AgglomerativeClustering(n_clusters=20).fit(coords)
    data["cluster"] = db.labels_
    data = data.dissolve(by="cluster", aggfunc={"p11": "count"})

    # Create a GeoDataFrame for clusters
    fig, ax = plt.subplots(figsize=(10, 8))
    # Apply the padded bounds to the axis
    ax.set_xlim(left=data_2021_bounds[0] - x_padding, right=data_2021_bounds[2] + x_padding)
    ax.set_ylim(bottom=data_2021_bounds[1] - y_padding, top=data_2021_bounds[3] + y_padding)
    ax.set_axis_off()

    # Plot convex hulls for each cluster
    for cluster_label, cluster_data in data.iterrows():
        convex_hull_polygon = cluster_data.geometry.convex_hull
        geopandas.GeoSeries(convex_hull_polygon).plot(ax=ax, color='grey', alpha=0.7, edgecolor='grey')

    # Plot the points
    data.plot(ax=ax, markersize=2, column="p11", legend=True, legend_kwds={"orientation": "horizontal", "label": "Počet nehod v úseku", "shrink": 0.8,})

    # Add basemap
    ctx.add_basemap(ax, crs=data.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

    # Add title and legend
    ax.set_title("Nehody v ZLK kraji s významnou mírou alkoholu")
    plt.tight_layout()

    if fig_location:
        plt.savefig(fig_location)
    if show_figure:
        plt.show()

if __name__ == "__main__":
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf, "geo1.png", True)
    plot_cluster(gdf, "geo2.png", True)