package util;

import java.io.File;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;
import java.util.List;
import java.util.ArrayList;

import util.FileInfo;

public class Util {
	public static void pushInfo(Socket socket, DataOutputStream dos, FileInfo fileInfo) {
		try {
			// session starts
			dos.writeInt(1);

			// server full fileName
			dos.writeUTF(fileInfo.getServerFile());
			// client full fileName
			dos.writeUTF(fileInfo.getClientFile());

			// session ends
			dos.writeInt(-1);
			dos.flush();
		} catch (IOException e) {
			System.err.println("[ERROR ] failed to push file info.");
			// e.printStackTrace();
		}
	}

	public static void push(Socket socket, DataOutputStream dos, FileInfo fileInfo) {	
		try {
			if (!fileInfo.exists()) {
				System.err.println("[ERROR ] file does not exist.");
				dos.writeInt(0);
				return;
			}

			List<FileInfo> subFileInfos = fileInfo.getSubFileInfos();
			// send number of subfiles (note: the file itself is included)
			dos.writeInt(subFileInfos.size());
			
			for (FileInfo subFileInfo : subFileInfos) {
				// full fileName
				dos.writeUTF(subFileInfo.getRemoteFile());
				// filesize
				dos.writeLong(subFileInfo.getFileSize());
				// System.out.println("[INFO] head sent.");

				byte[] b = new byte[(int)subFileInfo.getFileSize()];
				FileInputStream fis = new FileInputStream(subFileInfo.getFile());
				BufferedInputStream bis = new BufferedInputStream(fis);
				bis.read(b, 0, b.length);
				dos.write(b, 0, b.length);
				// System.out.println("[INFO] body sent.");

				dos.flush();
				fis.close();
				bis.close();

				System.out.println("[INFO  ] sent file: " + subFileInfo.getFullFileName() + ".");
			}

			// session ends
			dos.writeInt(-1);
		} catch (IOException e) {
			System.err.println("[ERROR ] failed to push file/dir: " + fileInfo.getFullFileName() + ".");
			// e.printStackTrace();
		}
	}

	public static String[] pullInfo(Socket socket, DataInputStream dis) {
		try {
			// session starts
			int start = dis.readInt();

			// server full fileName
			String serverFile = dis.readUTF();
			// client full fileName
			String clientFile = dis.readUTF();

			// session ends
			int end = dis.readInt();

			return new String[]{serverFile, clientFile};
		} catch (IOException e) {
			System.err.println("[ERROR ] failed to pull file info.");
			// e.printStackTrace();
			return null;
		}
	}

	public static void pull(Socket socket, DataInputStream dis) {
		try {
			// session starts
			int start = dis.readInt();
			if (start == 0) {
				System.out.println("[INFO  ] file does not exist on remote.");
				return;
			}

			for (int i = 0; i < start; i++) {
				// full fileName
				String fileName = dis.readUTF();
				// change windows path format to linux path format
				if (System.getProperty("os.name").toLowerCase().startsWith("linux")) {
					fileName = fileName.replace("\\", "/");
				}
				// filesize
				long length = dis.readLong();
				// System.out.println("[INFO] head saved.");

				File file = new File(fileName);
				file.getParentFile().mkdirs();
				FileOutputStream fos = new FileOutputStream(file);
				byte[] b = new byte[4096];
				int filesize = (int) length;
				int read = 0;
				int totalRead = 0;
				int remaining = filesize;
				while ((read = dis.read(b, 0, Math.min(b.length, remaining))) > 0) {
					totalRead += read;
					remaining -= read;
					fos.write(b, 0, read);
				}
				fos.close();
				// System.out.println("[INFO] body saved.");
				System.out.println("[INFO  ] received file: " + fileName + ".");
			}

			// session ends
			int end = dis.readInt();
		} catch (FileNotFoundException e) {
			// e.printStackTrace();
			System.err.println("[ERROR ] file not found on local server.");
		} catch (IOException e) {
			System.err.println("[ERROR ] failed to pull file.");
			// e.printStackTrace();
		}
	}
}