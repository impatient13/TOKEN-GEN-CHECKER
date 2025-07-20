import random
import string
import requests
import time
import os
from colorama import Fore, Style, init

init(autoreset=True)

def eska_banner():
    banner = r"""
███████╗███████╗██╗  ██╗ █████╗      ██████╗ ███████╗███╗   ██╗
██╔════╝██╔════╝██║ ██╔╝██╔══██╗    ██╔════╝ ██╔════╝████╗  ██║
█████╗  ███████╗█████╔╝ ███████║    ██║  ███╗█████╗  ██╔██╗ ██║
██╔══╝  ╚════██║██╔═██╗ ██╔══██║    ██║   ██║██╔══╝  ██║╚██╗██║
███████╗███████║██║  ██╗██║  ██║    ╚██████╔╝███████╗██║ ╚████║
╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝                             
    """.strip("\n")
    print(Fore.BLUE + banner + "\n" + Style.RESET_ALL)

def generate_token():
    return (
        "NT" +
        random.choice(string.ascii_letters) +
        ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(21)) + "." +
        random.choice(string.ascii_letters).upper() +
        ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5)) + "." +
        ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(27))
    )

def get_headers(token):
    return {
        "authorization": token,
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0"
    }

def is_token_valid(token):
    try:
        response = requests.get(
            "https://discordapp.com/api/v9/users/@me/library",
            headers=get_headers(token)
        )
        match response.status_code:
            case 200:
                print(f"{Fore.BLUE}[VALID]{Fore.RESET} {token}")
                return True
            case 403:
                print(f"{Fore.YELLOW}[LOCKED]{Fore.RESET} {token}")
                return False
            case 429:
                retry_after = response.json().get("retry_after", 5)
                print(f"{Fore.MAGENTA}[RATELIMIT]{Fore.RESET} {token} - Waiting {retry_after}s")
                time.sleep(retry_after)
                return is_token_valid(token)
            case _:
                print(f"{Fore.RED}[INVALID]{Fore.RESET} {token}")
                return False
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Fore.RESET} {token} - {e}")
        return False

def main():
    eska_banner()
    try:
        cantidad = int(input(Fore.BLUE + "\nAmount to generate: " + Fore.RESET))
    except ValueError:
        print(Fore.RED + "Invalid number.")
        return

    output_path = os.path.join(os.getcwd(), "valid_token.txt")
    valid_tokens = []

    for i in range(cantidad):
        token = generate_token()
        print(f"{Fore.CYAN}[GEN]{Fore.RESET} Token {i+1}/{cantidad}: {token}")
        if is_token_valid(token):
            valid_tokens.append(token)
            with open(output_path, "a") as f:
                f.write(token + "\n")

    print(f"\n{Fore.GREEN}Finished! {len(valid_tokens)} valid tokens saved to {output_path}{Fore.RESET}")
    input(Fore.BLUE + "\nPress Enter to exit...")

if __name__ == "__main__":
    main()
