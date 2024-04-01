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
    "slots",
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
TIMEOUT = 1

# API templates
ALL_MARKETS_URL = "https://api.manifold.markets/v0/markets"
MARKET_DESCRIPTION_TEMPLATE = "https://api.manifold.markets/v0/market/{market_id}"

# helper functions
def get_description(market_id):
    """
    Gets a description for a Manifold market
    """
    time.sleep(DELAY)

    my_url = MARKET_DESCRIPTION_TEMPLATE.format(market_id = market_id)
    response = requests.get(my_url, timeout = TIMEOUT)
    response.raise_for_status()
    return response.json()["textDescription"]

def check_word_list(phrase, word_list):
    """
    Checks word lists
    """
    for term in word_list:
        if term.lower() in phrase.lower():
            return True
    return False

def check_market_list(market_list, bad_words, good_words, checkin = 42):
    """
    Checks a list of markets for bad and good words
    Use the checkin parameter to get status updates
    """
    # input validation
    assert isinstance(market_list, list)
    assert isinstance(bad_words, list)
    assert isinstance(good_words, list)
    assert isinstance(checkin, int)
    assert checkin >= 1

    # variables to build up
    bad_markets = []
    good_markets = []

    # main loop
    for i, market in enumerate(market_list):
        # extract
        title = market["question"]
        market_id = market["id"]
        market_description = get_description(market_id)

        # check word lists
        if check_word_list(title, bad_words) or check_word_list(market_description, bad_words):
            bad_markets.append(market)
        if check_word_list(title, good_words) or check_word_list(market_description, good_words):
            good_markets.append(market)

        # checkin
        if i % checkin == 0:
            print(f"{i} markets checked!")

    # return
    return (bad_markets, good_markets)

# main code
if __name__ == "__main__":
    # sanity check
    print("Hello world")

    # get all markets
    r = requests.get(ALL_MARKETS_URL, timeout = TIMEOUT)
    r.raise_for_status()
    my_markets = r.json()
    result = check_market_list(my_markets, bad_words = BAD_WORDS, good_words = GOOD_WORDS)
