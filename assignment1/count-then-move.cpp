/**
* This program counts the number of elements in each partition and then moves the elements to the correct position.
* The program uses two passes to achieve this. The first pass counts the number of elements in each partition and the
* second pass moves the elements to the correct position.
* The numbers are partitioned based on the remainder of the number divided by the number of threads.
*/

# include <iostream>
# include <fstream>
# include <thread>
using namespace std;

const int NUM_THREADS = 4; // Number of threads
const int NUM_HASHBITS = 3; // Number of hash bits
const int NUM_BUCKETS = 1 << NUM_HASHBITS; // Number of buckets
std::vector<int> data = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20}; // Data to partition

/**
 * Get the partition for a number.
 * @param n The number to get the partition for.
 * @return The partition for the number.
 */
int get_partition(int n) {
  return n % NUM_BUCKETS;
}

/**
 * Count the number of elements in each partition.
 * @param input_data The data to count the partitions for.
 * @param local_counts The local counts for each partition.
 * @param thread_id The id of the thread.
 * @param start The start index of the data.
 * @param end The end index of the data.
 */
void count_partition(const vector<int>& input_data, vector<vector<int>>& local_counts, int thread_id, int start, int end) {
  for (int i = start; i < end; i++) {
    int partition = get_partition(input_data[i]);
    local_counts[thread_id][partition]++;
  }
}

/**
 * Compute the chunk size for each thread.
 * @param data_size The size of the data.
 * @return The chunk size for each thread.
 */
int compute_chunk_size(int data_size) {
  return data_size / NUM_THREADS;
}

/**
 * Compute the global offsets for each partition.
 * @param local_counts The local counts for each partition.
 * @param global_offsets The global offsets for each partition.
 */
void compute_offset(const vector<vector<int>>& local_counts, vector<int>& global_offsets) {
  vector<int> partition_offsets(NUM_THREADS, 0);

  for (int i = 0; i < NUM_THREADS; i++) {
    for (int j = 0; j < NUM_BUCKETS; j++) {
      partition_offsets[j] += local_counts[i][j];
    }
  }

  int offset = 0;
  for (int i = 0; i < NUM_BUCKETS; i++) {
    global_offsets[i] = offset;
    offset += partition_offsets[i];
  }
}

/**
 * Move elements to the correct position.
 * @param input_data The data to move.
 * @param output The output vector to store the elements.
 * @param local_counts The local counts for each partition.
 * @param global_offsets The global offsets for each partition.
 * @param thread_id The id of the thread.
 * @param start The start index of the data.
 * @param end The end index of the data.
 */
void move_elements(const vector<int>& input_data, vector<int>& output, const vector<vector<int>>& local_counts, vector<int> global_offsets,
                   int thread_id, int start, int end) {
  vector<int> local_offsets = global_offsets;

  // Adjust offsets to account for the other threads
  for (int i = 0; i < thread_id; i++) {
    for (int j = 0; j < NUM_BUCKETS; j++) {
      local_offsets[j] += local_counts[i][j];
    }
  }

  // Move elements to the correct position
  for (int i = start; i < end; i++) {
    int partition = get_partition(input_data[i]);
    output[local_offsets[partition]++] = input_data[i];
  }
}

/**
 * Print the output vector.
 * @param output The output vector to print.
 */
void print_output(vector<int> output) {
  cout << "Output: [ ";
  for (int i = 0; i < output.size(); i++) {
    cout << output[i] << (i == output.size() - 1 ? " ]" : ", ");
  }
  cout << endl;
}

/**
 * Main function to run the program.
 * @return The exit status of the program.
 */
int main() {
  int data_size = ::data.size(); // Size of the data

  vector<vector<int>> local_counts(NUM_BUCKETS, vector<int>(NUM_BUCKETS, 0)); // Local counts for each partition
  vector<int> global_offsets(NUM_BUCKETS, 0); // Global offsets for each partition
  vector<int> output(data_size); // Output vector to store the elements

  vector<thread> threads; // Vector to store the threads
  int chunk_size = compute_chunk_size(data_size); // Compute the chunk size for each thread

  // First pass where the number of elements in each partition is counted
  for (int i = 0; i < NUM_THREADS; i++) {
    int start = i * chunk_size; // Start index of the data
    // End index of the data - ternary is used to handle edge case of giving the last thread the remaining elements, if the data is not divisible by the number of threads
    int end = (i == NUM_THREADS - 1) ? data_size : start + chunk_size;
    // Create a thread to count the number of elements in each partition
    threads.emplace_back(count_partition, cref(::data), ref(local_counts), i, start, end);
  }

  // Wait for all threads to finish
  for (auto& th : threads) {
    th.join();
  }

  // Compute the global offsets for each partition
  compute_offset(local_counts, global_offsets);

  // Clear the threads vector before the second pass
  threads.clear();

  // Second pass where elements are moved to the correct position
  for (int i = 0; i < NUM_THREADS; i++) {
    int start = i * chunk_size; // Start index of the data
    int end = (i == NUM_THREADS - 1) ? data_size : start + chunk_size; // End index of the data
    // Create a thread to move the elements to the correct position
    threads.emplace_back(move_elements, cref(::data), ref(output), cref(local_counts), cref(global_offsets), i, start, end);
  }

  // Wait for all threads to finish
  for (auto& th : threads) {
    th.join();
  }

  // Print the output vector
  print_output(output);

  // Exit the program
  return 0;
}
