from needle_drop_review_collector import NeedleDropReviewCollector

# You need to get your own YouTube API key from Google's Dev Console.
# And put in a file or make a local variable called API_KEY.
from your_api_key import API_KEY


def main():
    if API_KEY:
        NeedleDropReviewCollector(API_KEY).run()
    else:
        print('You need an YouTube API key.')

    return 0


if __name__ == "__main__":
    main()
