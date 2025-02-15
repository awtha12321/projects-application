import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


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


def helper_for_transition_model(nlink, ncorpus, damping_factor):
    " will calculate the probability for going on the next links and the probability of random jump "
    " so will return two numbers "
    " transition_model should add those numbers with loop later "
    random_jump_factor = 1 - damping_factor
    following_link = damping_factor / nlink
    random_jump = random_jump_factor / ncorpus
    return following_link, random_jump

def add_probability_each_page(corpus, page, following_link, random_jump):
    " use loop to to add and return the dictionary "
    output_format = {}
    for page_ in corpus: # this should not be the corpus ... this should be another data strcuture that contains pages "i"
        if page_ == page:
            output_format[page] = random_jump
            continue

        output_format[page_] = following_link + random_jump


    return output_format


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    """
    # PLAN
    pass # of links in that page as an argument and the total number of page in the corpus -> to helper function
    check if the page has no links then add to each page the probability for links in the corpus (for link, exclude current page)
    || add every page including currrent page random jump
    if page has links -> add probability to links in the dict + add them random jump too (include current page) ||
    ncorpus = # of links + 1
    """
    page_i_easy_access = {}
    for page_ in corpus:
        for link in corpus[page_]:
            if link not in page_i_easy_access:
                page_i_easy_access[link] = []
            if page_ not in page_i_easy_access[link]:
                page_i_easy_access[link].append(page_)

    if len(corpus[page]) == 0:
        following_link, random_jump = helper_for_transition_model((len(corpus)-1), len(corpus), damping_factor)
        result = add_probability_each_page(corpus, page, following_link, random_jump)
        return result

    following_link, random_jump = helper_for_transition_model((len(corpus[page])), (len(corpus)), damping_factor)
    new_corpus = {}
    new_corpus[page] = {}
    for page_ in corpus[page]:
        new_corpus[page_] = {}
    print(f"page {page}")
    print(f"corpus: {corpus}")
    print(f"new_corpus: {new_corpus}")
    result = add_probability_each_page(new_corpus, page, following_link, random_jump)
    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    """
    PLAN
    HAVE TO DO ALL OF THIS IN A LOOP OF "n"
    1. pick the page among corpus at random for the first time
    2. send the previous page to transition model and we will get probabilities back
        2.1 choose one page among them with random library and given probabilities
    """

    result = {}
    for key in corpus:
        result[key] = 0

    for i in range(n):
        if i == 0:
            first_page = random.choice(list(corpus.keys()))
            result[first_page] = 1/n
            new_generate_page = transition_model(corpus, first_page, damping_factor)
            continue

        pages = list(new_generate_page.keys())
        probabilities = list(new_generate_page.values())
        chosen_page = random.choices(pages, weights=probabilities)[0]
        result[chosen_page] += 1
        new_generate_page = transition_model(corpus, chosen_page, damping_factor)

    for page_ in result:
        result[page_] = result[page_] / n

    return result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    """
    # PLAN
    1. assign 1/N to every page
    2. while CONVERGE(TRUE):
        2.1 apply the equation
            NOTE: use the newly created data structure for summation thing ( might have to use numpy )
            still might have to use loop but using the data strcuture makes it easier to get access to pages "i" that link to page "p"
        2.2 if the value does not change ( converge ) then stop the loop
            NOTE: have to repeat till each page does not change its value by more than 0.001 ( so i have to check if new value and current value have diff of 0.001)
            if there is a first sign that value is not changing anymore, count += 1 || if count == 2 times the corpus length then we can stop cuz they are not changing anymore
    """

    """
    #EQUATION EXPLAINED
    1. for the summartion sign -> we have to gather all the pages that is linked to current page that we are looping
        how? we have to loop the key's values and if the key's values includes "p" then get that key but looking it up everytime can be time consuming
            so create another data structure for each page and then its values are pages "i"
            OR we create the first loop for this data first.
    """


    # have to think about the best efficient way to create each page and their page "i" that links to page "p"
    # rough exmaple: "1.html": "3.html" | 2.html: 1.html, 3.html, 4.html then if we wanna get page "i" of 1.html then exclude 1.html key then
    # we will add 2.html cuz in its links, it has 1.html

    page_i_easy_access = {}

    for page_ in corpus:
        for link in corpus[page_]:
            if link not in page_i_easy_access:
                page_i_easy_access[link] = []
            if page_ not in page_i_easy_access[link]:
                page_i_easy_access[link].append(page_)


    converge = True
    N = len(corpus)
    d = damping_factor
    pagerank = {}
    converge_count = 0

    for page_ in corpus:
        pagerank[page_] = 1/N


    # print(corpus)
    # print(page_i_easy_access)
    # print(pagerank)

    while converge:
        old_pagerank = pagerank.copy()
        for page_ in page_i_easy_access:
            sum_of_page_i = 0
            if len(page_i_easy_access[page_]) == 0:
                continue
            else:
                for linked_to in page_i_easy_access[page_]:
                    if len(corpus[linked_to]) == 0:
                        divide = len(corpus)
                    else:
                        divide = len(corpus[linked_to])
                    sum_of_page_i += (pagerank[linked_to] / divide)

            page_score = ((1-d)/N) + (d*sum_of_page_i)
            pagerank[page_] = page_score

        diff = []
        for page_ in pagerank:
            diff.append(abs(old_pagerank[page_] - pagerank[page_]))


        if max(diff) <= 0.001:
            converge_count += 1
            if converge_count == (N*2):
                converge = False
                print(sum(pagerank.values()))

    return pagerank


if __name__ == "__main__":
    main()
