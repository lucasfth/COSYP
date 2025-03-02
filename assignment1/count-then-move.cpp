/**
 * This program counts the number of elements in each partition and then moves the elements to the correct position.
 * The program uses two passes to achieve this. The first pass counts the number of elements in each partition and the
 * second pass moves the elements to the correct position.
 * The numbers are partitioned based on the remainder of the number divided by the number of threads.
 */

#include <iostream>
#include <fstream>
#include <thread>
#include <vector>
#include <tuple>
#include <atomic>
#include <chrono>

using namespace std;
using namespace std::chrono;

const int NUM_THREADS = 8;                       // Number of threads
const int NUM_OF_HASHBITS = 8;                   // Number of hash bits
const int NUM_OF_BUCKETS = 1 << NUM_OF_HASHBITS; // Number of buckets
const int DATA_SIZE = 1 << 24;                   // Size of the data
const bool debug = false;                        // Debug flag

// Use atomic counters for thread-safe operations
array<atomic<int>, NUM_OF_BUCKETS> counter;

vector<tuple<int32_t, int32_t>> get_data_given_n(int n)
{
  vector<tuple<int32_t, int32_t>> data(n);
  for (int32_t i = 0; i < n; i++)
  {
    auto num = (i + 1) % NUM_OF_BUCKETS;
    data[i] = tuple<int32_t, int32_t>(i + 1, i + 1);
  }
  return data;
}

// Add some computation to better demonstrate multi-core benefits
void do_computation(tuple<int32_t, int32_t> &item)
{
  // Simple but non-trivial computation
  for (int i = 0; i < 50; i++)
  {
    get<1>(item) = (get<0>(item) * get<1>(item) + i) % 10000;
  }
}

/**
 * Get the partition for a number.
 * @param n The number to get the partition for.
 * @return The partition for the number.
 */
int get_partition(int32_t n)
{
  return n % NUM_OF_BUCKETS;
}

/**
 * Compute the chunk size for each thread.
 * @param data_size The size of the data.
 * @return The chunk size for each thread.
 */
int compute_chunk_size(int data_size)
{
  return data_size / NUM_THREADS;
}

/**
 * Atomically increment the counter for a bucket and return the previous value.
 */
int increment_buffer_counter(int id)
{
  return counter[id]++;
}

/**
 * Move an element to its destination buffer.
 */
void move_element(const tuple<int32_t, int32_t> &item, vector<vector<tuple<int32_t, int32_t>>> &buffers)
{
  int partition = get_partition(get<0>(item));
  int pos = increment_buffer_counter(partition);
  buffers[partition][pos] = item;
}

/**
 * Process a chunk of data with affinity to a specific CPU core.
 * This function handles both computation and data movement in a single pass.
 */
void process_chunk(int thread_id, int start, int end,
                   const vector<tuple<int32_t, int32_t>> &data,
                   vector<vector<tuple<int32_t, int32_t>>> &buffers)
{

  // Set thread affinity to specific CPU core
  cpu_set_t cpuset;
  CPU_ZERO(&cpuset);
  // Use modulo in case we have more threads than cores
  CPU_SET(thread_id % thread::hardware_concurrency(), &cpuset);
  pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset);

  for (int j = start; j < end; j++)
  {
    auto item = data[j];
    do_computation(item); // Do some actual computation
    move_element(item, buffers);
  }
}

/**
 * Print the output vector.
 * @param output The output vector to print.
 */
void print_output(const vector<vector<tuple<int32_t, int32_t>>> &buffers)
{
  cout << "Data (first 10 elements from each partition): " << endl;
  for (int i = 0; i < NUM_OF_BUCKETS; i++)
  {
    cout << "Partition " << i << " (size: " << counter[i] << "): ";
    int elements_to_print = min(10, counter[i].load());
    for (int j = 0; j < elements_to_print; j++)
    {
      cout << "(" << get<0>(buffers[i][j]) << "," << get<1>(buffers[i][j]) << ") ";
    }
    cout << endl;
  }
}

/**
 * Main function to run the program.
 * @return The exit status of the program.
 */
int main()
{
  cout << "Number of available CPU cores: " << thread::hardware_concurrency() << endl;

  // Initialize atomic counters
  for (int i = 0; i < NUM_OF_BUCKETS; i++)
  {
    counter[i] = 0;
  }

  auto data = get_data_given_n(DATA_SIZE);
  int chunk_size = compute_chunk_size(DATA_SIZE);

  vector<thread> threads;
  // Create output buffers for each partition
  vector<vector<tuple<int32_t, int32_t>>> buffers(NUM_OF_BUCKETS, vector<tuple<int32_t, int32_t>>(DATA_SIZE / NUM_OF_BUCKETS + 1));

  auto start_time = high_resolution_clock::now();

  // Launch threads to process data chunks concurrently
  for (int i = 0; i < NUM_THREADS; i++)
  {
    int start = i * chunk_size;
    int end = (i == NUM_THREADS - 1) ? DATA_SIZE : start + chunk_size;
    threads.push_back(thread(process_chunk, i, start, end, ref(data), ref(buffers)));
  }

  // Wait for all threads to complete
  for (auto &t : threads)
  {
    t.join();
  }

  auto end_time = high_resolution_clock::now();
  auto duration = duration_cast<milliseconds>(end_time - start_time);

  cout << "Processing time: " << duration.count() << " ms with " << NUM_THREADS << " threads" << endl;

  // Print results if debug flag is set
  if (debug)
  {
    print_output(buffers);
  }

  return 0;
}
