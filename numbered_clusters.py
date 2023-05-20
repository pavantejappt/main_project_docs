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
        marker_cluster = MarkerCluster().add_to(map)
        pt=-1
        for point in range(0, len(centroid)):
            color = 'blue' if point == cluster else 'green' # set the color of the marker based on the cluster
            number = str(pt+1) # set the number of the marker
            pt+=1
            folium.Marker(
                location=centroid[point],
                popup=folium.Popup(str(centroid[point])),
                icon=folium.DivIcon(
                    html=f'<div style="font-size: 12pt; font-weight: bold; color: white; background-color: {color}; border-radius: 50%; width: 25px; height: 25px; display: flex; justify-content: center; align-items: center;">{number}</div>',
                    icon_size=(30, 30)
                )
            ).add_to(marker_cluster)
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
