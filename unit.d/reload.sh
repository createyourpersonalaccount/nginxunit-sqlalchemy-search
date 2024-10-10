#!/bin/sh
curl -X GET --unix-socket /var/run/control.unit.sock \
     http://localhost/control/applications/litestar/restart
