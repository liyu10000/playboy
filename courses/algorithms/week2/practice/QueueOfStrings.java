import java.util.Scanner;

public class QueueOfStrings
{
	private class Node
	{
		String item;
		Node next;
	}

	private Node first;
	private Node last;
	private int size;

	public QueueOfStrings()
	{
		first = null;
		last = null;
		size = 0;
	}

	public void enqueue(String item)
	{
		Node node = new Node();
		node.item = item;
		if (last != null)
			last.next = node;
		last = node;
		if (first == null)
			first = last;
		size++;
	}

	public String dequeue()
	{
		if (size == 0)
			return "";
		String item = first.item;
		Node tmp = first;
		first = first.next;
		tmp = null; // make last to be null if empty
		size--;
		return item;
	}

	public boolean isEmpty()
	{
		return size == 0;
	}

	public int size()
	{
		return size;
	}

	public static void main(String[] args)
	{
		Scanner scanner = new Scanner(System.in);
		QueueOfStrings stack = new QueueOfStrings();
		while (scanner.hasNextLine()) {
			String s = scanner.nextLine();
			if (s.equals("-")) System.out.println(stack.dequeue());
			else stack.enqueue(s);
		}
	}
}