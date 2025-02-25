#include <iostream>
#include <fstream>
#include <thread>
#include <atomic>
#include <vector>
#include <tuple>
#include <array>

using namespace std;

const int NUM_THREADS = 4; // Number of threads
const int NUM_HASHBITS = 3; // Number of hash bits
const int NUM_BUCKETS = 1 << NUM_HASHBITS; // Number of buckets
const int DATA_SIZE = 20; // Size of the data

// Use individual atomic integers instead of atomic array
array<atomic<int>, NUM_BUCKETS> counter;

vector<tuple<int64_t, int64_t>> get_data_given_n(int n) {
  vector<tuple<int64_t,int64_t>> data(n);
  for (int64_t i = 0; i < n; i++) {
    data[i] = tuple<int64_t, int64_t>(i+1, i+1);
  }
  return data;
}

/**
 * Get the partition for a number.
 * @param n The number to get the partition for.
 * @return The partition for the number.
 */
int get_partition(int64_t n) {
  return n % NUM_BUCKETS;
}

int increment_buffer_counter(int id) {
    // Atomically increment and return previous value
    return counter[id]++;
}

/**
 * Compute the chunk size for each thread.
 * @param data_size The size of the data.
 * @return The chunk size for each thread to take.
 */
int compute_input_chunk_size(int data_size) {
  return data_size / NUM_THREADS;
}

void move_element(const tuple<int64_t, int64_t>& input_data, vector<vector<tuple<int64_t, int64_t>>>& buffers) {
  int partition = get_partition(get<0>(input_data));
  buffers[partition][increment_buffer_counter(partition)] = input_data;
}

/**
* Print the output vector.
* @param output The output vector to print.
*/
void print_output(const vector<vector<tuple<int64_t, int64_t>>>& output) {
  cout << "Data: [ ";
  for (int i = 0; i < output.size(); i++) {
    for (int j = 0; j < counter[i]; j++) { // Only print valid elements
      cout << "(" << get<0>(output[i][j]) << ", " << get<1>(output[i][j]) << ")"
           << ((i == output.size() - 1 && j == counter[i] - 1) ? " ]" : ", ");
    }
  }
  cout << endl;
}

void print_input(const vector<tuple<int64_t, int64_t>>& input) {
  cout << "Data: [ ";
  for (int i = 0; i < input.size(); i++) {
    cout << "(" << get<0>(input[i]) << ", " << get<1>(input[i]) << ")" << (i == input.size() - 1 ? " ]" : ", ");
  }
  cout << endl;
}

/**
* Main function to run the program.
* @return The exit status of the program.
*/
int main() {
  // Initialize counters to 0
  for (int i = 0; i < NUM_BUCKETS; i++) {
    counter[i] = 0;
  }

  auto data = get_data_given_n(DATA_SIZE);

  print_input(data);

  int chunk_size = compute_input_chunk_size(DATA_SIZE);

  vector<thread> threads;
  vector<vector<tuple<int64_t, int64_t>>> buffers(NUM_BUCKETS, vector<tuple<int64_t, int64_t>>(DATA_SIZE));

  for (int i = 0; i < NUM_THREADS; i++) {
    int start = i * chunk_size;
    int end = (i == NUM_THREADS - 1) ? DATA_SIZE : start + chunk_size;
    threads.push_back(thread([start, end, &data, &buffers]() {
      for (int j = start; j < end; j++) {
        move_element(data[j], buffers);
      }
    }));
  }

  // Wait for all threads to complete
  for (auto& t : threads) {
    t.join();
  }

  print_output(buffers);

  return 0;
}