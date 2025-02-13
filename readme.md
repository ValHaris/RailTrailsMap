
# Idea

Show all cycling paths on former railway lines on map. 
 
# Concept

The map is composed of 2 layers:
1. As base layer the standard OpenSteetMap map, served directly from OpenStreetmap
1. As overlay a semi-transparent layer highlighting the rail trails.

The overlay map is served from static images.

This allows to:
- keep hosting costs down
- have less software running on the server, reducing complexity and attack surface
- run an immutable server

Because the RailTrail layer consists of mostly empty tiles, we can apply some optimizations:

## Serving optimizations

We are rendering [meta tiles](https://wiki.openstreetmap.org/wiki/Meta_tiles), but serving plain PNG files.

Each meta tile is processed to determine whether its contained tiles are fully transparent or contain content. Only tiles with content are extracted and uploaded to the server.

The web server is configured to return a fully transparent default tile for any requested tile that is not available on the file system.

## Rendering optimizations

For zoom levels up to level 9, all meta tiles for the whole planet will be rendered.
For zoom levels above that, only those tiles will be rendered where the corresponding tile on the lower zoom level was non-empty.

# Implementation

Tile generation is done by a docker container based on https://github.com/Overv/openstreetmap-tile-server


# References:
  - https://www.volkerschatz.com/net/osm/renderd.html
  - http://bahntrassenradeln.de/
  - https://github.com/Overv/openstreetmap-tile-server
