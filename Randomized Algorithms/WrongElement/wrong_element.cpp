#include <iostream>
#include <fstream>
#include <vector>
#include <bitset>
#include <algorithm>
#include <random>
#include <time.h>
#include <chrono>

using namespace std;

template <int N>
bitset<N> from_hex(string &hex_str) {
    bitset <N> bits;
    transform(hex_str.begin(), hex_str.end(), hex_str.begin(), ::tolower);
    size_t pos = 0;
    for (auto letter : hex_str) {
        switch (letter) {
            case '0':
                break;
            case '1':
                bits.set(pos + 3);
                break;
            case '2':
                bits.set(pos + 2);
                break;
            case '3':
                bits.set(pos + 2);
                bits.set(pos + 3);
                break;
            case '4':
                bits.set(pos + 1);
                break;
            case '5':
                bits.set(pos + 1);
                bits.set(pos + 3);
                break;
            case '6':
                bits.set(pos + 1);
                bits.set(pos + 2);
                break;
            case '7':
                bits.set(pos + 1);
                bits.set(pos + 2);
                bits.set(pos + 3);
                break;
            case '8':
                bits.set(pos);
                break;
            case '9':
                bits.set(pos);
                bits.set(pos + 3);
                break;
            case 'a':
                bits.set(pos);
                bits.set(pos + 2);
                break;
            case 'b':
                bits.set(pos);
                bits.set(pos + 2);
                bits.set(pos + 3);
                break;
            case 'c':
                bits.set(pos);
                bits.set(pos + 1);
                break;
            case 'd':
                bits.set(pos);
                bits.set(pos + 1);
                bits.set(pos + 3);
                break;
            case 'e':
                bits.set(pos);
                bits.set(pos + 1);
                bits.set(pos + 2);
                break;
            case 'f':
                bits.set(pos);
                bits.set(pos + 1);
                bits.set(pos + 2);
                bits.set(pos + 3);
                break;
        }
        pos += 4;
    }
    return bits;
}

template <int N>
vector<bitset<N>> read_matrix(ifstream &is, const int &n) {
    vector<bitset<N>> matrix(n);
    bitset<N> bits;
    string str;
    for (int i = 0; i < n; ++i) {
        is >> str;
        bits = from_hex<N>(str);
        for (unsigned int j = n; j < 4 * str.size(); ++j) {
            bits.set(j, false);
        }
        matrix[i] = bits;
    }
    return matrix;
}

mt19937_64 create_generator() {
    mt19937_64 generator;
    generator.seed(time(NULL));
    return generator;
}

mt19937_64 generator = create_generator();
uniform_int_distribution<int>  distribution(0, 1);

template <int N>
bitset<N> generate_vector(bitset<N> &bits, const int &length) {
    for (int n = 0; n < length; ++n) {
        bits[n] = distribution(generator);
    }
    return bits;
}

template <int N>
bitset<N> mul(const vector<bitset<N>> &matrix, const bitset<N> &v, bitset<N> &result) {
    const unsigned long n = matrix.size();
    for (unsigned i = 0; i < n; ++i) {
        result[i] = 1 & (matrix[i] & v).count();
    }
    return result;
}

template <int N>
int check_mul(const bitset<N> &v, const vector<bitset<N>> &matrix, const bitset<N> &correct, const int &n) {
    bitset<N> res;
    unsigned start = v._Find_first();
    if (start == N) {
        return correct._Find_first();
    }
    for (int i = start; i < n; ++i) {
        if (v[i]) {
            res ^= matrix[i];
        }
    }
    return (res ^ correct)._Find_first();
}

template <int N>
void check(ifstream &is, ofstream &os, const int &n, const int &iterations) {
    auto a = read_matrix<N>(is, n);
    auto b = read_matrix<N>(is, n);
    auto c = read_matrix<N>(is, n);

    string answer;
    bitset<N> v, result, tmp_result, tmp_compare, right_result;
    for (int i = 0; i < iterations; ++i) {
        generate_vector<N>(v, n);
        mul<N>(a, mul<N>(b, v, tmp_result), result);
        mul<N>(c, v, right_result);

        tmp_compare = result ^ right_result;
        auto row = tmp_compare._Find_first();

        if (row != N) {
            auto column = check_mul<N>(a[row], b, c[row], n);
            os << "Yes\n" << row + 1 << " " << column + 1 << "\n";
            return;
        }
    }
    os << "No\n";
}

int main() {
    ifstream is("element.in");
    ofstream os("element.out");
    const int N1 = 64, N2 = 4000;
    const int iterations = 20;
    int n;
    is >> n;
    while(n) {
        (n <= N1) ? check<N1>(is, os, n, iterations) : check<N2>(is, os, n, iterations);
        is >> n;
    }

    is.close();
    os.close();

    return 0;
}
