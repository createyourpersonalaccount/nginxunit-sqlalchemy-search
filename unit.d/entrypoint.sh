#!/bin/sh
f=/var/run/control.unit.sock
unitd
until [ -S "$f" ]; do
  sleep 0.1
done
curl -X PUT --data-binary @/etc/unit.json --unix-socket "$f" http://localhost/config
tail -f /dev/null
