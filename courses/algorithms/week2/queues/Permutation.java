/* *****************************************************************************
 *  Name:
 *  Date:
 *  Description:
 **************************************************************************** */

import edu.princeton.cs.algs4.StdIn;
import edu.princeton.cs.algs4.StdOut;

public class Permutation {
    public static void main(String[] args) {
        if (args.length < 1) {
            StdOut.println("need to take one argument k.");
            return;
        }
        int k = Integer.parseInt(args[0]);
        RandomizedQueue<String> rqueue = new RandomizedQueue<>();
        while (!StdIn.isEmpty()) {
            String item = StdIn.readString();
            rqueue.enqueue(item);
        }
        for (int i = 0; i < k; i++) {
            String item = rqueue.dequeue();
            StdOut.println(item);
        }
    }
}
