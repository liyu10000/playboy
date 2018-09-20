### dataflow
	Server waits for commands from Client, push or pull.

#### job: server_to_client
<pre>
Server:
	"server_to_client"
		TBD
Client:
	"server_to_client"
		TBD
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