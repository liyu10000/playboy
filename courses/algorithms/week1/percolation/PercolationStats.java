/* *****************************************************************************
 *  Name:
 *  Date:
 *  Description:
 **************************************************************************** */

import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;
import edu.princeton.cs.algs4.StdStats;

public class PercolationStats {
    private final double m;
    private final double s;
    private final double lo;
    private final double hi;

    public PercolationStats(int n,
                            int trials)    // perform trials independent experiments on an n-by-n grid
    {
        if (n <= 0 || trials <= 0)
            throw new IllegalArgumentException(n + " or " + trials + " not positive.");
        double[] ps = new double[trials];
        for (int i = 0; i < trials; i++) {
            Percolation percolation = new Percolation(n);
            while (!percolation.percolates()) {
                int row = StdRandom.uniform(1, n + 1);
                int col = StdRandom.uniform(1, n + 1);
                percolation.open(row, col);
            }
            ps[i] = percolation.numberOfOpenSites() / (double) (n * n);
        }

        m = StdStats.mean(ps);
        s = StdStats.stddev(ps);
        double delta = 1.96 * s / Math.sqrt(trials);
        lo = m - delta;
        hi = m + delta;
    }

    public double mean()                          // sample mean of percolation threshold
    {
        return m;
    }

    public double stddev()                        // sample standard deviation of percolation threshold
    {
        return s;
    }

    public double confidenceLo()                  // low  endpoint of 95% confidence interval
    {
        return lo;
    }

    public double confidenceHi()                  // high endpoint of 95% confidence interval
    {
        return hi;
    }

    public static void main(String[] args) {
        if (args.length != 2) {
            StdOut.println("need to take two arguments n and T.");
            return;
        }
        int n = Integer.parseInt(args[0]);
        int trials = Integer.parseInt(args[1]);
        PercolationStats percolationStats = new PercolationStats(n, trials);
        double m = percolationStats.mean();
        double s = percolationStats.stddev();
        double lo = percolationStats.confidenceLo();
        double hi = percolationStats.confidenceHi();
        StdOut.printf("mean                    = %f\n", m);
        StdOut.printf("stddev                  = %f\n", s);
        // StdOut.printf("95% confidence interval = [%f, %f]\n", lo, hi);
        StdOut.print("95% confidence interval = [");
        StdOut.print(lo);
        StdOut.print(", ");
        StdOut.print(hi);
        StdOut.print("]\n");
    }
}
