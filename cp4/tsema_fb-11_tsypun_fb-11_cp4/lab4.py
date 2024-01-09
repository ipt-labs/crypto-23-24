from exchangeProto import ExchangeProtocol
from RSA import RSA

import server_com


YELLOW = "\u001b[33m"
BOLD = "\u001b[1m"
RESET = "\u001b[0m"


def main():
    e = 2 ** 16 + 1
    ep = ExchangeProtocol(Alice=RSA(e, 512, "Alice"), 
                          Bob=RSA(e, 512, "Bob")
    )

    ep.startExchange()
    enc = ep.sendKey(ep.Bob.getPubKey(), ep.Alice, ep.Bob, 1337228322)
    key = ep.receiveKey(ep.Alice.getPubKey(), ep.Alice, ep.Bob, enc)

    print(key)


if __name__ == "__main__":
    com_str = "Communication with test server"
    print(f"\n{YELLOW}{BOLD}+{40*'-'}+\n|{com_str:^40}|\n+{40*'-'}+{RESET}")
    server_com.main()

    ep_str = "Exchange Protocol"
    print(f"\n\n{YELLOW}{BOLD}+{30*'-'}+\n|{ep_str:^30}|\n+{30*'-'}+{RESET}\n\n")
    main()
    