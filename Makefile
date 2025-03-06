# This makefile doesn't try to manage dependencies.
# It's main purpose is to have a central place for the various commands and share variables between them.

target_host := root@railtrails.ineranves.de:/opt/railtrails
source_base := /mnt/osm-data
input_file := /mnt/storage/planet-250224.osm.pbf
docker_tag_name := martin/railtrails
volume_mounts := -v ${input_file}:/data/region.osm.pbf -v ${source_base}/static:/data/styles/data -v osm-data:/data/database/ -v ${source_base}/tiles:/data/tiles -v ${source_base}/extracted-tiles:/data/extracted-tiles

nothing:
	@echo "Please specify a target"

sync: synctiles syncfrontend

synctiles:
	rsync --delete -v -r ${source_base}/extracted-tiles/ ${target_host}/tiles

buildfrontend:
	cd frontend && npm run build

syncfrontend: buildfrontend
	rsync --delete -v -r --exclude /tiles frontend/dist/ ${target_host}

dockerimage:
	cd docker && docker build -t ${docker_tag_name} .

cleanall: cleantiles cleandatabase

cleantiles:
	rm -rf ${source_base}/extracted-tiles/* ${source_base}/tiles/* 
	
cleandatabase:	
	rm -rf ${source_base}/world/*

import: 
	docker run -p 5432:5432 -e "OSM2PGSQL_EXTRA_ARGS=-C 20480" -e "FLAT_NODES=enabled" -e THREADS=24 ${volume_mounts} ${docker_tag_name} import

render:
	docker run -p 5432:5432 -e THREADS=24 ${volume_mounts} --shm-size=512m ${docker_tag_name} generate

servetiles:
	docker run -p 8888:80 -p 5432:5432 -e THREADS=24 ${volume_mounts} --shm-size=512m ${docker_tag_name} run


download:
	aria2c --dir=$(dir ${input_file}) --out=$(notdir ${input_file}) https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf.torrent

.PHONY: nothing synctiles buildfrontend syncfrontend dockerimage cleanall cleantiles cleandatabase import render servetiles download