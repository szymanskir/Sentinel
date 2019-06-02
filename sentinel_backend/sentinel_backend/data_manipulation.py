import pandas as pd


def get_keywords_mention_count(mentions_data: pd.DataFrame):
    if len(mentions_data) == 0:
        return pd.DataFrame(columns=["keyword", "origin_date", "counts"])

    return (
        mentions_data.groupby(by=["keyword", "origin_date"])
        .size()
        .reset_index(name="counts")
    )


def get_sentiment_scores(mentions_data: pd.DataFrame):
    if len(mentions_data) == 0:
        return pd.DataFrame(columns=["keyword", "origin_date", "sentiment_score"])

    return (
        mentions_data[["keyword", "origin_date", "sentiment_score"]]
        .groupby(by=["keyword", "origin_date"])
        .agg("mean")
        .reset_index()
    )
