## File Sharing Program

### compile and run
 - Compile: _javac -d bin src/server/*.java src/client/*.java src/util/*.java_
 - Execute (server side): _java server.Server [port]_
 - Execute (client side, cmd mode): _java client.Client [server host] [server port]_
 - Execute (client side, gui mode): _java client.ClientGui_

### GUI
 - connection: the connection host and port with server. Need to watch on status.
 - file list: the list of files or folders to push/pull.
 - control:
<pre>
	push: upload from local to remote.
	pull: download from remote to local.
	delete: delete file/folder entry.
	add: add new file/folder entry. A pop up window will appear for inputs.
	save info: save host/port and file/folder entries to local csv files, so that it will be loaded next time at GUI startup.
</pre>

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