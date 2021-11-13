import math
import time
import crypt

import pp

lines_per_node = 5000

lines_processed = 0
available_cpus = 0

wordlist_file = open("wordlist.txt", "r")
lines_in_file = sum(1 for line in wordlist_file)
wordlist_file.seek(0)


def consume_file():
    chunks = []

    while len(chunks) < available_cpus:
        words = []

        for i in range(lines_per_node):
            word = wordlist_file.read()

            if word == "":
                break

            words.append(word)
        chunks.append(words)

    return tuple(chunks)


def reached_file_end():
    return wordlist_file.readline() == ""


def brute_force(wordlist, key):
    try:
        broke = key.split('$')
        for line in wordlist:
            if key == str(crypt.crypt(line.rstrip(), '$' + broke[1] + '$' + broke[2])):
                return line
        return ''
    except Exception as e:
        print('Invalid input')
        quit()


def show_progress():
    print("{0:.2f} % processed.".format(float(lines_processed) / float(lines_in_file) * 100))


def cluster(key):
    global available_cpus, lines_processed

    print("Working. Please be patient...")

    while not reached_file_end():
        show_progress()
        chunks = consume_file()

        jobs = [(chunk, job_server.submit(brute_force, (chunks, key), (), ("crypt",))) for chunk in chunks]
        for chunk, job in jobs:
            if job() != '':
                print("Decrypted key: ", job())
                return

        lines_processed += lines_per_node * available_cpus

    wordlist_file.close()


pp_servers = ("*",)
job_server = pp.Server(ncpus=0, ppservers=pp_servers)

# time.sleep(1)

for computer, cpu_count in job_server.get_active_nodes().iteritems():
    if computer != "local" and cpu_count > 0:
        print("IP: {} com {} núcleos disponíveis.".format(computer, cpu_count))
        available_cpus += cpu_count

key = "$6$.FdDGttw$d/0si3x4ujcbbWIctsbxmqNWrFgrBCjIblzv7aPJWkXxL0Iak9T.wD3pVPGa6qKDW0rhNLXPyzNHMzho.Nkgc1"

start_time = time.time()

cluster(key)

print("Processing time: ", time.time() - start_time, "s")
job_server.print_stats()