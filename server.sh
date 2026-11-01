#!/bin/bash

echo "To compile specify the word 'compile' as the 1st argument and the '.proto' file as the 2nd argument"
echo "Ex: ./server.sh compile main.proto"

#find .proto file
find_proto_file() {
    for file in *.proto; do
        if [[ -f "$file" ]]; then
            proto_file="$file"
            return 0
        fi
    done

    return 1
}
   
if [[ $1 == "compile" ]]; then
    if find_proto_file; then
        echo "Found proto file: $proto_file"
    fi

    if [[ $? -eq 0 ]]; then
        python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. "$proto_file"
        if [[ $? -eq 0 ]]; then
            echo "Compiled succesfully!"
        fi
    fi
fi


