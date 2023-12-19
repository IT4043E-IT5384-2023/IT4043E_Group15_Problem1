from twitter.data_processing import clean_data
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean Twitter data")
    parser.add_argument('--dry_run', action="store_const", default=False, const=True)
    
    args, _ = parser.parse_known_args()
    
    clean_data(args.dry_run)