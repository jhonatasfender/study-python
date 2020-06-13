from finding.args import Args
from finding.search.search import Search


def main():
    args = Args()
    Search(args.parse())


if __name__ == '__main__':
    main()
