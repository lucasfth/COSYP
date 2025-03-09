/**
 * @param num_of_threads The number of threads used.
 * @param num_of_hashbits The number of hash bits used.
 * @param data_size The size of the data used.
 * @param filename The name of the CSV file to append metrics to.
 * @param debug The debug flag to print debug information.
 * @return The exit status of the program. Will write to the CSV file.
 */

#include <iostream>
#include <fstream>
#include <thread>
#include <atomic>
#include <vector>
#include <tuple>
#include <array>
#include <chrono>
#include <pthread.h>
#include <iomanip>
#include <sys/sysinfo.h>

using namespace std;
using namespace std::chrono;

// Define a maximum number of buckets for the atomic array
const int MAX_BUCKETS = 256;

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
 * Get the data given a number.
 * @param n The number to get the data for.
 * @return The data for the number.
 */
vector<tuple<int32_t, int32_t>> get_data_given_n(int n)
{
  vector<tuple<int32_t, int32_t>> data(n);
  for (int32_t i = 0; i < n; i++)
  {
    data[i] = tuple<int32_t, int32_t>(i + 1, i + 1);
  }
  return data;
}

/**
 * Get the partition for a number.
 * @param n The number to get the partition for.
 * @param num_of_buckets The number of buckets to use.
 * @return The partition for the number.
 */
int get_partition(int32_t n, int num_of_buckets)
{
  return n % num_of_buckets;
}

/**
 * Atomically increment the buffer counter and return the previous value.
 * @param counter The counter to increment.
 * @param id The id of the buffer counter to increment.
 */
int increment_buffer_counter(array<atomic<int>, MAX_BUCKETS> &counter, int id)
{
  return counter[id]++;
}

/**
 * Compute the chunk size for each thread.
 * @param data_size The size of the data.
 * @param num_of_threads The number of threads
 * @return The chunk size for each thread to take.
 */
int compute_input_chunk_size(int data_size, int num_of_threads)
{
  return data_size / num_of_threads;
}

/**
 * Move an element to a specific partition.
 * @param counter The counter to increment.
 * @param input_data The data to move.
 * @param buffers The buffers to move the data to.
 * @param num_of_buckets The number of buckets to use.
 */
void move_element(array<atomic<int>, MAX_BUCKETS> &counter, const tuple<int32_t, int32_t> &input_data,
                  vector<vector<tuple<int32_t, int32_t>>> &buffers, int num_of_buckets)
{
  int partition = get_partition(get<0>(input_data), num_of_buckets);
  buffers[partition][increment_buffer_counter(counter, partition)] = input_data;
}

/**
 * Process a chunk of data with affinity to a specific CPU core
 * @param counter The counter to increment.
 * @param thread_id The id of the thread.
 * @param start The start index of the chunk.
 * @param end The end index of the chunk.
 * @param data The data to process.
 * @param buffers The buffers to move the data to.
 * @param num_of_buckets The number of buckets to use.
 */
void process_chunk(array<atomic<int>, MAX_BUCKETS> &counter, int thread_id, int start, int end,
                   vector<tuple<int32_t, int32_t>> &data,
                   vector<vector<tuple<int32_t, int32_t>>> &buffers,
                   int num_of_buckets)
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
    move_element(counter, item, buffers, num_of_buckets);
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
 * Print the usage of the program.
 * @param program_name The name of the program.
 */
void print_usage(const char *program_name)
{
  cout << "Usage: " << program_name << " <num_of_threads> <num_of_hashbits> <data_size> <filename> <debug>" << endl;
  cout << "Example: " << program_name << " 8 8 16777216 metrics.csv 0" << endl;
}

/**
 * Append performance metrics to a CSV file.
 * @param filename The name of the CSV file.
 * @param num_of_threads The number of threads used.
 * @param num_of_hashbits The number of hash bits used.
 * @param num_of_buckets The number of buckets used.
 * @param data_size The size of the data used.
 * @param duration The duration of the computation.
 * @param num_cores The number of CPU cores used.
 * @param memory_used The amount of memory used.
 */
void append_metrics_to_csv(const string &filename, int num_of_threads, int num_of_hashbits, int num_of_buckets, int data_size, double duration, int num_cores, long memory_used)
{
  ofstream file;
  // open file on linux
  file.open(filename, ios_base::app);
  if (file.is_open())
  {
    file << filename << ","
         << num_of_threads << ","
         << num_of_hashbits << ","
         << num_of_buckets << ","
         << data_size << ","
         << fixed << setprecision(6) << duration << ","
         << num_cores << ","
         << memory_used << endl;
    file.close();
  }
  else
  {
    cerr << "Unable to open file: " << filename << endl;
  }
}

/**
 * Main function to run the program.
 * @return The exit status of the program.
 */
int main(int argc, char *argv[])
{
  if (argc != 6)
  {
    print_usage(argv[0]);
    return 1;
  }

  int num_of_threads = stoi(argv[1]);
  int num_of_hashbits = stoi(argv[2]);
  int data_size = stoi(argv[3]);
  string filename = argv[4];
  bool debug = stoi(argv[5]);

  int num_of_buckets = 1 << num_of_hashbits;
  if (num_of_buckets > MAX_BUCKETS)
  {
    cerr << "Error: Number of buckets exceeds maximum supported (" << MAX_BUCKETS << ")" << endl;
    return 1;
  }

  print_params(argv[0], num_of_threads, num_of_hashbits, num_of_buckets, data_size, filename, debug);

  // Use atomic counters for thread-safe operations with fixed maximum size
  array<atomic<int>, MAX_BUCKETS> counter;
  // Initialize counters to 0
  for (int i = 0; i < MAX_BUCKETS; i++)
  {
    counter[i] = 0;
  }

  auto data = get_data_given_n(data_size);
  int chunk_size = compute_input_chunk_size(data_size, num_of_threads);

  vector<thread> threads;
  vector<vector<tuple<int32_t, int32_t>>> buffers(num_of_buckets, vector<tuple<int32_t, int32_t>>(data_size / num_of_buckets + 1));

  auto start_time = chrono::high_resolution_clock::now();
  for (int i = 0; i < num_of_threads; i++)
  {
    int start = i * chunk_size;
    int end = (i == num_of_threads - 1) ? data_size : start + chunk_size;
    threads.push_back(thread(process_chunk, i, start, end, ref(data), ref(buffers)));
  }

  // Wait for all threads to complete
  for (auto &t : threads)
  {
    t.join();
  }

  auto end_time = chrono::high_resolution_clock::now();
  auto duration = chrono::duration_cast<chrono::milliseconds>(end_time - start_time);
  cout << "Processing time: " << duration.count() << " ms with " << num_of_threads << " threads" << endl;

  // Verify results by counting elements in each bucket
  vector<int> bucket_counts(num_of_buckets, 0);
  for (int i = 0; i < num_of_buckets; i++)
  {
    bucket_counts[i] = counter[i].load();
  }
  cout << "Elements per bucket: ";
  for (int i = 0; i < min(8, num_of_buckets); i++)
  {
    cout << bucket_counts[i] << " ";
  }
  cout << (num_of_buckets > 8 ? "..." : "") << endl;

  if (debug)
  {
    print_output(data);
  }

  return 0;
}