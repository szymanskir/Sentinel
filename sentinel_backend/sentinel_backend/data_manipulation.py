import pandas as pd


def get_keywords_mention_count(mentions_data: pd.DataFrame):
    mention_count = (
        mentions_data.groupby(by=["keyword", "date"]).size().reset_index(name="counts")
    )

    return mention_count


def get_sentiment_scores(mentions_data: pd.DataFrame):
    sentiment_scores = (
        mentions_data[["keyword", "date", "sentimentScore"]]
        .groupby(by=["keyword", "date"])
        .agg("mean")
        .reset_index()
    )

    return sentiment_scores
