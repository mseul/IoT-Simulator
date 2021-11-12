#!/bin/bash

generate_test_for_fail() {
	echo "if ! $2 &>/dev/null; then    echo $1 PASS; else echo $1 FAIL; fi;"
}

#echo $1
#echo $2

tests=""
while IFS= read -r line; do
    #tests["${line%%=*}"]="${line#*=}"
    tests+=$(generate_test_for_fail "${line%%=*}" "${line#*=}")
done

testoutput=""
for atest in "${tests[@]}"
do
	testoutput+=$(eval "$atest")
done

mytesthash=$(echo -n $testoutput | md5sum)

echo $mytesthash
