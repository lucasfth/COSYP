#include <iostream>
#include <fstream>
#include <thread>
#include <atomic>
#include <vector>
#include <tuple>
#include <array>
#include <chrono>
#include <pthread.h>

using namespace std;
using namespace std::chrono;

const int NUM_THREADS = 8;                 // Number of threads
const int NUM_HASHBITS = 8;                // Number of hash bits
const int NUM_BUCKETS = 1 << NUM_HASHBITS; // Number of buckets
const int DATA_SIZE = 1 << 24;             // Size of the data
const bool debug = false;                  // Debug flag

// Use individual atomic integers instead of atomic array
array<atomic<int>, NUM_BUCKETS> counter;

// Add some computation to better demonstrate multi-core benefits
void do_computation(tuple<int32_t, int32_t> &item)
{
  // Simple but non-trivial computation
  for (int i = 0; i < 50; i++)
  {
    get<1>(item) = (get<0>(item) * get<1>(item) + i) % 10000;
  }
}

vector<tuple<int32_t, int32_t>> get_data_given_n(int n)
{
  vector<tuple<int32_t, int32_t>> data(n);
  for (int32_t i = 0; i < n; i++)
  {
    // auto num = (i + 1) % NUM_BUCKETS;
    data[i] = tuple<int32_t, int32_t>(i+1, i+1);
  }
  return data;
}

/**
 * Get the partition for a number.
 * @param n The number to get the partition for.
 * @return The partition for the number.
 */
int get_partition(int32_t n)
{
  return n % NUM_BUCKETS;
}

int increment_buffer_counter(int id)
{
  // Atomically increment and return previous value
  return counter[id]++;
}

/**
 * Compute the chunk size for each thread.
 * @param data_size The size of the data.
 * @return The chunk size for each thread to take.
 */
int compute_input_chunk_size(int data_size)
{
  return data_size / NUM_THREADS;
}

void move_element(const tuple<int32_t, int32_t> &input_data, vector<vector<tuple<int32_t, int32_t>>> &buffers)
{
  int partition = get_partition(get<0>(input_data));
  buffers[partition][increment_buffer_counter(partition)] = input_data;
}

/**
 * Process a chunk of data with affinity to a specific CPU core
 */
void process_chunk(int thread_id, int start, int end,
                   vector<tuple<int32_t, int32_t>> &data,
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
void print_output(const vector<tuple<int32_t, int32_t>> &input)
{
  cout << "Data: [ ";
  for (int i = 0; i < min(20, (int)input.size()); i++)
  {
    cout << "(" << get<0>(input[i]) << ", " << get<1>(input[i]) << ")" << (i == min(19, (int)input.size() - 1) ? " ]..." : ", ");
  }
  cout << endl;
}

/**
 * Main function to run the program.
 * @return The exit status of the program.
 */
int main()
{
  cout << "Number of available CPU cores: " << thread::hardware_concurrency() << endl;
  cout << "Number of threads: " << NUM_THREADS << endl;


  cout << "Fill counter with 0..." << endl;
  // Initialize counters to 0
  for (int i = 0; i < NUM_BUCKETS; i++)
  {
    counter[i] = 0;
  }

  cout << "Initializing data..." << endl;

  auto data = get_data_given_n(DATA_SIZE);
  cout << "Data created with size: " << data.size() << endl;
  int chunk_size = compute_input_chunk_size(DATA_SIZE);

  vector<thread> threads;
  vector<vector<tuple<int32_t, int32_t>>> buffers(NUM_BUCKETS, vector<tuple<int32_t, int32_t>>(DATA_SIZE));

  auto start_time = chrono::high_resolution_clock::now();
  cout << "Finished initializing data..." << endl;
  cout << "Processing data with " << NUM_THREADS << " threads..." << endl;
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

  auto end_time = chrono::high_resolution_clock::now();
  auto duration = chrono::duration_cast<chrono::milliseconds>(end_time - start_time);
  cout << "Processing time: " << duration.count() << " ms with " << NUM_THREADS << " threads" << endl;

  // Verify results by counting elements in each bucket
  vector<int> bucket_counts(NUM_BUCKETS, 0);
  for (int i = 0; i < NUM_BUCKETS; i++)
  {
    bucket_counts[i] = counter[i].load();
  }
  cout << "Elements per bucket: ";
  for (int i = 0; i < min(8, NUM_BUCKETS); i++)
  {
    cout << bucket_counts[i] << " ";
  }
  cout << (NUM_BUCKETS > 8 ? "..." : "") << endl;

  if (debug)
  {
    print_output(data);
  }

  return 0;
}