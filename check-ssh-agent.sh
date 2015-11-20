#!/usr/bin/env bash

#credit: https://github.com/alt3/cakebox

printf %63s |tr " " "-"
printf '\n'
printf "Sanity checking SSH Agent Forwarding\n"
printf %63s |tr " " "-"
printf '\n'

# Show user
USER=$(whoami 2>&1)
echo "Running checks as user $USER"

# Show status of SSH Agent
echo "SSH Agent details:"
OUTPUT=$(ssh-agent 2>&1)
IFS=' ' read -a lines <<< "$OUTPUT"
for line in "${lines[@]}"
do
    echo "=> $line"
done

# Show loaded keys
echo "SSH Forwarded keys:"
OUTPUT=$(ssh-add -l 2>&1)
EXITCODE=$?
echo "=> $OUTPUT"