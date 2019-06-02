import pytest
from sentinel_connectors.hn_common import clean_html


@pytest.mark.parametrize(
    "text_input, expected",
    [
        ("<div>Sample Sentence.</div>", "Sample Sentence."),
        ("<div>Sample &pound Sentence.</div>", "Sample £ Sentence."),
    ],
)
def test_clean_html(text_input, expected):
    result = clean_html(text_input)
    assert result == expected
