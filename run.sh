#!/bin/bash

docker pull registry.gitlab.com/kiliant/paper-archive:latest

docker run \
    -e SZ_USER=user \
    -e SZ_PASSWORD=`pass Web/sueddeutsche.de | head -1` \
    -v paper_archive:/data \
    registry.gitlab.com/kiliant/paper-archive:latest
