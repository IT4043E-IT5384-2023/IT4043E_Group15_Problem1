
from twitter.scraping import scrape
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Profile scraper for Twitter")
    parser.add_argument('--load_uids', action="store_const", default=False, const=True)
    parser.add_argument('--post_process', action="store_const", default=False, const=True) # suggest
    
    args, _ = parser.parse_known_args()

    scrape(
        load_uids=args.load_uids, 
        post_process=args.post_process
    )