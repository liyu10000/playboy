import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JTextArea;
import javax.swing.JScrollPane;
import javax.swing.JFileChooser;
import javax.swing.JOptionPane;
import java.awt.Font;
import java.awt.Color;
import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.BufferedReader;
import java.io.BufferedWriter;


public class TextEditor {
	static JFrame frame;
	static JTextArea text;

	public TextEditor() {
		frame = new JFrame("Text Editor");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		// menu
		JMenuBar menuBar = new JMenuBar();
		// file menus
		JMenu file = new JMenu("File");
		file.add(new FileMenu("open"));
		file.add(new FileMenu("save"));
		file.add(new FileMenu("clear"));
		file.add(new FileMenu("print"));
		file.add(new FileMenu("close"));
		menuBar.add(file);
		// edit menus
		JMenu edit = new JMenu("Edit");
		JMenu edit_s = new JMenu("size");
		edit_s.add(new EditMenu("increase"));
		edit_s.add(new EditMenu("decrease"));
		edit.add(edit_s);
		JMenu edit_c = new JMenu("color");
		edit_c.add(new EditMenu("black"));
		edit_c.add(new EditMenu("red"));
		edit_c.add(new EditMenu("green"));
		edit.add(edit_c);
		menuBar.add(edit);
		frame.setJMenuBar(menuBar);

		// text area
		JPanel panel = new JPanel();
		panel.setLayout(new BorderLayout());
		text = new JTextArea();
		text.setTabSize(4);
		text.setLineWrap(true);
		JScrollPane scrollPane = new JScrollPane(text);
		panel.add(scrollPane, BorderLayout.CENTER);
		frame.add(panel);

		frame.setSize(500, 600);
		frame.setVisible(true);
	}

	public static void main(String[] args) {
		new TextEditor();
	}

	private class FileMenu extends JMenuItem implements ActionListener {
		public FileMenu(String name) {
			super(name);
			addActionListener(this);
		}
		public void actionPerformed(ActionEvent e) {
			String s = e.getActionCommand();
			JFileChooser chooser;
			switch (s) {
				case "open":
					chooser = new JFileChooser(System.getProperty("java.class.path"));
					if (chooser.showOpenDialog(null) == JFileChooser.APPROVE_OPTION) {
						File f = new File(chooser.getSelectedFile().getAbsolutePath());
						try {
							FileReader fr = new FileReader(f);
							BufferedReader br = new BufferedReader(fr);
							String body = "", line = "";
							while ((line = br.readLine()) != null) {
								body += line + "\n";
							}
							text.setText(body);
							br.close();
						} catch (Exception evt) {
							JOptionPane.showMessageDialog(frame, evt.getMessage());
						}
					} else {
						System.out.println("open operation cancelled");
					}
					break;
				case "save":
					chooser = new JFileChooser(System.getProperty("java.class.path"));
					if (chooser.showSaveDialog(null) == JFileChooser.APPROVE_OPTION) {
						File f = new File(chooser.getSelectedFile().getAbsolutePath());
						try {
							FileWriter fw = new FileWriter(f, false);
							BufferedWriter bw = new BufferedWriter(fw);
							bw.write(text.getText());
							bw.flush();
							bw.close();
						} catch (Exception evt) {
							JOptionPane.showMessageDialog(frame, evt.getMessage());
						}
					} else {
						System.out.println("save operation cancelled");
					}
					break;
				case "clear":
					text.setText("");
					break;
				case "print":
					try {
						text.print();
					} catch (Exception evt) {
						JOptionPane.showMessageDialog(frame, evt.getMessage());
					}
					break;
				case "close":
					frame.setVisible(false);
					System.exit(0);
					break;
				default:
					System.err.println("no match");
			}
		}
	}

	private class EditMenu extends JMenuItem implements ActionListener {
		public EditMenu(String name) {
			super(name);
			addActionListener(this);
		}
		public void actionPerformed(ActionEvent e) {
			String s = e.getActionCommand();
			if (s.equals("increase")) {
				float new_size = text.getFont().getSize2D() + 2;
				text.setFont(text.getFont().deriveFont(new_size));
				System.out.println("font size increased to " + (int)new_size);
			} else if (s.equals("decrease")) {
				float new_size = text.getFont().getSize2D() - 2;
				text.setFont(text.getFont().deriveFont(new_size));
				System.out.println("font size decreased to " + (int)new_size);
			} else if (s.equals("black")) {
				text.setForeground(Color.black);
				System.out.println("text color changed to black");
			} else if (s.equals("red")) {
				text.setForeground(Color.red);
				System.out.println("text color changed to red");
			} else if (s.equals("green")) {
				text.setForeground(Color.green);
				System.out.println("text color changed to green");
			} 
		}
	}
}