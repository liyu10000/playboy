package util;

import java.io.File;


public class FileInfo {
	private String serverFile;
	private String clientFile;
	private boolean isServer;
	private File file;
	private long lastModified;

	public FileInfo(String serverFile, String clientFile, boolean isServer) {
		this.serverFile = serverFile;
		this.clientFile = clientFile;
		this.isServer = isServer;
		if (isServer) {
			this.file = new File(serverFile);
		} else {
			this.file = new File(clientFile);
		}
		this.lastModified = this.file.lastModified();
	}

	public boolean exists() {
		return this.file.exists();
	}

	public String getFileName() {
		return this.file.getName();
	}

	public String getFullFileName() {
		return this.file.getAbsolutePath();
	}

	public String getServerFile() {
		return this.serverFile;
	}

	public String getClientFile() {
		return this.clientFile;
	}

	public String getRemoteFile() {
		if (this.isServer) {
			return this.clientFile;
		} else {
			return this.serverFile;
		}
	}

	public File getFile() {
		return this.file;
	}

	public long getFileSize() {
		return this.file.length();
	}

	public boolean hasModified() {
		if (this.file.lastModified() > this.lastModified) {
			this.lastModified = this.file.lastModified();
			return true;
		}
		return false;
	}
}