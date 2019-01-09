#include <iostream>
#include <cmath>
#include <fstream>
#include <vector>
#include <algorithm>
#include <random>
#include <chrono>

using namespace std;

mt19937_64 create_generator() {
    mt19937_64 generator;
    generator.seed(time(NULL));
    return generator;
}

mt19937_64 generator = create_generator();
const int p = 300007;
uniform_int_distribution<int> distribution(1, p - 1);

inline int mod(const int &x, const int &m) {
    return (x % m + m) % m;
}

vector<vector<int>> generate_tutte(vector<pair<int, int>> edges, const int &n) {
    vector<vector<int>> tutte(n);
    for (int i = 0; i < n; ++i) {
        tutte[i].resize(n);
    }

    int value;
    for (auto edge: edges) {
        value = distribution(generator);
        tutte[edge.first][edge.second] = value;
        tutte[edge.second][edge.first] = mod(-value, p);
    }
    return tutte;
}

int gcdex(const int &a, const int &b, int &x, int &y) {
    if (a == 0) {
        x = 0;
        y = 1;
        return b;
    }
    int x1, y1;
    int d = gcdex(b % a, a, x1, y1);
    x = y1 - (b / a) * x1;
    y = x1;
    return d;
}

int inverse_mod(const int &a, const int &m) {
    int x, y;
    int g = gcdex(a, m, x, y);

    if (g != 1)
        exit(1);
    else
        return mod(x, m);
}

inline int mulmod(const int &a, const int &b, const int &m) {
    return mod(a * b, m);
}

inline int divmod(const int &a, const int &b, const int &m) {
    return mulmod(a, inverse_mod(b, m), m);
}


int gauss(vector<vector<int>> &m, vector<vector<int>> &inverse) {
    const int n = m.size();
    int det = 1;

    for (int i = 0; i < n; ++i) {
        fill(inverse[i].begin(), inverse[i].end(), 0);
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

        swap(m[k], m[i_lead]);
        swap(inverse[k], inverse[i_lead]);

        int m_kk = m[k][k];
        det = mulmod(det, m_kk, p);
        for (int j = k; j < n; ++j) {
            m[k][j] = divmod(m[k][j], m_kk, p);
        }
        for (int j = 0; j < n; ++j) {
            inverse[k][j] = divmod(inverse[k][j], m_kk, p);
        }
        for (int i = k + 1; i < n; ++i) {
            if (m[i][k] != 0) {
                int m_ik = m[i][k];
                for (int j = k; j < n; ++j) {
                    m[i][j] = mod(m[i][j] - m[k][j] * m_ik, p);
                }
                for (int j = 0; j < n; ++j) {
                    inverse[i][j] = mod(inverse[i][j] - inverse[k][j] * m_ik, p);
                }
            }
        }
    }

    for (int k = n - 1; k > 0; --k) {
        for (int i = k - 1; i >= 0; --i) {
            if (m[i][k] != 0) {
                for (int j = 0; j < n; ++j) {
                    inverse[i][j] = mod(inverse[i][j] - inverse[k][j] * m[i][k], p);
                }
            }
        }
    }

    return det;
}

int main() {
    int n, m;

    ifstream ifile("matching.in");
    ifile >> n >> m;
    vector<pair<int, int>> edges(m);
    int u, v;
    for (int i = 0; i < m; ++i) {
        ifile >> u >> v;
        edges[i] = u < v ? pair<int, int>(u - 1, v - 1) : pair<int, int>(v - 1, u - 1);
    }
    ifile.close();

    vector<bool> answers(m, false);
    vector<vector<int>> inverse_tutte(n);
    for (int i = 0; i < n; ++i) {
        inverse_tutte[i].resize(n);
    }
    int iterations = 15;
    if (n % 2 == 0 && m >= n / 2) {
        for (int iteration = 0; iteration < iterations; ++iteration) {
            vector<vector<int>> tutte = generate_tutte(edges, n);
            if (gauss(tutte, inverse_tutte) != 0) {
                for (int i = 0; i < m; ++i) {
                    if (answers[i] == 0) {
                        answers[i] = (inverse_tutte[edges[i].first][edges[i].second] != 0);
                    }
                }
            }
        }
    }

    ofstream ofile("matching.out");
    for (int i = 0; i < m; ++i) {
        if (answers[i])
            ofile << "YES\n";
        else
            ofile << "NO\n";
    }
    ofile.close();

    return 0;
}