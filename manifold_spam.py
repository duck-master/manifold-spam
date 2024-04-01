"""
A primitive spam filter for Manifold Markets
"""
# imports
import time
import requests

# hardcoding bad words
BAD_WORDS = [
    "nhà cái",
    "cược",
    "iddaa",
    "bahis",
    "bookmaker",
    "casino",
    #"slots",   # false positives
    "omegle",
    "rainbow friends",
    "heardle",
    "erectile dysfunction",
    "sexual dysfunction",
    "cbd gummies",
    "keto gummies",
    "ChatGPT po Polsku",
    "ChatGPT Deutsch",
    "ChatGPT Français",
    "nigger",
    "tranny",
    "trannies",
    "retard",
    "faggot"
    ]

# hardcoding good words (mostly as a sanity check)
GOOD_WORDS = [
    "subsidized",
    "presidential",
    "election",
    "global",
    "worldwide",
    "technology",
    "metaculus",
    "polymarket",
    "CO2",
    "Donald Trump",
    "Joe Biden",
    "GPT"
]

# seconds to delay (to avoid rate limiting)
DELAY = 0.1

# timeout (to avoid code hanging)
TIMEOUT = 5

# API templates
ALL_MARKETS_URL = "https://api.manifold.markets/v0/markets"
MARKET_DESCRIPTION_TEMPLATE = "https://api.manifold.markets/v0/market/{market_id}"

# helper functions
def get_detailed_market_data(market_id):
    """
    Gets a description for a Manifold market
    """
    time.sleep(DELAY)

    my_url = MARKET_DESCRIPTION_TEMPLATE.format(market_id = market_id)
    response = requests.get(my_url, timeout = TIMEOUT)
    response.raise_for_status()
    return response.json()

def check_word_list(phrase, word_list):
    """
    Checks a phrase against word lists
    """
    for term in word_list:
        if term in phrase or term.lower() in phrase:
            return True
    return False

def augment_market_list(market_list, checkin = 42):
    """
    Returns a list of markets with descriptions
    """
    assert isinstance(market_list, list)
    result = []

    # main loop
    for i, market in enumerate(market_list):
        market_id = market["id"]
        result.append(get_detailed_market_data(market_id))

        # checkin
        if checkin:
            if i % checkin == 0:
                print(f"{i} markets scraped")

    # return
    return result

def check_market_list(market_list, word_list, checkin = None):
    """
    Checks a list of markets for bad and good words
    Use the checkin parameter to get status updates
    NOTE: this assumes that t
    """
    # input validation
    assert isinstance(market_list, list)
    assert isinstance(word_list, list)
    assert isinstance(checkin, (int, type(None)))
    assert checkin >= 1

    # variable to build up
    result = []

    # main loop
    for i, market in enumerate(market_list):
        # extract
        title = market["question"]
        description = market["textDescription"]

        # check word lists
        if check_word_list(title, word_list) or check_word_list(description, word_list):
            result.append(market)

        # checkin
        if checkin:
            if i % checkin == 0:
                print(f"{i} markets checked!")

    # return
    return result

# main code
if __name__ == "__main__":
    # sanity check
    print("Hello world")

    # get all markets
    r = requests.get(ALL_MARKETS_URL, timeout = TIMEOUT)
    r.raise_for_status()
    my_markets = r.json()

    # augment market list
    print("Scraping market descriptions...")
    my_augmented_markets = augment_market_list(my_markets)

    # check results (TODO)
    bad_markets = check_market_list(my_markets, BAD_WORDS)
    print(f"{len(bad_markets)} bad markets found")
    good_markets = check_market_list(my_markets, GOOD_WORDS)
    print(f"{len(good_markets)} good markets found")
