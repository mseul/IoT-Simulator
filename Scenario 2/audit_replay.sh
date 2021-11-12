#!/bin/bash

generate_test_for_fail() {
	echo "if ! "$2" &>/dev/null; then    echo $1 PASS; else echo $1 FAIL; fi;"
}

peerhost=$1

tests=""
while IFS= read -r line; do
    tests+=$(generate_test_for_fail "${line%%=*}" "${line#*=}")
done

testoutput=""
for atest in "${tests[@]}"
do
	testoutput+=$(eval "$atest" 2>1)
done

echo "Test Outcome: $testoutput"
testoutputsanitized=${testoutput// /}
testoutputsanitized=${testoutputsanitized//[^a-zA-Z0-9_]/}

if [ -n "$peerhost" ]; then
    echo "Connecting to Peer $peerhost..."
    peertestoutput+=$(ssh -tt -o StrictHostKeyChecking=accept-new -i ./peering_key root@$peerhost "$atest" 2>/dev/null)
    echo "Peer Outcome: $peertestoutput"
    peertestoutputsanitized=${peertestoutput// /}
    peertestoutputsanitized=${peertestoutputsanitized//[^a-zA-Z0-9_]/}    

    if [[ "$testoutputsanitized" == "$peertestoutputsanitized" ]]; then
        echo "Results MATCH"
    else
        echo "Results do NOT match."
    fi

fi
