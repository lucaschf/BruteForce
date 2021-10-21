import crypt


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
    wordlist = read_file("C://Users//lucas//Desktop//wordlist.txt")
    result = brute_force(wordlist,
                         '$6$.FdDGttw$d/0si3x4ujcbbWIctsbxmqNWrFgrBCjIblzv7aPJWkXxL0Iak9T.wD3pVPGa6qKDW0rhNLXPyzNHMzho.Nkgc1')
    if result != '':
        print(result)
    else:
        print("senha não encontrada");


if __name__ == '__main__':
    main()
