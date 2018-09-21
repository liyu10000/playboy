// package client;

import java.awt.Font;
import java.awt.Component;
import java.awt.Container;
import java.awt.BorderLayout;
import java.awt.GridBagLayout;
import java.awt.GridBagConstraints;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
//import java.awt.event.KeyEvent;
import java.awt.image.BufferedImage;
import java.awt.Image;
import java.awt.Insets;
import java.awt.Dimension;
import java.io.File;
//import java.io.IOException;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.table.TableColumn;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.JTextField;
import javax.swing.JFileChooser;
import javax.swing.JOptionPane;
import javax.swing.ImageIcon;
import javax.swing.border.Border;
import javax.swing.BorderFactory;
import javax.swing.UIManager;
import javax.swing.plaf.FontUIResource;
import java.util.Enumeration;

// import client.Client;


public class ClientGui {
	// private Client client;
	private JFrame frame;
	private JTable table;

	public ClientGui() {
		setUIFont (new FontUIResource(new Font("MS Mincho",Font.PLAIN, 20)));
		guiSetup();
	}

	private void guiSetup() {
		JFrame frame = new JFrame("Sync");
		frame.setLayout(new GridBagLayout());
		GridBagConstraints c = new GridBagConstraints();
		Border eBorder = BorderFactory.createEtchedBorder();

		// connection panel
		JPanel panelUp = new JPanel();
		panelUp.setBorder(BorderFactory.createTitledBorder(eBorder, "connection"));
		c.gridx = c.gridy = 0;
		c.gridwidth = 2; c.gridheight = 1;
		c.fill = GridBagConstraints.BOTH;
		c.anchor = GridBagConstraints.CENTER;
		c.weightx = 100; c.weighty = 15;
		frame.add(panelUp, c);

		// file lists panel
		JPanel panelDown = new JPanel();
		panelDown.setBorder(BorderFactory.createTitledBorder(eBorder, "file lists"));
		panelDown.setLayout(new BorderLayout());
		c.gridx = 0; c.gridy = 1;
		c.gridwidth = 1; c.gridheight = 1;
		c.weightx = 80; c.weighty = 85;
		String[][] data = {
			{"0", "/home/sakulaki/yolo-yuli/playboy/java/P2PFileSharing/res/test.txt", "C:/tsimage/playboy/java/P2PFileSharing/res/test.txt"},
			{"1", "/home/sakulaki/yolo-yuli/playboy/java/P2PFileSharing/res/test.jpg", "C:/tsimage/playboy/java/P2PFileSharing/res/test.jpg"},
			{"2", "/home/sakulaki/yolo-yuli/playboy/java/P2PFileSharing/res/test.xml", "C:/tsimage/playboy/java/P2PFileSharing/res/test.xml"}
		};
		String[] columnNames = {"index", "server (remote)", "client (local)"};
		table = new JTable(data, columnNames);
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
		frame.add(panelDown, c);

		// control panel
		JPanel panelRight = new JPanel();
		panelRight.setBorder(BorderFactory.createTitledBorder(eBorder, "control"));
		c.gridx = 1; c.gridy = 1;
		c.gridwidth = 1; c.gridheight = 1;
		c.weightx = 20; c.weighty =85;
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

	public static void main(String[] args) {
		
		new ClientGui();
	}
}