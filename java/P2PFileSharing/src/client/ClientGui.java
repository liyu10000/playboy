package client;

import java.awt.Font;
import java.awt.Component;
import java.awt.Container;
import java.awt.BorderLayout;
import java.awt.GridBagLayout;
import java.awt.GridBagConstraints;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.awt.Image;
import java.awt.Insets;
import java.awt.Dimension;
import java.io.File;
import java.io.IOException;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.table.TableModel;
import javax.swing.table.TableColumn;
import javax.swing.table.AbstractTableModel;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.event.ListSelectionListener;
import javax.swing.JTextField;
import javax.swing.JFileChooser;
import javax.swing.JOptionPane;
import javax.swing.ImageIcon;
import javax.swing.border.Border;
import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.UIManager;
import javax.swing.plaf.FontUIResource;
import java.util.List;
import java.util.ArrayList;
import java.util.Enumeration;

import client.Client;
import util.FileInfo;
import util.CsvIO;

public class ClientGui {
	private Client clientCase;
	private JFrame frame;
	private JTable table;
	private String[] columnNames;
	private List<FileInfo> fileInfoList;
	private JTextField hostText;
	private JTextField portText;
	private JLabel connectStatus;

	public ClientGui() {
		loadData();
		setUIFont(new FontUIResource(new Font("MS Mincho", Font.PLAIN, 20)));
		guiSetup();
	}

	private boolean startClient(String host, int port) {
		clientCase = new Client(host, port);
		return clientCase.start();
	}

	private void closeClient() {
		clientCase.close();
	}

	private void loadData() {
		this.columnNames = new String[] {"index", "server (remote)", "client (local)"};
		this.fileInfoList = new ArrayList<FileInfo>();
		File csvFile = new File((new File(System.getProperty("user.dir"))).getParentFile(), "res"+File.separator+"fileList.csv");
		if (!csvFile.exists()) {
			this.fileInfoList = null;
			return;
		}
		ArrayList<ArrayList<String>> data = CsvIO.readCsv(csvFile.getAbsolutePath());
		for (ArrayList<String> row : data) {
			this.fileInfoList.add(new FileInfo(row.get(1), row.get(2), false));
		}
	}

	private void saveData() {
		ArrayList<ArrayList<String>> data = new ArrayList<ArrayList<String>>();
		for (int i = 0; i < table.getRowCount(); i++) {
			ArrayList<String> row = new ArrayList<String>();
			for (int j = 0; j < table.getColumnCount(); j++) {
				row.add((String) table.getValueAt(i, j));
			}
			data.add(row);
		}
		File csvFile = new File((new File(System.getProperty("user.dir"))).getParentFile(), "res"+File.separator+"fileList.csv");
		CsvIO.writeCsv(csvFile.getAbsolutePath(), data);
	}

	private void guiSetup() {
		JFrame frame = new JFrame("Sync");
		frame.setLayout(new GridBagLayout());
		GridBagConstraints c = new GridBagConstraints();
		Border eBorder = BorderFactory.createEtchedBorder();

		// connection panel
		JPanel panelUp = new JPanel();
		panelUp.setBorder(BorderFactory.createTitledBorder(eBorder, "connection"));
		panelUp.setLayout(new GridBagLayout());
		GridBagConstraints cPanelUp = new GridBagConstraints();
		JLabel hostMark = new JLabel("host:");
		cPanelUp.fill = GridBagConstraints.NONE;
		cPanelUp.anchor = GridBagConstraints.LINE_END;
		cPanelUp.insets = new Insets(0,0,0,20);
		cPanelUp.gridx = 1; cPanelUp.gridy = 0;
		cPanelUp.gridwidth = 1; cPanelUp.gridheight = 1;
		cPanelUp.weightx = 10;
		panelUp.add(hostMark, cPanelUp);
		hostText = new JTextField();
		hostText.setText("127.0.0.1");
		cPanelUp.fill = GridBagConstraints.HORIZONTAL;
		cPanelUp.anchor = GridBagConstraints.LINE_START;
		cPanelUp.insets = new Insets(0,0,0,0);
		cPanelUp.gridx = 2; cPanelUp.gridy = 0;
		cPanelUp.gridwidth = 2; cPanelUp.gridheight = 1;
		cPanelUp.weightx = 20;
		panelUp.add(hostText, cPanelUp);
		JLabel portMark = new JLabel("port:");
		cPanelUp.fill = GridBagConstraints.NONE;
		cPanelUp.anchor = GridBagConstraints.LINE_END;
		cPanelUp.insets = new Insets(0,0,0,20);
		cPanelUp.gridx = 5; cPanelUp.gridy = 0;
		cPanelUp.gridwidth = 1; cPanelUp.gridheight = 1;
		cPanelUp.weightx = 10;
		panelUp.add(portMark, cPanelUp);
		portText = new JTextField();
		portText.setText("9999");
		cPanelUp.fill = GridBagConstraints.HORIZONTAL;
		cPanelUp.anchor = GridBagConstraints.LINE_START;
		cPanelUp.insets = new Insets(0,0,0,0);
		cPanelUp.gridx = 6; cPanelUp.gridy = 0;
		cPanelUp.gridwidth = 2; cPanelUp.gridheight = 1;
		cPanelUp.weightx = 20;
		panelUp.add(portText, cPanelUp);
		JLabel connectMark = new JLabel("status:");
		cPanelUp.fill = GridBagConstraints.NONE;
		cPanelUp.anchor = GridBagConstraints.LINE_END;
		cPanelUp.insets = new Insets(0,0,0,20);
		cPanelUp.gridx = 9; cPanelUp.gridy = 0;
		cPanelUp.gridwidth = 1; cPanelUp.gridheight = 1;
		cPanelUp.weightx = 10;
		panelUp.add(connectMark, cPanelUp);
		connectStatus = new JLabel("disconnected");
		cPanelUp.fill = GridBagConstraints.HORIZONTAL;
		cPanelUp.anchor = GridBagConstraints.CENTER;
		cPanelUp.insets = new Insets(0,0,0,0);
		cPanelUp.gridx = 10; cPanelUp.gridy = 0;
		cPanelUp.gridwidth = 2; cPanelUp.gridheight = 1;
		cPanelUp.weightx = 20;
		panelUp.add(connectStatus, cPanelUp);
		JButton connectBtn = new MyButton("connect");
		cPanelUp.fill = GridBagConstraints.HORIZONTAL;
		cPanelUp.anchor = GridBagConstraints.CENTER;
		cPanelUp.insets = new Insets(0,10,0,10);
		cPanelUp.gridx = 12; cPanelUp.gridy = 0;
		cPanelUp.gridwidth = 2; cPanelUp.gridheight = 1;
		cPanelUp.weightx = 20;
		panelUp.add(connectBtn, cPanelUp);
		JButton disconnectBtn = new MyButton("disconnect");
		cPanelUp.fill = GridBagConstraints.HORIZONTAL;
		cPanelUp.anchor = GridBagConstraints.CENTER;
		cPanelUp.insets = new Insets(0,10,0,20);
		cPanelUp.gridx = 14; cPanelUp.gridy = 0;
		cPanelUp.gridwidth = 2; cPanelUp.gridheight = 1;
		cPanelUp.weightx = 20;
		panelUp.add(disconnectBtn, cPanelUp);
		c.gridx = c.gridy = 0;
		c.gridwidth = 2; c.gridheight = 1;
		c.fill = GridBagConstraints.BOTH;
		c.anchor = GridBagConstraints.CENTER;
		c.weightx = 100; c.weighty = 15;
		frame.add(panelUp, c);

		// file lists panel
		JPanel panelDown = new JPanel();
		panelDown.setBorder(BorderFactory.createTitledBorder(eBorder, "file list"));
		panelDown.setLayout(new BorderLayout());
		TableModel tableModel = new MyTableModel();
		table = new JTable(tableModel);
		table.setRowHeight(25);
		DefaultTableCellRenderer centerRenderer = new DefaultTableCellRenderer();
		centerRenderer.setHorizontalAlignment(DefaultTableCellRenderer.CENTER);
		TableColumn indexCol = table.getColumnModel().getColumn(0);
		indexCol.setPreferredWidth(100);
		indexCol.setMinWidth(100);
		indexCol.setMaxWidth(200);
		indexCol.setCellRenderer(centerRenderer);
		JScrollPane scrollPane = new JScrollPane(table);
		table.setFillsViewportHeight(true);
		panelDown.add(scrollPane, BorderLayout.CENTER);
		c.gridx = 0; c.gridy = 1;
		c.gridwidth = 1; c.gridheight = 1;
		c.weightx = 85; c.weighty = 85;
		frame.add(panelDown, c);

		// control panel
		JPanel panelRight = new JPanel();
		panelRight.setBorder(BorderFactory.createTitledBorder(eBorder, "control"));
		panelRight.setLayout(new BoxLayout(panelRight, BoxLayout.Y_AXIS));
		JButton push = new MyButton("push");
		JButton pull = new MyButton("pull");
		JButton delete = new MyButton("delete");
		JButton add = new MyButton("add");
		panelRight.add(push);
		panelRight.add(Box.createVerticalStrut(20));
		panelRight.add(pull);
		panelRight.add(Box.createVerticalStrut(20));
		panelRight.add(delete);
		panelRight.add(Box.createVerticalStrut(20));
		panelRight.add(add);
		c.gridx = 1; c.gridy = 1;
		c.gridwidth = 1; c.gridheight = 1;
		c.weightx = 15; c.weighty =85;
		frame.add(panelRight, c);
		
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setPreferredSize(new Dimension(1200, 600));
		frame.setMinimumSize(new Dimension(1200, 600));
		frame.pack();
		frame.setVisible(true);
	}

	private static void setUIFont(FontUIResource f) {
	    Enumeration<Object> keys = UIManager.getDefaults().keys();
	    while (keys.hasMoreElements()) {
	        Object key = keys.nextElement();
	        Object value = UIManager.get(key);
	        if (value instanceof FontUIResource) {
	            UIManager.put(key, f);
	        }
	    }
	}

	private void appendRow(FileInfo fileInfo) {
		MyTableModel model = (MyTableModel) table.getModel();
		model.appendRow(fileInfo);
	}

	private void removeRows(int[] rows) {
		MyTableModel model = (MyTableModel) table.getModel();
		for (int i = 0; i < rows.length; i++) {
			model.removeRow(table.getSelectedRow());
		}
	}

	private class MyButton extends JButton implements ActionListener {
		public MyButton(String name) {
			super(name);
			setAlignmentX(Component.CENTER_ALIGNMENT);
			addActionListener(this);
		}

		public void actionPerformed(ActionEvent e) {
			String s = e.getActionCommand();
			int[] rows = table.getSelectedRows();
			if (s.equals("connect")) {
				String host = hostText.getText();
				int port = Integer.valueOf(portText.getText());
				if (startClient(host, port)) {
					connectStatus.setText("connected");
				}
			} else if (s.equals("disconnect")) {
				saveData();
				if (connectStatus.getText().equals("connected")) {
					closeClient();
					connectStatus.setText("disconnected");
				}
			} else if (!s.equals("add") && rows.length == 0) {
				JOptionPane.showMessageDialog(frame, "no file choosed", "warning", JOptionPane.WARNING_MESSAGE);
			} else if (s.equals("push") || s.equals("pull")) {
				String signal;
				if (s.equals("push")) {
					signal = "client_to_server";
				} else {
					signal = "server_to_client";
				}
				for (int i = 0; i < rows.length; i++) {
					clientCase.shuttle(signal, fileInfoList.get(rows[i]));
				}
			} else if (s.equals("delete")) {
				removeRows(rows);
			} else if (s.equals("add")) {
				FileInfo fileInfo = new FileInfo("/home/sakulaki/yolo-yuli/playboy/java/P2PFileSharing/res/test.py", "C:/tsimage/playboy/java/P2PFileSharing/res/test.py", false);
				appendRow(fileInfo);
			}
		}
	}

	private class MyTableModel extends AbstractTableModel {
		public int getColumnCount() {
			return columnNames.length;
		}

		public int getRowCount() {
			return fileInfoList.size();
		}

		public String getColumnName(int col) {
			return columnNames[col];
		}

		public Object getValueAt(int row, int col) {
			FileInfo fileInfo = fileInfoList.get(row);
			switch (col) {
				case 0: return String.valueOf(row);
				case 1: return fileInfo.getServerFile();
				case 2: return fileInfo.getClientFile();
				default: return null;
			}
		}

		public void appendRow(FileInfo fileInfo) {
			fileInfoList.add(fileInfo);
			fireTableRowsInserted(fileInfoList.size()-1, fileInfoList.size()-1);

		}

		public void removeRow(int row) {
			fileInfoList.remove(row);
			fireTableRowsDeleted(row, row);
		}
	}

	public static void main(String[] args) {
		new ClientGui();
	}
}