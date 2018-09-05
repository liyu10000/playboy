import javax.swing.*;

public class JFrameTest {
	private JFrame frame;

	public JFrameTest() {
		frame = new JFrame("Text Editor");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		JButton open = new JButton("open");
		open.setBounds(165, 35, 115, 55);
		frame.add(open);
		frame.setSize(500, 600);
		frame.setLayout(null);
		frame.setVisible(true);
	}

	public static void main(String[] args) {
		new JFrameTest();
	}
}