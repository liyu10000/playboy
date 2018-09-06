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
import java.io.FileWriter;
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
		JMenuItem file_o = new FileMenu("open");
		JMenuItem file_s = new FileMenu("save");
		JMenuItem file_p = new FileMenu("print");
		JMenuItem file_n = new FileMenu("new");
		file.add(file_o);
		file.add(file_s);
		file.add(file_p);
		file.add(file_n);
		menuBar.add(file);
		// edit menus
		JMenu edit = new JMenu("Edit");
		JMenu edit_s = new JMenu("size");
		JMenuItem edit_si = new EditMenu("increase");
		JMenuItem edit_sd = new EditMenu("decrease");
		JMenu edit_c = new JMenu("color");
		JMenuItem edit_cb = new EditMenu("black");
		JMenuItem edit_cr = new EditMenu("red");
		JMenuItem edit_cg = new EditMenu("green");
		edit_s.add(edit_si);
		edit_s.add(edit_sd);
		edit.add(edit_s);
		edit_c.add(edit_cb);
		edit_c.add(edit_cr);
		edit_c.add(edit_cg);
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
			switch (s) {
				case "open":
					JFileChooser chooser = new JFileChooser();
					if (chooser.showOpenDialog(null) == JFileChooser.APPROVE_OPTION) {
						
					}
					break;
				case "save":
					JFileChooser chooser = new JFileChooser();
					if (chooser.showSaveDialog(null) == JFileChooser.APPROVE_OPTION) {
						File f = new File(chooser.getSelectedFile().getAbsolutePath());
						try {
							FileWriter wr = new FileWriter(f, false);
							BufferedWriter bw = new BufferedWriter(wr);
							bw.write(text.getText());
							bw.flush();
							bw.close();
						} catch (Exception evt) {
							JOptionPane.showMessageDialog(frame, evt.getMessage());
						}
					} else {
						JOptionPane.showMessageDialog(frame, "the user cancelled the operation");
					}
					break;
				case "print":
					break;
				case "new":
					break;
				default:
					System.out.println("no match");
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