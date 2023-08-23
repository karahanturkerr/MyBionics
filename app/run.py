from src.my_bionics import MyBionics
import argparse

from src.training_process import TrainingProcess


training_process = TrainingProcess()


def main():
    parser = argparse.ArgumentParser(description="A simple CLI program with command handling.")

    subparsers = parser.add_subparsers(title="Commands", dest="command")

    subparsers.add_parser("training", help="Execute command 1")
    subparsers.add_parser("face_detect_export", help="Execute command 2")
    subparsers.add_parser("start", help="Execute command 3")

    args = parser.parse_args()

    if args.command == "training":
        training_process.get_image_and_labels()
    elif args.command == "face_detect_export":
        training_process.face_detect_data_export()
    elif args.command == "start":
        my_bionics = MyBionics()
        my_bionics.start()
    else:
        print("Invalid command")


if __name__ == "__main__":
    main()
