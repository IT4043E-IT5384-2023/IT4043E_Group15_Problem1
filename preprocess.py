from twitter.data_processing import preprocess_data
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess Twitter data for ML")
    parser.add_argument('--dry_run', action="store_const", default=False, const=True)
    
    args, _ = parser.parse_known_args()
    
    preprocess_data(args.dry_run)