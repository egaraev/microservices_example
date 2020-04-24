#!/bin/sh


# Create Rabbitmq user
( sleep 10; \
echo " [######] SCRIPT PING "; \
rabbitmqctl await_startup ; \
rabbitmqctl add_vhost / ; \
rabbitmqctl add_user user1 pass1 ; \
rabbitmqctl set_user_tags user1 administrator ; \
rabbitmqctl set_permissions -p / user1  ".*" ".*" ".*" ; \
echo " [######] USER CREATION DONE ") & rabbitmq-server
