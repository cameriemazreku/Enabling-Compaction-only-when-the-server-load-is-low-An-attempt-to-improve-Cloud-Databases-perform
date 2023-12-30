#!/bin/bash
output_file=$1
while true; do
    clear  # Clear the terminal to refresh the output
    sudo cat /proc/buddyinfo >> $output_file 
    echo >> $output_file
    sleep 5  # Adjust the sleep duration as needed
done

