#!/bin/bash

RAM_USAGE_RERC_LIMIT=20
DELAY_SEC=2
ALARM_URL="http://0.0.0.0:8080"
SERVER_ID=123

echo "<- ram checker started ->"
echo "RAM_USAGE_RERC_LIMIT: $RAM_USAGE_RERC_LIMIT"
echo "DELAY_SEC: $DELAY_SEC"
echo "ALARM_URL: $ALARM_URL"
echo "SERVER_ID: $SERVER_ID"
echo "request to: ${ALARM_URL}/${SERVER_ID}"

while true
do
    # grab the second line of the ouput produced by the command: free -g (displays output in Gb)
    secondLine=$(free -m | sed -n '2p')

    #split the string in secondLine into an array
    read -ra ADDR <<< "$secondLine"

    #get the total RAM from array
    totalRam="${ADDR[1]}"

    #get the used RAM from array
    usedRam="${ADDR[2]}"

    # calculate and display the percentage
    pct="$(($usedRam*100/$totalRam))"
    echo -en "\r$pct%"
    sleep $DELAY_SEC


    if [ $pct -ge $RAM_USAGE_RERC_LIMIT ]
    then
        echo -ne ' ALARM!'
        curl -s -X POST -H 'Content-Type: application/json' -d "{\"value\":\"$pct\"}"  "${ALARM_URL}/${SERVER_ID}" > /dev/null
    else
        :
    fi
done