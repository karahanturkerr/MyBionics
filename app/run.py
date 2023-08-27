from src.my_bionics import MyBionics
import argparse



def main():
    parser = argparse.ArgumentParser(description="A simple CLI program with command handling.")

    subparsers = parser.add_subparsers(title="Commands", dest="command")

    subparsers.add_parser("start", help="Execute command 3")

    args = parser.parse_args()

    if args.command == "start":
        my_bionics = MyBionics()
        my_bionics.start()
    else:
        print("Invalid command")


if __name__ == "__main__":
    main()
