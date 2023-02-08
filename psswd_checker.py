import requests
import hashlib
# import sys


def request_api_data(query_pwd):
    url = 'https://api.pwnedpasswords.com/range/' + query_pwd
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Erreur de recupération: {res.status_code}, vérifiez l\'API et réessayez!')
    return res


def pwd_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwd_check(password):
    mdpsha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = mdpsha1[:5], mdpsha1[5:]
    response = request_api_data(first5_char)
    return pwd_leaks_count(response, tail)


def main(args):
    count = pwd_check(password)
    if count:
        print(
            f'le mot de passe "{password}" a été trouvé {count} fois... tu devrais le changer!')
    else:
        print(
            f'le mot de passe "{password}" est tranquille...pour l\'instant lol!')


# main(sys.argv[1:])
if __name__ == '__main__':
    debut = True
    while True:
        if debut:
            print("###\nVérificateur de mot de passe contre d'anciennes violations via l'API Pwned Passwords!\n###")
            print('Saisir "stop" pour quitter')
        password = input('mdp à vérifier: ')

        if password == 'stop':
            break
        else : debut = False

        main(password)
