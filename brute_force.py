import crypt
import multiprocessing as mp


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


def read_file(url):
    file = open(url, 'r')
    content = file.readlines()
    file.close()
    return content


def main():
    pool = mp.Pool(mp.cpu_count())

    hash = '$6$dlflg0s6vwXmt0Ip$HVmq5nAwAWFdMWfpvHZPbKU1A7y4jadrUn9J5.McKWNChBljVCzcdlenWekibdeegZuQdlYIHTj8Ax12TXKNH/'
    wordlist = read_file("wordlist.txt")

    result = pool.apply(brute_force, args=(wordlist, hash))
    pool.close()

    if result != '':
        print(result)
    else:
        print("password not found")


if __name__ == '__main__':
    main()
