# include <iostream>
# include <fstream>
# include <thread>

using namespace std;

const int CHUNK_SIZE = 4; // Chunk size for each threads output buffer
const int NUM_THREADS = 4; // Number of threads
const int NUM_HASHBITS = 2; // Number of hash bits
const int NUM_BUCKETS = 1 << NUM_HASHBITS; // Number of buckets
const int DATA_SIZE = 20; // Size of the data

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
int get_partition(int n) {
  return n % NUM_BUCKETS;
}

/**
 * Compute the chunk size for each thread.
 * @param data_size The size of the data.
 * @return The chunk size for each thread to take.
 */
int compute_input_chunk_size(int data_size) {
  return data_size / NUM_THREADS;
}

/**
* Print the output vector.
* @param output The output vector to print.
*/
void print_output(vector<tuple<int64_t, int64_t>> output) {
  cout << "Data: [ ";
  for (int i = 0; i < output.size(); i++) {
    cout << "(" << get<0>(output[i]) << ", " << get<1>(output[i]) << ")" << (i == output.size() - 1 ? " ]" : ", ");
  }
  cout << endl;
}

/**
* Main function to run the program.
* @return The exit status of the program.
*/
int main() {
  auto data = get_data_given_n(DATA_SIZE);

  print_output(data);
  // vector<vector<int>> local_counts(NUM_THREADS, vector<int>(NUM_BUCKETS, 0)); // Initialize a 2D vector of size NUM_THREADS x NUM_BUCKETS with 0s
  // int offset = 0; // Offset for the data
  // int
}
