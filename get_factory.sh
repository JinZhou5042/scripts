#!/bin/bash

ps -aux | grep "[v]ine_factory" | while read -r user pid other; do
    cmd=$(ps -p $pid -o args=)
    cmd_launching_dir=$(tr '\0' '\n' < /proc/$pid/environ | grep '^PWD=' | cut -d '=' -f 2)
    for word in $cmd; do
        if [[ $word =~ \.json$ ]]; then
            factory_file=$word
            break;
        fi
    done
    if [ "${factory_file:0:1}" == "/" ]; then
        factory_file=$factory_file
    else
        factory_file="$(readlink -m "${cmd_launching_dir}/${factory_file}")"
    fi
    factory_content=$(cat $factory_file)
    manager_name=$(echo $factory_content | jq -r '.["manager-name"]')
    
    output_file="factory_info.txt"
    echo "command = $cmd" > $output_file
    echo "factory launching directory = $cmd_launching_dir" >> $output_file
    echo "factory configuration file = $factory_file" >> $output_file
    echo "factory manager name = $manager_name" >> $output_file
    echo "factory content = $factory_content" >> $output_file
     
 

done


