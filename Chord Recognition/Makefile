setup:
    docker build . -t workshop
    docker run -p 8888:8888 -d --name caio_workshop workshop
.PHONY: get-url
get-url:
    @docker logs caio_workshop >& logs
    @cat logs | grep "127." | sed -n 2p
    @rm -rf logs
clean:
    docker stop caio_workshop
    docker rm caio_workshop
    docker rmi workshop 
