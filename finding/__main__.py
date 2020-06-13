from finding.args import Args
from finding.search.search import Search

if __name__ == '__main__':
    args = Args()
    Search(args.parse())
