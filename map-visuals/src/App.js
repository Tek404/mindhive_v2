import React, { useState, useEffect } from "react";
import "./styles.css";
import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer, Marker, Popup, Circle, FeatureGroup } from "react-leaflet";
import MarkerClusterGroup from "react-leaflet-cluster";
import { Icon, divIcon, point } from "leaflet";
import L from "leaflet";

const customIcon = new Icon({
  iconUrl: require("./icons/store.png"),
  iconSize: [38, 38]
});

const createClusterCustomIcon = function (cluster) {
  return new divIcon({
    html: `<span class="cluster-icon">${cluster.getChildCount()}</span>`,
    className: "custom-marker-cluster",
    iconSize: point(33, 33, true)
  });
};

const circleOptions = {
  color: 'red',
  fillColor: 'red',
  fillOpacity: 0.2,
};

export default function App() {
  const [markers, setMarkers] = useState([]);

  useEffect(() => {
    // Fetch data from the backend API
    fetch("http://127.0.0.1:8000/api/outlets/")
      .then((response) => response.json())
      .then((data) => {
        // Process the data and update the markers state
        const updatedMarkers = data.map((item) => ({
          geocode: [item.latitude, item.longitude],
          popUp: item.name,
          isWithinRadius: false
        }));
        setMarkers(updatedMarkers);
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  const isWithinRadius = (marker, otherMarkers) => {
    for (const otherMarker of otherMarkers) {
      if (marker !== otherMarker) {
        const distance = L.latLng(marker.geocode).distanceTo(L.latLng(otherMarker.geocode));
        if (distance <= 5000) {
          return true;
        }
      }
    }
    return false;
  };

  return (
    <MapContainer center={[3.15673, 101.71225]} zoom={13} maxZoom={18}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <MarkerClusterGroup chunkedLoading iconCreateFunction={createClusterCustomIcon}>
        {markers.map((marker, index) => {
          const icon = isWithinRadius(marker, markers)
            ? new Icon({ iconUrl: require("./icons/outlet.png"), iconSize: [38, 38] })
            : customIcon;

          return (
            <Marker key={index} position={marker.geocode} icon={icon}>
              <Popup>{marker.popUp}</Popup>
            </Marker>
          );
        })}
      </MarkerClusterGroup>

      <FeatureGroup>
        {markers.map((marker, index) => (
          <Circle
            key={`circle-${index}`}
            center={marker.geocode}
            pathOptions={circleOptions}
            radius={5000}
          />
        ))}
      </FeatureGroup>
    </MapContainer>
  );
}