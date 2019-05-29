/* *****************************************************************************
 *  Name: Li Yu
 *  Date: 5 / 29 / 2019
 *  Description: self-study
 **************************************************************************** */

import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;

import java.util.Iterator;
import java.util.NoSuchElementException;

public class RandomizedQueue<Item> implements Iterable<Item> {
    private Item[] array;
    private int size;

    public RandomizedQueue()                 // construct an empty randomized queue
    {
        array = (Item[]) new Object[4];
        size = 0;
    }

    public boolean isEmpty()                 // is the randomized queue empty?
    {
        return size == 0;
    }

    public int size()                        // return the number of items on the randomized queue
    {
        return size;
    }

    private void resizeArray(int newCapacity) {
        Item[] newArray = (Item[]) new Object[newCapacity];
        for (int i = 0; i < size; i++)
            newArray[i] = array[i];
        array = newArray;
    }

    public void enqueue(Item item)           // add the item
    {
        if (item == null)
            throw new IllegalArgumentException("item should not be null.");
        array[size++] = item;
        if (size == array.length / 2)
            resizeArray(array.length * 2);
    }

    public Item dequeue()                    // remove and return a random item
    {
        if (size == 0)
            throw new NoSuchElementException("queue is empty.");
        int i = StdRandom.uniform(size);
        Item item = array[i];
        size--;
        array[i] = array[size];
        array[size] = null;
        if (size > 0 && size == array.length / 4)
            resizeArray(array.length / 4);
        return item;
    }

    public Item sample()                     // return a random item (but do not remove it)
    {
        if (size == 0)
            throw new NoSuchElementException("queue is empty.");
        int i = StdRandom.uniform(size);
        Item item = array[i];
        return item;
    }

    private class RandomIterator implements Iterator<Item> {
        private int[] order = StdRandom.permutation(size);
        private int current = 0;

        public boolean hasNext() {
            return current < size;
        }

        public Item next() {
            if (current == size)
                throw new NoSuchElementException("no more items.");
            Item item = array[order[current++]];
            return item;
        }

        public void remove() {
            throw new UnsupportedOperationException("not supported.");
        }
    }

    public Iterator<Item> iterator()         // return an independent iterator over items in random order
    {
        return new RandomIterator();
    }

    public static void main(String[] args)   // unit testing (optional)
    {
        int[] a = StdRandom.permutation(10);
        for (int i : a)
            StdOut.println(i);
    }
}
