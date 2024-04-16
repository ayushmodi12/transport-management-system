import requests
import itertools

login_url = 'http://127.0.0.1:5000/login'

def generate_password_combinations(length):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    password_combinations = [''.join(combination) for combination in itertools.product(alphabet, repeat=length)]
    return password_combinations

def brute_force_attack(username, max_length=4):
    for length in range(1, max_length + 1):
        print(f"Trying passwords of length {length}...")
        password_combinations = generate_password_combinations(length)
        for password in password_combinations:

            payload = {'username': username, 'password': password}
            response = requests.post(login_url, data=payload)
            
            if response.status_code == 429:
                print("Too many requests. Rate Limiter has been setup on server. Exiting...")
                return
            
            if response.status_code == 200 and response.url != login_url:
                print(f'Successful login with username: {username}, password: {password}')
                return

def main():
    username = input('Enter username: ')
    brute_force_attack(username)

if __name__ == '__main__':
    main()
