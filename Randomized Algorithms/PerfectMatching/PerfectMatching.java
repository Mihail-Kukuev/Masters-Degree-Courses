import javafx.util.Pair;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.math.BigInteger;
import java.util.*;

public class PerfectMatching {

    private static int P = 10000019;
    private static BigInteger BIG_P = BigInteger.valueOf(P);
    private static Random RANDOM = new Random();

    public static void main(String[] args) throws FileNotFoundException {
        Scanner sc = new Scanner(new File("matching.in"));

        int n = sc.nextInt();
        int m = sc.nextInt();

        List<Pair<Integer, Integer>> edges = new ArrayList<>(m);
        for (int i = 0; i < m; ++i) {
            int u = sc.nextInt() - 1;
            int v = sc.nextInt() - 1;
            edges.add(u < v ? new Pair<>(u, v) : new Pair<>(v, u));
        }
        sc.close();

        BitSet answers = new BitSet(m);
        long[][] tutte = new long[n][n];
        long[][] inverseTutte = new long[n][n];

        int iterations = 5;
        if (n % 2 == 0 && m >= n / 2) {
            for (int iteration = 0; iteration < iterations; ++iteration) {
                generateTutte(edges, tutte);
                if (gauss(tutte, inverseTutte) != 0) {
                    for (int i = 0; i < m; ++i) {
                        if (!answers.get(i)) {
                            answers.set(i, inverseTutte[edges.get(i).getKey()][edges.get(i).getValue()] != 0);
                        }
                    }
                }
            }
        }

        PrintWriter pw = new PrintWriter("matching.out");
        for (int i = 0; i < m; ++i) {
            if (answers.get(i)) {
                pw.println("YES");
            } else {
                pw.println("NO");
            }
        }
        pw.close();

    }

    private static void generateTutte(List<Pair<Integer, Integer>> edges, long[][] tutte) {
        for (long[] row : tutte) {
            Arrays.fill(row, 0);
        }

        int value;
        for (Pair<Integer, Integer> edge : edges) {
            value = RANDOM.nextInt(P - 1) + 1;
            tutte[edge.getKey()][edge.getValue()] = value;
            tutte[edge.getValue()][edge.getKey()] = Math.floorMod(-value, P);
        }
    }

    private static long gauss(long[][] m, long[][] inverse) {
        int n = m.length;
        long det = 1;

        for (int i = 0; i < n; ++i) {
            Arrays.fill(inverse[i], 0);
            inverse[i][i] = 1;
        }

        for (int k = 0; k < n; ++k) {
            int i_lead = k;

            for (int i = k; i < n; ++i) {
                if (m[i][k] != 0) {
                    i_lead = i;
                    break;
                }
            }

            if (m[i_lead][k] == 0) {
                return 0;
            }

            swap(m, k, i_lead);
            swap(inverse, k, i_lead);

            det = Math.floorMod(det * m[k][k], P);
            int inversed_m_kk = BigInteger.valueOf(m[k][k]).modInverse(BIG_P).intValue();
            for (int j = k; j < n; ++j) {
                m[k][j] = Math.floorMod(m[k][j] * inversed_m_kk, P);
            }
            for (int j = 0; j < n; ++j) {
                inverse[k][j] = Math.floorMod(inverse[k][j] * inversed_m_kk, P);
            }
            for (int i = k + 1; i < n; ++i) {
                if (m[i][k] != 0) {
                    long m_ik = m[i][k];
                    for (int j = k; j < n; ++j) {
                        m[i][j] = Math.floorMod(m[i][j] - m[k][j] * m_ik, P);
                    }
                    for (int j = 0; j < n; ++j) {
                        inverse[i][j] = Math.floorMod(inverse[i][j] - inverse[k][j] * m_ik, P);
                    }
                }
            }
        }

        for (int k = n - 1; k > 0; --k) {
            for (int i = k - 1; i >= 0; --i) {
                if (m[i][k] != 0) {
                    for (int j = 0; j < n; ++j) {
                        inverse[i][j] = Math.floorMod(inverse[i][j] - inverse[k][j] * m[i][k], P);
                    }
                }
            }
        }

        return det;
    }

    private static void swap(long[][] a, int i, int j) {
        for (int k = 0; k < a[i].length; k++) {
            long tmp = a[i][k];
            a[i][k] = a[j][k];
            a[j][k] = tmp;
        }
    }
}
