package util;

import java.io.File;
import java.io.IOException;


public class FileInfo {
	private String filename;
	private String serverDir;
	private String clientDir;
	private File file;
	private long lastModified;

	public FileInfo(String filename, String serverDir, String clientDir, boolean isServer) {
		this.filename = filename;
		this.serverDir = serverDir;
		this.clientDir = clientDir;
		if (isServer) {
			this.file = new File(serverDir, filename);
		} else {
			this.file = new File(clientDir, filename);
		}
		this.lastModified = this.file.lastModified();
	}

	public String getFilename() {
		return filename;
	}

	public String getServerDir() {
		return serverDir;
	}

	public String getClientDir() {
		return clientDir;
	}

	public File getFile() {
		return file;
	}

	public long getFileSize() {
		return file.length();
	}

	public boolean hasModified() {
		if (file.lastModified() > lastModified) {
			lastModified = file.lastModified();
			return true;
		}
		return false;
	}

	// private File serverFile;
	// private File clientFile;
	// private long serverFileLastModified;
	// private long clientFilelastModified;

	// public FileInfo(String serverFilename, String clientFilename) {
	// 	try {
	// 		this.serverFile = new File(serverFilename);
	// 		if (!this.serverFile.exists()) {
	// 			this.serverFile.createNewFile();
	// 		}
	// 		this.clientFile = new File(clientFilename);
	// 		if (!this.clientFile.exists()) {
	// 			this.clientFile.createNewFile();
	// 		}
	// 		this.serverFileLastModified = serverFile.lastModified();
	// 		this.clientFilelastModified = clientFile.lastModified();
	// 	} catch (IOException e) {
	// 		e.printStackTrace();
	// 	}
	// }

	// public long getServerFileSize() {
	// 	return serverFile.length();
	// }

	// public long getClientFileSize() {
	// 	return clientFile.length();
	// }

	// public boolean serverModified() {
	// 	if (serverFile.lastModified() > serverFileLastModified) {
	// 		serverFileLastModified = serverFile.lastModified();
	// 		return true;
	// 	}
	// 	return false;
	// }

	// public boolean clientModified() {
	// 	if (clientFile.lastModified() > clientFilelastModified) {
	// 		clientFilelastModified = clientFile.lastModified();
	// 		return true;
	// 	}
	// 	return false;
	// }
}