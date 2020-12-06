#!/bin/bash
NUM_CLIENTS=5
cd ..
sudo ./xserver 123 > log &
SERVER=$!
sleep 2
for ((i = 0; i < $NUM_CLIENTS; i++)); do
    python3 ../Fish/Remote/client.py 'localhost' 123 &
    CLIENTS="$CLIENTS $!"
done
wait $SERVER
for client in $CLIENTS; do
    kill $client
done
cat log
if [[ $(cat log) == "[1, 0]" ]]; then
    echo PASSED
else
    echo FAILED
fi
rm log
