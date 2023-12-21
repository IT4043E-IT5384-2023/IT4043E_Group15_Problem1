from twitter import assembly_pipe
from twitter.config import PROFILE_PATH
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Profile scraper for Twitter")
    parser.add_argument('--crawl_data_path', type=str, default=PROFILE_PATH)
    parser.add_argument('--memory_to_disk', action="store_const", default=False, const=True)
    parser.add_argument('--infer_only', action="store_const", default=False, const=True)
    parser.add_argument('--scoring', type=str, default="roc_auc_ovo")
    
    
    args, _ = parser.parse_known_args()

    assembly_pipe(
        twitter_data = args.crawl_data_path,
        memory_to_disk = args.memory_to_disk,
        infer_only = args.infer_only,
        scoring = args.scoring
    )