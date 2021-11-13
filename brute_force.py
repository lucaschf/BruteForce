import crypt
import multiprocessing as mp


def main():
    pool = mp.Pool(mp.cpu_count())
    wordlist = read_file("wordlist.txt")

    # example
    # '$6$dlflg0s6vwXmt0Ip$HVmq5nAwAWFdMWfpvHZPbKU1A7y4jadrUn9J5.McKWNChBljVCzcdlenWekibdeegZuQdlYIHTj8Ax12TXKNH/'
    key = input("Hashed key: ")
    # tries to break using brute force.
    result = pool.apply(brute_force, args=(wordlist, key))
    pool.close()

    if result != '':
        print(result)
    else:
        print("password not found")


# reads the file, stores its content in memory and closes it.
def read_file(url):
    file = open(url, 'r')
    content = file.readlines()
    file.close()
    return content


# tries to break the key by comparing it with every entry in wordlist encrypted.
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


if __name__ == '__main__':
    main()
