#!/bin/bash

#activate the env
source env/bin/activate

#generate the mandatory JWT_SECRET if it doesnt exist
if [[ "$JWT_SECRET" == "" ]]; then
    echo "JWT_SECRET doesnt exist. Creating a new one..."
    export JWT_SECRET="$(python -c 'import secrets; print(secrets.token_hex(32))')"
fi

create_mariadb_docker_container() {
    echo "Creating mariadb-server docker..."
    # echo "sudo docker run -d \
    #     --name mariadb-server \
    #     --restart unless-stopped \
    #     -e MARIADB_USER="$DB_USER"
    #     -e MARIADB_ROOT_PASSWORD="$DB_ROOT_PASSWORD"
    #     -e MARIADB_DATABASE="$DB_NAME"
    #     -e MARIADB_PASSWORD="$DB_PASSWORD"
    #     -p 127.0.0.1:"$DB_PORT":3306 \
    #     -v mariadb_data:/var/lib/mysql \ 
    #     mariadb:latest"
    
    sudo docker run -d \
        --name mariadb-server \
        --restart unless-stopped \
        -e MARIADB_USER="$DB_USER" \
        -e MARIADB_ROOT_PASSWORD="$DB_ROOT_PASSWORD" \
        -e MARIADB_DATABASE="$DB_NAME" \
        -e MARIADB_PASSWORD="$DB_PASSWORD" \
        -p 127.0.0.1:"$DB_PORT":3306 \
        -v mariadb_data:/var/lib/mysql \
        mariadb:latest
}



#check if there is a mariadb-server docker container
if ! sudo docker ps -a | grep -i mariadb-server; then
    echo "No mariadb-server docker container found"
    echo "Creating a mariadb-server docker container..."

    if create_mariadb_docker_container; then
        echo "mariadb-server created successfully!"
    else
        echo "something went wrong when creating the mariadb-server container..."
    fi
else
    echo "mariadb-server docker container found"
    #check if its running 
    if ! sudo docker ps | grep -i mariadb-server; then 
        echo "container is stopped."
        echo "Starting mariadb-server..."
        sudo docker start mariadb-server
    fi

    if sudo docker start mariadb-server; then
        echo "mariadb-server started successfully!"
    fi
fi

#start the server (-m is module flag so it solves the paths correctly)
python -m server.main

# echo "To compile specify the word 'compile' as the 1st argument and the '.proto' file as the 2nd argument"
# echo "Ex: ./server.sh compile main.proto"

# #find .proto file
# find_proto_file() {
#     for file in *.proto; do
#         if [[ -f "$file" ]]; then
#             proto_file="$file"
#             return 0
#         fi
#     done

#     return 1
# }
   
# if [[ $1 == "compile" ]]; then
#     if find_proto_file; then
#         echo "Found proto file: $proto_file"
#     fi

#     if [[ $? -eq 0 ]]; then
#         python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/"$proto_file"
#         if [[ $? -eq 0 ]]; then
#             echo "Compiled succesfully!"
#         fi
#     fi
# fi


