# **Messenger**

## How to run

### On local host (Currently not working, sorry =/. Use **'On specified address'** instead)
To run client and server at the same time just do the following:  

`git clone https://github.com/Farrukhraz/messenger.git`  

`cd messenger`  

`python messenger`  

In this case server will receive connections from all hosts on 7777 port.
Client will run on 'localhost:7777'

### On specified address

`git clone https://github.com/Farrukhraz/messenger.git`  

**Run *server***:  

`cd messenger/server`  

`python main.py [-p 1234 -addr blabla.com]`

**Run *client***:  

`cd messenger/client`  

`python main.py -addr blabla.com [-p 1234]`
