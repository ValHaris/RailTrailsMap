import './style.css';
import 'ol/ol.css';
import {Map, View} from 'ol';
import {XYZ} from 'ol/source';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import {defaults as defaultControls} from 'ol/control/defaults.js';
import { fromLonLat, toLonLat } from 'ol/proj'; 
import ScaleLine from 'ol/control/ScaleLine.js';

const map = new Map({
  target: 'map',
  controls: defaultControls().extend([
    new ScaleLine()
  ]),
  layers: [
    new TileLayer({
      source: new OSM(),
      attributions: [
        OSM.ATTRIBUTION,
                'Tiles courtesy of ' +
                '<a href="http://openstreetmap.org">' +
                'OpenStreetMap' +
                '</a>'
              ],
    }),
    new TileLayer({
      source: new XYZ({
              url: window.location.protocol + '//railtrailsmap.net/tiles/{z}/{x}/{y}.png',
              // url: 'http://localhost:8888/tile/{z}/{x}/{y}.png',  // for testing
              maxZoom: 16,
              minZoom: 4
            })
    }) 
  ],
  view: new View()
});


function updateURL() {
  const view = map.getView();
  const center = view.getCenter();
  const zoom = view.getZoom();

  // Convert coordinates to Lon/Lat
  const lonLat = toLonLat(center);

  // Update the URL without reloading the page
  const newUrl = `${window.location.pathname}?lon=${lonLat[0].toFixed(6)}&lat=${lonLat[1].toFixed(6)}&zoom=${zoom.toFixed(2)}`;
  history.replaceState(null, '', newUrl);
}

map.on('moveend', updateURL);

// Optional: Read URL parameters on load and set the initial view
const params = new URLSearchParams(window.location.search);
const lon = parseFloat(params.get('lon')) || 10;
const lat = parseFloat(params.get('lat')) || 51;
const zoom = parseFloat(params.get('zoom')) || 6;

map.getView().setCenter(fromLonLat([lon, lat]));
map.getView().setZoom(zoom);