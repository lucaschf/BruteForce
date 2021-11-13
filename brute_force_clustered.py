import crypt
import time

import pp

lines_per_node = 5000

lines_processed = 0
available_cpus = 0

wordlist_file = open("wordlist.txt", 'r')
lines_in_file = sum(1 for line in wordlist_file)
wordlist_file.seek(0)

reached_file_end = False
is_aborted = False


def read_file():
    chunks = []
    global reached_file_end

    while len(chunks) < available_cpus and not reached_file_end:
        words = []

        for i in range(lines_per_node):
            word = wordlist_file.readline()

            if word == "":
                reached_file_end = True
                break

            words.append(word)
        chunks.append(words)

    return tuple(chunks)


def brute_force(wordlist, key):
    try:
        broke = key.split('$')
        for line in wordlist:
            if key == str(crypt.crypt(line.rstrip(), '$' + broke[1] + '$' + broke[2])):
                return line
        return ''
    except RuntimeError:
        print('\nInvalid input. Aborting...')
        quit()


def show_progress():
    print("Working[{0:.2f}%]".format(float(lines_processed) / float(lines_in_file) * 100))


def start_cluster(key, job_server):
    global available_cpus, lines_processed, is_aborted

    if available_cpus == 0:
        print("No available processors for the task")
        is_aborted = True
        return

    print("Working. Please be patient...")

    while not reached_file_end:
        chunks = read_file()
        show_progress()

        jobs = [(chunk, job_server.submit(brute_force, (chunk, key,), (), ("crypt",))) for chunk in chunks]
        for chunk, job in jobs:
            lines_processed += len(chunk)
            if job() != "":
                print("\nDecrypted key: ", job())
                return

    print("\nFailed to decrypt\n")


def main():
    global available_cpus

    pp_servers = ("*",)
    job_server = pp.Server(ppservers=pp_servers)

    for host, cpu_count in job_server.get_active_nodes().items():
        # if host != "local" and cpu_count > 0:
        print("{} processors available from {} host.\n ".format(cpu_count, host))
        available_cpus += cpu_count

    target = "$6$dlflg0s6vwXmt0Ip$HVmq5nAwAWFdMWfpvHZPbKU1A7y4jadrUn9J5" \
             ".McKWNChBljVCzcdlenWekibdeegZuQdlYIHTj8Ax12TXKNH/"

    start_time = time.time()
    start_cluster(target, job_server)
    wordlist_file.close()

    if not is_aborted:
        print("Processing time: ", time.time() - start_time, "s")
        job_server.print_stats()


if __name__ == '__main__':
    main()
