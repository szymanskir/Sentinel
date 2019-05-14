import pandas as pd

from .data_manipulation import get_keywords_mention_count, get_sentiment_scores


def create_mentions_count_plot(mentions_data: pd.DataFrame):
    plot_data = get_keywords_mention_count(mentions_data)
    keywords = set(plot_data.keyword)

    def create_single_keyword_plot_data(keyword):
        data = plot_data[plot_data.keyword == keyword]
        return {
            "x": [str(x.to_pydatetime()) for x in data["date"]],
            "y": data["counts"].tolist(),
            "type": "scatter",
            "mode": "lines+points",
            "name": keyword,
        }

    return [create_single_keyword_plot_data(keyword) for keyword in keywords]


def create_sentiment_scores_plot(mentions_data: pd.DataFrame):
    plot_data = get_sentiment_scores(mentions_data)
    keywords = set(plot_data.keyword)

    def create_single_keyword_plot_data(keyword):
        data = plot_data[plot_data.keyword == keyword]
        return {
            "x": [str(x.to_pydatetime()) for x in data["date"]],
            "y": data["sentimentScore"].tolist(),
            "type": "scatter",
            "mode": "lines+points",
            "name": keyword,
        }

    return [create_single_keyword_plot_data(keyword) for keyword in keywords]
