### dataflow
	Server waits for commands from Client, push or pull.

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