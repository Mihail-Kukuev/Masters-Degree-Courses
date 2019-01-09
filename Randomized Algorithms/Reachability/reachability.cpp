#include <iostream>
#include <cmath>
#include <fstream>
#include <vector>
#include <set>
#include <algorithm>
#include <random>

using namespace std;

void dfs(const int &v, const vector<vector<int>> &graph, vector<char> &used, vector<int> &order) {
    used[v] = true;
    for (int adj_v: graph[v]) {
        if (!used[adj_v])
            dfs(adj_v, graph, used, order);
    }
    order.push_back(v);
}

void fill_component(const int &v, const vector<vector<int>> &graph_t, vector<char> &used, vector<int> &component) {
    used[v] = true;
    component.push_back(v);
    for (int adj_v: graph_t[v]) {
        if (!used[adj_v])
            fill_component(adj_v, graph_t, used, component);
    }
}

vector<int> top_sort(const vector<vector<int>> &graph) {
    int n = graph.size();
    vector<char> used(n);
    vector<int> order;

    used.assign(n, false);
    for (int i = 0; i < n; ++i) {
        if (!used[i])
            dfs(i, graph, used, order);
    }
    return order;
}


vector<vector<int>> create_components(const vector<vector<int>> &graph_t, const vector<int> &order) {
    int n = graph_t.size();
    vector<char> used(n);
    vector<vector<int>> components;

    used.assign(n, false);
    for (int i = n - 1; i >= 0; --i) {
        int v = order[i];
        if (!used[v]) {
            vector<int> component;
            fill_component(v, graph_t, used, component);
            components.push_back(component);
        }
    }
    return components;
}

vector<int> color_vertices(const vector<vector<int>> &graph, const vector<vector<int>> &components_order) {
    vector<int> colors(graph.size());
    for (unsigned int color = 0; color < components_order.size(); ++color) {
        for (int v: components_order[color]) {
            colors[v] = color;
        }
    }
    return colors;
}

vector<set<int>> reduce(const vector<vector<int>> &graph, const vector<int> &v_colors, const size_t &colors_number) {
    vector<set<int>> reduced(colors_number);
    for (unsigned int v = 0; v < graph.size(); ++v) {
        for (int adj_v: graph[v]) {
            if (v_colors[v] != v_colors[adj_v]) {
                reduced[v_colors[v]].insert(v_colors[adj_v]);
            }
        }
    }
    return reduced;
}

void update_weights(vector<double> &weigths, const vector<set<int>> &reduced) {
    for (int v = reduced.size() - 1; v >= 0; --v) {
        for (int adj_v: reduced[v]) {
            weigths[v] = min(weigths[v], weigths[adj_v]);
        }
    }
}

random_device rd;
mt19937 gen(rd());
uniform_real_distribution<double> dist(0.0, 1.0);

vector<int> nearly_reachable_degrees(const vector<set<int>> &reduced, const vector<vector<int>> &components_order,
                                     const int &iterations) {
    int N = reduced.size();
    vector<double> weights(N), weight_sums(N);
    weight_sums.assign(N, 0.0);

    for (int iteration = 0; iteration < iterations; ++iteration) {
        for (int i = 0; i < N; ++i) {
            weights[i] = dist(gen);
            int size = components_order[i].size();
            for (int count = 1; count < size; ++count) {
                weights[i] = min(weights[i], dist(gen));
            }
        }

        update_weights(weights, reduced);

        for (int i = 0; i < N; ++i) {
            weight_sums[i] += log(1 - weights[i]);
        }
    }

    vector<int> reachable_degs(N);
    for (int i = 0; i < N; ++i) {
        reachable_degs[i] = round(-iterations * 1.0 / weight_sums[i]);
    }
    return reachable_degs;
}

int main() {
    int n, m;

    ifstream ifile("reachability.in");
    ifile >> n >> m;

    vector<vector<int>> graph(n), graph_t(n);

    int u, v;
    for (int i = 0; i < m; ++i) {
        ifile >> u >> v;
        graph[u - 1].push_back(v - 1);
        graph_t[v - 1].push_back(u - 1);
    }
    ifile.close();

    vector<int> order = top_sort(graph);
    vector<vector<int>> components_order = create_components(graph_t, order);
    vector<int> v_colors = color_vertices(graph, components_order);

    vector<set<int>> reduced = reduce(graph, v_colors, components_order.size());
    //reduced topological order is 0->1->2...->reduced.size()
    vector<int> reachable_degs = nearly_reachable_degrees(reduced, components_order, 50);

    ofstream ofile("reachability.out");
    for (int i = 0; i < n; ++i) {
        ofile << reachable_degs[v_colors[i]] << "\n";
    }
    ofile.close();

    return 0;
}
