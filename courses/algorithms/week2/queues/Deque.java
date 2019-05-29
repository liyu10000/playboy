/* *****************************************************************************
 *  Name: Li Yu
 *  Date: 5 / 29 / 2019
 *  Description: self-study
 **************************************************************************** */

import edu.princeton.cs.algs4.StdOut;

import java.util.Iterator;
import java.util.NoSuchElementException;

public class Deque<Item> implements Iterable<Item> {
    private Node first;
    private Node last;
    private int size;

    private class Node {
        private Item item;
        private Node prev;
        private Node next;

        Node(Item item) {
            this.item = item;
            this.prev = null;
            this.next = null;
        }
    }

    private class MyIterator implements Iterator<Item> {
        private Node current = first;

        public boolean hasNext() {
            return current != null;
        }

        public Item next() {
            if (current == null)
                throw new NoSuchElementException("no more items.");
            Item item = current.item;
            current = current.next;
            return item;
        }

        public void remove() {
            throw new UnsupportedOperationException("not supported.");
        }
    }

    public Deque()                           // construct an empty deque
    {
        first = null;
        last = null;
        size = 0;
    }

    public boolean isEmpty()                 // is the deque empty?
    {
        return size == 0;
    }

    public int size()                        // return the number of items on the deque
    {
        return size;
    }

    public void addFirst(Item item)          // add the item to the front
    {
        if (item == null)
            throw new IllegalArgumentException("item should not be null.");
        Node node = new Node(item);
        if (first == null) {
            first = node;
            last = first;
        }
        else {
            first.prev = node;
            node.next = first;
            first = node;
        }
        size++;
    }

    public void addLast(Item item)           // add the item to the end
    {
        if (item == null)
            throw new IllegalArgumentException("item should not be null.");
        Node node = new Node(item);
        if (last == null) {
            last = node;
            first = last;
        }
        else {
            node.prev = last;
            last.next = node;
            last = node;
        }
        size++;
    }

    public Item removeFirst()                // remove and return the item from the front
    {
        if (size == 0)
            throw new NoSuchElementException("Deque is empty.");
        Item item = first.item;
        if (size == 1) {
            first = null;
            last = null;
        }
        else {
            first.next.prev = null;
            first = first.next;
        }
        size--;
        return item;
    }

    public Item removeLast()                 // remove and return the item from the end
    {
        if (size == 0)
            throw new NoSuchElementException("Deque is empty.");
        Item item = last.item;
        if (size == 1) {
            first = null;
            last = null;
        }
        else {
            last.prev.next = null;
            last = last.prev;
        }
        size--;
        return item;
    }

    public Iterator<Item> iterator()         // return an iterator over items in order from front to end
    {
        return new MyIterator();
    }

    public static void main(String[] args)   // unit testing (optional)
    {
        Deque<String> deque = new Deque<>();
        deque.addFirst("gwge");
        deque.addLast("gwegg");
        deque.addFirst("2343");
        StdOut.println(deque.size());
        for (String item : deque)
            StdOut.println(item);
        deque.removeLast();
        for (String item : deque)
            StdOut.println(item);
        deque.removeFirst();
        for (String item : deque)
            StdOut.println(item);
        deque.removeLast();
        for (String item : deque)
            StdOut.println(item);
    }
}
