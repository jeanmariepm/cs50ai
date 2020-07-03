import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 100000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    target_size = len(corpus[page])
    if target_size > 0:
        model = {key: (1 - damping_factor) / (len(corpus)) for key in corpus.keys()}
        for target in corpus[page]:
            model[target] += damping_factor / target_size
    else:
        model = {key: 1 / (len(corpus)) for key in corpus.keys()}
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = {k: 0 for k in corpus.keys()}
    page = random.choice(list(corpus.keys()))
    for i in range(n):
        model = transition_model(corpus, page, damping_factor)
        page = random.choices(list(model.keys()), list(model.values()), k=1)[0]
        rank[page] += 1 / n
    return rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = {k: 1 / len(corpus) for k in corpus.keys()}
    for page in corpus.keys():
        links = corpus[page]
        # print(f'p={page}, l = {list(links)}')
        if len(links) == 0:
            links = set()
            for other_page in corpus.keys():
                if page != other_page:
                    links.add(other_page)
            corpus[page] = links

    stable = False
    while not stable:
        stable = True
        tmp_rank = rank.copy()
        for page in corpus.keys():
            assert (0 <= rank[page] <= 1)
            new_rank = 0
            for ref_page in corpus.keys():
                if page not in corpus[ref_page]:
                    continue
                else:
                    num_links = len(corpus[ref_page])
                    contr_rank = damping_factor * rank[ref_page] / num_links
                    new_rank += contr_rank
                    # print(f'{page}<-{ref_page}:{num_links},{rank[ref_page]},{contr_rank}')
            new_rank += (1 - damping_factor) / len(corpus)
            # print(f'{page} being assigned {new_rank}')

            rank_delta = rank[page] - new_rank
            if rank_delta > 0.005 or rank_delta < -0.005:
                stable = False
            tmp_rank[page] = new_rank
        rank = tmp_rank.copy()
        # print(f'Ranks after iteration: {list(rank.values())}')
    return rank


if __name__ == "__main__":
    main()
