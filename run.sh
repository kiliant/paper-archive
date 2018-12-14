#!/bin/bash

docker run \
    -e SZ_USER=email-address \
    -e SZ_PASSWORD=`pass Web/sueddeutsche.de | head -1` \
    -v paper_archive:/data \
    paper-archive
