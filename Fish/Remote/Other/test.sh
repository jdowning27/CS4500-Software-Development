#!/bin/bash
sudo ./xserver 123 > log &
SERVER=$!
sleep 2
for ((i = 0; i < $1; i++)); do
    python3 client.py 123 &
    CLIENTS="$CLIENTS $!"
done
wait $SERVER
for client in $CLIENTS; do
    kill $client
done
echo
cat log
rm log
