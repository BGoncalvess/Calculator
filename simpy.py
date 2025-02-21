from sympy import simplify, cos, sin
import argparse

parser = argparse.ArgumentParser(description='Sympy test')
parser.add_argument("--var_x", "-x", help="Test variable", type=int)
parser.add_argument("--var_y","-y", help="Test variable", type=int)

args = parser.parse_args()

print(simplify((args.var_x)**2 + (args.var_y)**2))