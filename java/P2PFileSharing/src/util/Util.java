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

import util.FileInfo;

public class Util {
	public static void pushInfo(Socket socket, DataOutputStream dos, FileInfo fileInfo) {
		try {
			// session starts
			dos.writeInt(1);

			// server full filename
			dos.writeUTF(fileInfo.getServerFile());
			// client full filename
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

			// session starts
			dos.writeInt(1);

			dos.writeUTF(fileInfo.getRemoteFile());
			// filesize
			dos.writeLong(fileInfo.getFileSize());
			// System.out.println("[INFO] head sent.");

			byte[] b = new byte[(int)fileInfo.getFileSize()];
			FileInputStream fis = new FileInputStream(fileInfo.getFile());
			BufferedInputStream bis = new BufferedInputStream(fis);
			bis.read(b, 0, b.length);
			dos.write(b, 0, b.length);
			// System.out.println("[INFO] body sent.");

			// session ends
			dos.writeInt(-1);
			dos.flush();
			fis.close();
			bis.close();

			System.out.println("[INFO  ] sent file: " + fileInfo.getFullFilename() + ".");
		} catch (IOException e) {
			System.err.println("[ERROR ] failed to push file: " + fileInfo.getFullFilename() + ".");
			// e.printStackTrace();
		}
	}

	public static String[] pullInfo(Socket socket, DataInputStream dis) {
		try {
			// session starts
			int start = dis.readInt();

			// server full filename
			String serverFile = dis.readUTF();
			// client full filename
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

			// full filename
			String filename = dis.readUTF();
			// filesize
			long length = dis.readLong();
			// System.out.println("[INFO] head saved.");

			FileOutputStream fos = new FileOutputStream(filename);
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

			// session ends
			int end = dis.readInt();

			System.out.println("[INFO  ] received file: " + filename + ".");
		} catch (FileNotFoundException e) {
			// e.printStackTrace();
			System.err.println("[ERROR ] file not found on local server.");
		} catch (IOException e) {
			System.err.println("[ERROR ] failed to pull file.");
			// e.printStackTrace();
		}
	}
}