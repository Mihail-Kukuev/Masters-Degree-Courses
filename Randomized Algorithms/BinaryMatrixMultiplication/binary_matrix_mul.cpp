#include <iostream>
#include <fstream>
#include <vector>
#include <bitset>
#include <algorithm>
#include <random>
#include <time.h>

using namespace std;

const size_t N = 4000;

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

vector<bitset<N>> read_matrix(ifstream &is, const int &n) {
    vector<bitset<N>> matrix;
    bitset<N> bits;
    string str;
    for (int i = 0; i < n; ++i) {
        is >> str;
        bits = from_hex(str);
        for (unsigned int j = n; j < 4 * str.size(); ++j) {
            bits.set(j, false);
        }
        matrix.emplace_back(bits);
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

bitset<N> generate_vector(bitset<N> &bits, const int &length) {
    for (int n = 0; n < length; ++n) {
        bits[n] = distribution(generator);
    }
    return bits;
}

bitset<N> mul(const vector<bitset<N>> &matrix, const bitset<N> &vector, bitset<N> &result) {
    for (unsigned i = 0; i < matrix.size(); ++i) {
        result[i] = 1 & (matrix[i] & vector).count();
    }
    return result;
}

void print_vector(const bitset<N> &vector, const int &length) {
    string str = vector.to_string().substr(N - length, length);
    reverse(str.begin(), str.end());
    cout << str << endl;
}

void print_matrix(const vector<bitset<N>> &matrix, const int &length) {
    for (auto row : matrix) {
        print_vector(row, length);
    }
}

int main() {
    ifstream is("matrix.in");
    int n;
    is >> n;
    auto a = read_matrix(is, n);
    auto b = read_matrix(is, n);
    auto c = read_matrix(is, n);
    is.close();

    string answer = "YES";
    int iterations = 50;
    bitset<N> v, tmp, result, right_result;
    for (int i = 0; i < iterations; ++i) {
        generate_vector(v, n);
        mul(a, mul(b, v, tmp), result);
        mul(c, v, right_result);

        /*cout << "\n\niteration " << i << "\n\n";
        cout << "v\n";
        print_vector(v, n);
        cout << "a\n";
        print_matrix(a, n);
        cout << "b\n";
        print_matrix(b, n);
        cout << "c\n";
        print_matrix(c, n);
        cout << "result\n";
        print_vector(result, n);
        cout << "right\n";
        print_vector(right_result, n);*/

        if (result != right_result) {
            answer = "NO";
            break;
        }
    }

    ofstream os("matrix.out");
    os << answer;
    os.close();

    return 0;
}