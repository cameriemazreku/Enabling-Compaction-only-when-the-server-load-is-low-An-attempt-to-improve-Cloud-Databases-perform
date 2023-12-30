import redis
import json
import threading
import subprocess
def get_huge_pages_free():
    try:
        # Run the command and capture the output
        meminfo_output = subprocess.check_output(['grep', 'HugePages_Rsvd', '/proc/meminfo'])

        # Decode the bytes to string
        meminfo_output_str = meminfo_output.decode('utf-8')

        # Split the output into lines
        lines = meminfo_output_str.split('\n')

        # Find the line containing HugePages_Free
        for line in lines:
            if 'HugePages_Rsvd' in line:
                _, huge_pages_free = line.strip().split(':')
                return int(huge_pages_free.split()[0])

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    return None

def worker(start, end, r, key_template, value):
    pipe = r.pipeline()
    for i in range(start, end):
        key = key_template.format(i)
        val = json.dumps(value)
        pipe.set(key, val)

        if i % 100 == 0:  # Execute every 10,000 commands
            pipe.execute()
            after_create_huge_pages_rsvd = get_huge_pages_free()
            print("HugePages_Rsvd after creating table: {}".format(after_create_huge_pages_rsvd))
            #print(f"{i} entries inserted by {threading.current_thread().name}")

    # Execute any remaining commands in the pipeline
    pipe.execute()

def main():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True, health_check_interval=30)
    number_of_entries = 600000000
    key_template = "myFirstKey_{}"
    value = {
        "name": "John Doe",
        "age": 40,
        "address": "107-39 165th street, Lawrenceville, GA 205664",
        "occupation": "uNEMPLOYED",
        "Marraige status": "Single"
    }

    num_threads = 1000 # You can adjust the number of threads
    threads = []

    # Calculate the range of entries for each thread
    entries_per_thread = number_of_entries // num_threads

    for i in range(num_threads):
        start = i * entries_per_thread
        end = (i + 1) * entries_per_thread if i < num_threads - 1 else number_of_entries

        thread = threading.Thread(target=worker, args=(start, end, r, key_template, value), name=f"Thread-{i+1}")
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    after_create_huge_pages_free = get_huge_pages_free()
    print("HugePages_Free after creating table: {}".format(after_create_huge_pages_free))

if __name__ == "__main__":
    main()

