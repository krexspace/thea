sudo docker run \
    --name p-neo \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$PWD/data_neo:/data \
    --env=NEO4J_AUTH=none \
    -d neo4j
