/* *****************************************************************************
 *  Name:
 *  Date:
 *  Description:
 **************************************************************************** */

import edu.princeton.cs.algs4.WeightedQuickUnionUF;

public class Percolation {
    private final WeightedQuickUnionUF uf1;
    private final WeightedQuickUnionUF uf2;
    private final int n;
    private final boolean[][] m;
    private int openSites;

    public Percolation(int n)                // create n-by-n grid, with all sites blocked
    {
        if (n <= 0)
            throw new IllegalArgumentException(n + " should be positive.");
        this.n = n;
        m = new boolean[n + 1][n + 1];
        uf1 = new WeightedQuickUnionUF(n * n + 2);  // with both virtual top and bottom
        uf2 = new WeightedQuickUnionUF(n * n + 1);  // only with virtual top
        openSites = 0;
    }

    private int index(int row, int col) {
        return (row - 1) * n + (col - 1) + 1;
    }

    private void validate(int row, int col) {
        if (row < 1 || row > n || col < 1 || col > n)
            throw new IllegalArgumentException(row + " and " + col + " should be in range 1 ~ n");
    }

    public void open(int row, int col)    // open site (row, col) if it is not open already
    {
        if (isOpen(row, col))
            return;
        int p = index(row, col);
        if (row == 1) {
            uf1.union(p, 0);
            uf2.union(p, 0);
        }
        if (row == n) {
            uf1.union(p, n * n + 1);
        }

        if (col > 1 && isOpen(row, col - 1)) {  // left
            uf1.union(p, index(row, col - 1));
            uf2.union(p, index(row, col - 1));
        }
        if (row > 1 && isOpen(row - 1, col)) {  // top
            uf1.union(p, index(row - 1, col));
            uf2.union(p, index(row - 1, col));
        }
        if (col < n && isOpen(row, col + 1)) {  // right
            uf1.union(p, index(row, col + 1));
            uf2.union(p, index(row, col + 1));
        }
        if (row < n && isOpen(row + 1, col)) {  // bottom
            uf1.union(p, index(row + 1, col));
            uf2.union(p, index(row + 1, col));
        }

        m[row][col] = true;
        openSites++;
    }

    public boolean isOpen(int row, int col)  // is site (row, col) open?
    {
        validate(row, col);
        return m[row][col];
    }

    public boolean isFull(int row, int col)  // is site (row, col) full?
    {
        return isOpen(row, col) && uf2.connected(0, index(row, col));
    }

    public int numberOfOpenSites()       // number of open sites
    {
        return openSites;
    }

    public boolean percolates()              // does the system percolate?
    {
        return uf1.connected(0, n * n + 1);
    }

    public static void main(String[] args) {
        Percolation percolation = new Percolation(10);
        percolation.open(5, 5);
    }
}
