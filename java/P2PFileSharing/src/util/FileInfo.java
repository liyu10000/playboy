package util;

import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.ArrayList;


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

	public boolean isFile() {
		return this.file.isFile();
	}

	public boolean isDirectory() {
		return this.file.isDirectory();
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

	private void getSubFileInfos(File currFile, List<String> fileNames) {
		if (currFile.isFile()) {
			fileNames.add(currFile.getAbsolutePath());
		} else {
			File[] subFiles = currFile.listFiles();
			for (File subFile : subFiles) {
				getSubFileInfos(subFile, fileNames);
			}
		}
	}

	public List<FileInfo> getSubFileInfos() {
		List<String> fileNames = new ArrayList<String>();
		getSubFileInfos(this.file, fileNames);

		List<FileInfo> subFileInfos = new ArrayList<FileInfo>();
		Path localPath = Paths.get(getFullFileName());
		Path remotePath = Paths.get(getRemoteFile());
		for (String fileName : fileNames) {
			Path localFilePath = Paths.get(fileName);
			// the case when it's a file, not a directory
			if (localPath.getNameCount() == localFilePath.getNameCount()) {
				subFileInfos.add(this);
				break;
			}
			Path remoteFilePath = remotePath.resolve(localFilePath.subpath(localPath.getNameCount(), localFilePath.getNameCount()));
			String remoteFileName = remoteFilePath.toString();
			FileInfo subFileInfo = null;
			if (this.isServer) {
				subFileInfo = new FileInfo(fileName, remoteFileName, true);
			} else {
				subFileInfo = new FileInfo(remoteFileName, fileName, false);
			}
			subFileInfos.add(subFileInfo);
		}
		return subFileInfos;
	}
}