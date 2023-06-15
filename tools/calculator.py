import argparse
from pyport.lib.black_scholes import black_scholes


def main():
    parser = argparse.ArgumentParser(description='Option Calculator')
    parser.add_argument('--S', type=float, help='Current price of the underlying asset')
    parser.add_argument('--K', type=float, help='Strike price of the option')
    parser.add_argument('--r', type=float, help='Risk-free interest rate')
    parser.add_argument('--T', type=float, help='Time to expiration (in years)')
    parser.add_argument('--sigma', type=float, help='Volatility of the underlying asset')
    parser.add_argument('--q', type=float, help='Dividend rate of the underlying asset')
    parser.add_argument('--type', choices=['call', 'put'], help='Type of the option')
    args = parser.parse_args()

    if None in (args.S, args.K, args.r, args.T, args.sigma, args.q, args.type):
        parser.error('Please provide all the required arguments.')

    result = black_scholes(args.S, args.K, args.r, args.T, args.sigma, args.q, args.type)
    print(result)

if __name__ == '__main__':
    main()
