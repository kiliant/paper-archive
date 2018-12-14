#!/bin/bash

docker run \
    -e SZ_USER=email@example.com \
    -e SZ_PASSWORD=`pass Web/sueddeutsche.de | head -1` \
    -v paper_archive:/data \
    registry.gitlab.com/kiliant/paper-archive:latest
