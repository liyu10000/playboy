package util;

import java.io.File;


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
}