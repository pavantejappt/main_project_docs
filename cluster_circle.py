from flask import Flask, render_template, request
import folium
from folium.plugins import MarkerCluster
from sklearn.cluster import KMeans
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        lat = request.form['lat']
        lon = request.form['lon']
        # perform clustering using KMeans
        kmeans = KMeans(n_clusters=7, random_state=42).fit(X)
        cluster = kmeans.predict([[lat, lon]])[0]
        # generate map with cluster centroids
        centroid = kmeans.cluster_centers_
        map = folium.Map(location=[lat, lon], zoom_start=15)
        for point in range(0, len(centroid)):
            color = 'blue' if point == cluster else 'green' # set the color of the circle based on the cluster
            number = str(point+1) # set the number of the circle
            folium.Circle(
                location=centroid[point],
                radius=1000, # set the radius of the circle in meters
                popup=folium.Popup(str(centroid[point])),
                fill=True,
                fill_color=color,
                fill_opacity=0.5,
                color=None,
                # add a div icon with the cluster number
                tooltip='Cluster ' + number,
                icon=folium.features.DivIcon(
                    icon_size=(10,10),
                    icon_anchor=(5,5),
                    html='<div style="font-size: 8pt; color : black">'+number+'</div>'
                )
            ).add_to(map)
        folium.Marker( # add a marker for the predicted point
            location=[lat, lon],
            popup='Predicted point',
            icon=folium.Icon(icon='star', color='red')
        ).add_to(map)
        map = map._repr_html_()
        return render_template('index.html', lat=lat, lon=lon, cluster=cluster, map=map)
    else:
        return render_template('index.html')

if __name__=="__main__":
    data = pd.read_csv('/config/workspace/Dataset/uber-raw-data-sep14.csv')
    X = data[['Lat', 'Lon']]
    app.run(host="0.0.0.0")
