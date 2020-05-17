from po_pollard import po_pollard
from big_little import big_little
from pohlig_hellman import pohlig_hellman, weak_pohlig_hellman
import threading
import argparse
import math


def parse_init():
    parser = argparse.ArgumentParser(description='El-Gamal.')
    parser.add_argument(
        '-y',
        type=int,
        nargs='?',
        default=None,
        help='Public key.'
    )
    parser.add_argument(
        '-g',
        type=int,
        nargs='?',
        default=None,
        help='Primitive root modulo p.'
    )
    parser.add_argument(
        '-p',
        type=int,
        nargs='?',
        default=None,
        help='Module.'
    )
    parser.add_argument(
        '-ph',
        action='store_true',
        help="If specified, generate weak parameters for pohlig-hellman algorithm."
    )
    args = parser.parse_args()
    if args.ph:
        print("Pohlig-Hellman mode is activated.")
        return args, True
    if args.y is None or args.g is None or args.p is None:
        exit("Error: a tuple (y, g, p) is required.")
    return args, False


def execute(y, g, p, method, f):
    if method == 'po_pollard':
        res = po_pollard(g, y, p)
        if type(res) == str:
            f.write(res)
        else:
            f.write("The result of the algorithm is: {}".format(res))
    elif method == 'big_little':
        t = int(p ** 0.5)
        f.write("Parameter t is chosen as: {}".format(t))
        res = big_little(g, y, p, t)
        if res:
            f.write("The result of the algorithm is: {}".format(res))
    elif method == 'pohlig_hellman':
        res = pohlig_hellman(g, y, p)
        f.write("The result of the algorithm is: {}".format(res))
    else:
        exit("Unknown method")
    return 0


if __name__ == '__main__':
    args, mode = parse_init()
    if mode:
        f_prime, m_prime, s_prime, p_small = weak_pohlig_hellman()
        print("Ferma prime:", f_prime)
        print("Mersenne prime:", m_prime)
        if s_prime:
            print("Single prime:", s_prime)
        if p_small:
            print("Small prime:", p_small)
    else:
        for method in ['po_pollard', 'big_little', 'pohlig_hellman']:
            time = None
            print("Do you want to specify time limit for attack {}?".format(method))
            is_yes = False
            while True:
                answer = input().lower()
                if answer in ['n', 'no', 'нет', 'н']:
                    break
                elif answer in ['y', 'yes', 'да', 'д']:
                    is_yes = True
                    break
                else:
                    print("Please type [yes/no]")
            if is_yes:
                print("Please write time in seconds:")
                while True:
                    time = input()
                    try:
                        time = int(time)
                    except Exception:
                        print("Use integer for time in seconds.")
                    else:
                        break
            with open('./results/' + method + '.txt', 'w') as f:
                thread = threading.Thread(target=execute, args=(args.y, args.g, args.p, method, f))
                thread.daemon = True
                thread.start()
                thread.join(time if time else int(math.log(args.p, 2) * 60 * 60 / 32) + 5 * 60)

