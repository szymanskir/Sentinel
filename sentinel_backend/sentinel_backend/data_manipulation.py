import pandas as pd


def get_keywords_mention_count(mentions_data: pd.DataFrame):
    if len(mentions_data) == 0:
        return pd.DataFrame(columns=["keyword", "date", "counts"])

    return (
        mentions_data.groupby(by=["keyword", "date"]).size().reset_index(name="counts")
    )


def get_sentiment_scores(mentions_data: pd.DataFrame):
    if len(mentions_data) == 0:
        return pd.DataFrame(columns=["keyword", "date", "sentimentScore"])

    return (
        mentions_data[["keyword", "date", "sentimentScore"]]
        .groupby(by=["keyword", "date"])
        .agg("mean")
        .reset_index()
    )
