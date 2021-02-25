# **Messenger**

## How to run (On local host)

`git clone https://github.com/Farrukhraz/messenger.git`  

### **Run *server***:  

`cd messenger/server`  

`python main.py [-p 7777 -addr blabla.com]`  

`-p` and `-addr` arguments are optional. By default `-p=7777` and `-addr=" "`  

### **Run *client***:  

`cd messenger/client`  

`python main.py -addr localhost [-p 7777]`  

`-p` argument is optional but `-addr` is required. By default `-p=7777`. Use `-addr localhost`
to run client locally   
