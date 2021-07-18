#!/bin/bash

#creating manager and workers
docker-machine create --driver virtualbox manager
docker-machine create --driver virtualbox worker1
docker-machine create --driver virtualbox worker2
docker-machine create --driver virtualbox worker3

#connect manager and start swarm
eval $(docker-machine env manager)
docker swarm init --advertise-addr eth1

#copy code like below that swarm has given
    docker swarm join --token SWMTKN-1-46rhtokdqdi9r64stiieoeek4gbmpvozn9snv93kfl14cj1air-4t525v014h0ot6ubs88mjkv9z 192.168.99.152:2377

eval $(docker-machine env worker1)
#paste worker link above
eval $(docker-machine env worker2)
#paste worker link above
eval $(docker-machine env worker3)
#paste worker link above

eval $(docker-machine env manager)

docker service create --name registry --publish published=5000,target=5000 registry:2


cd backend-software
docker build -t backend-software .

docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml push

docker stack deploy --compose-file docker-compose.yml backend-software

note: if ".docker/machine/machines/manager/ca.pem: no such file or directory" error exist use command
      eval $(docker-machine env -u)

