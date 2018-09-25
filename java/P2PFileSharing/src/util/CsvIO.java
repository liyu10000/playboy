package util;

import java.io.FileReader;
import java.io.BufferedReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class CsvIO {
	private static final String DELIMITER = ",";
	private static final String SEPARATOR = "\n";

	public static ArrayList<ArrayList<String>> readCsv(String fileName) {
		ArrayList<ArrayList<String>> data = new ArrayList<ArrayList<String>>();
		BufferedReader fileReader = null;
		try{
			fileReader = new BufferedReader(new FileReader(fileName));
			String line;
			while ((line = fileReader.readLine()) != null) {
				ArrayList<String> row = new ArrayList<String>();
				String[] tokens = line.split(DELIMITER);
				for (String token : tokens) {
					row.add(token);
				}
				data.add(row);
			}
		} catch (Exception e) {
			System.err.println("[ERROR ] failed to read csv file.");
		} finally {
			try {
				fileReader.close();
				System.out.println("[INFO  ] loaded data from " + fileName);
			} catch (IOException e) {
				System.err.println("[ERROR ] failed to close BufferedReader.");
			}
		}
		return data;
	}

	public static void writeCsv(String fileName, ArrayList<ArrayList<String>> data) {
		FileWriter fileWriter = null;
		try {
			fileWriter = new FileWriter(fileName);
			for (ArrayList<String> row : data) {
				for (String token : row) {
					fileWriter.append(token);
					fileWriter.append(DELIMITER);
				}
				fileWriter.append(SEPARATOR);
			}
		} catch (Exception e) {
			System.err.println("[ERROR ] failed to write csv file.");
		} finally {
			try {
				fileWriter.flush();
				fileWriter.close();
				System.out.println("[INFO  ] saved data to " + fileName);
			} catch (IOException e) {
				System.err.println("[ERROR ] failed to close FileWriter.");
			}
		}
	}

	public static void main(String[] args) {
		String fileName = System.getProperty("user.dir")+"/../res/fileList.csv";
		System.out.println(fileName);
	}
}