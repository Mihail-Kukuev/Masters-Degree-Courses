import javafx.util.Pair;

import java.io.File;
import java.io.PrintWriter;
import java.math.BigInteger;
import java.util.Scanner;

public class CarmichaelTest {

    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(new File("carmichael.in"));
        PrintWriter pw = new PrintWriter("carmichael.out");

        long amount = sc.nextLong();
        long n;
        for (int i = 0; i < amount; i++) {
            n = sc.nextLong();
            pw.write(isCarmichael(n) ? "Yes\n" : "No\n");
        }

        sc.close();
        pw.close();
    }

    private static boolean isCarmichael(long n) {
        if (isPrime(n) || n < 2 || (n & 1) == 0)
            return false;

        long rounds = 20;
        long a;
        long leftLimit = 2;
        BigInteger bigN = BigInteger.valueOf(n);
        BigInteger bigN_1 = BigInteger.valueOf(n-1);
        BigInteger bigA;
        for (int k = 0; k < rounds; ++k) {
            a = leftLimit + (long) (Math.random() * (n - 2 - leftLimit));

            long g = gcd (n, a);
            while (g != 1) {
                ++a;
                g = gcd (n, a);
            }

            bigA = BigInteger.valueOf(a);
            if (!BigInteger.ONE.equals(bigA.modPow(bigN_1, bigN))){
                return false;
            }
        }
        return true;
    }

    private static long gcd (long a, long b) {
        return (a == 0) ? b : gcd (b % a, a);
    }

    private static boolean isPrime(long n) {
        if (n == 2)
            return true;
        if (n < 2 || (n & 1) == 0)
            return false;

//        long rounds = (long) (Math.log(n) / Math.log(2));
        long rounds = Math.min((long) (Math.log(n) / Math.log(2)), 20);
        long a;
        long leftLimit = 2;
        for (int k = 0; k < rounds; ++k) {
            a = leftLimit + (long) (Math.random() * (n - 2 - leftLimit));
            if (!millerRabin(n, a))
                return false;
        }
        return true;
    }

    private static boolean millerRabin(long n, long a) {
        Pair<Integer, Long> pair = decompose(n - 1);
        int s = pair.getKey();
        long d = pair.getValue();

        BigInteger bigN = BigInteger.valueOf(n);
        BigInteger bigN_1 = BigInteger.valueOf(n - 1);
        BigInteger bigA = BigInteger.valueOf(a);
        BigInteger bigD = BigInteger.valueOf(d);
        BigInteger bigTwo = BigInteger.valueOf(2);

        BigInteger x = bigA.modPow(bigD, bigN);
        if (x.equals(BigInteger.ONE) || x.equals(bigN_1))
            return true;

        for (int r = 1; r < s; r++) {
            x = x.modPow(bigTwo, bigN);
            if (x.equals(BigInteger.ONE)) {
                return false;
            }
            if (x.equals(bigN_1)) {
                return true;
            }
        }
        return false;
    }

    private static Pair<Integer, Long> decompose(long n) {
        int s = 0;
        long d = n;
        while ((d & 1) == 0) {
            d >>= 1;
            ++s;
        }
        return new Pair<>(s, d);
    }
}
