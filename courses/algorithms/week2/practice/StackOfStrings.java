import java.util.Scanner;

public class StackOfStrings
{
	private class Node
	{
		String item;
		Node next;
	}

	private Node first;
	private int size;

	public StackOfStrings()
	{
		first = null;
		size = 0;
	}

	public void push(String item)
	{
		Node node = new Node();
		node.item = item;
		node.next = first;
		first = node;
		size++;
	}

	public String pop()
	{
		if (size == 0)
			return "";
		String item = first.item;
		first = first.next;
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
		Scanner scan = new Scanner(System.in);
		StackOfStrings stack = new StackOfStrings();
		while (scan.hasNextLine()) {
			String s = scan.nextLine();
			if (s.equals("-")) System.out.println(stack.pop());
			else stack.push(s);
		}
	}
}