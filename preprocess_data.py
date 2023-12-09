from twitter.data_processing import encode_users, encode_tweets
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Profile scraper for Twitter")
    parser.add_argument('--del_temp', action="store_const", default=False, const=True)
    
    args, _ = parser.parse_known_args()
    
    encode_tweets()
    encode_users()

    if args.del_temp:
        pass