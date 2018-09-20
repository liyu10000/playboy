package util;

import java.io.File;
import java.io.IOException;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;

import util.FileInfo;

public class Util {
	public static void push(Socket socket, DataOutputStream dos, FileInfo fileInfo, boolean isServer) throws IOException {
		// session starts
		dos.writeInt(1);

		// directory
		if (!isServer) {
			dos.writeUTF(fileInfo.getServerDir());
		} else {
			dos.writeUTF(fileInfo.getClientDir());
		}
		// filename
		dos.writeUTF(fileInfo.getFilename());
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
	}

	public static void pull(Socket socket, DataInputStream dis) throws IOException {
		// session starts
		int start = dis.readInt();

		// directory
		String directory = dis.readUTF();
		// filename
		String filename = dis.readUTF();
		// filesize
		long length = dis.readLong();
		// System.out.println("[INFO] head saved.");

		FileOutputStream fos = new FileOutputStream(directory + File.separatorChar + filename);
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
	}
}