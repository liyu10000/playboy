## File Sharing Program

### compile and run
 - Compile: _javac -d bin src/server/*.java src/client/*.java src/util/*.java_
 - Execute (server side): _java server.Server [port]_
 - Execute (client side, cmd mode): _java client.Client [server host] [server port]_
 - Execute (client side, gui mode): _java client.ClientGui_

### dataflow
 - Norm: Server waits for commands from Client, push or pull.
 
#### job: server_to_client
<pre>
Server:
	"server_to_client"
		2 read file info
		3 send file
Client:
	"server_to_client"
		1 send file info
		4 read file
</pre>

#### job: client_to_server
<pre>
Server:
	"client_to_server"
		2 read file
Client:
	"client_to_server"
		1 send file
</pre>