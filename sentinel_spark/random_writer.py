import kafka
import json
from sentinel_common.mentions import Mention, HackerNewsMetadata
import random, string
from datetime import datetime
import time

KAFKA_URL = "sandbox-hdp.hortonworks.com:6667"


def ensure_topics_exist():
    all_topics = ["reddit", "twitter", "google-news", "hacker-news"]

    admin = kafka.admin.KafkaAdminClient(bootstrap_servers=[KAFKA_URL])
    client = kafka.KafkaClient([KAFKA_URL])
    existing_topics = client.topics
    topics = [
        kafka.admin.NewTopic(topic, 1, 1)
        for topic in all_topics
        if topic not in existing_topics
    ]
    admin.create_topics(topics)


producer = kafka.KafkaProducer(
    bootstrap_servers=[KAFKA_URL],
    value_serializer=lambda m: json.dumps(m).encode("utf8"),
)


s_nouns = [
    "A dude",
    "My mom",
    "The king",
    "Some guy",
    "A cat with rabies",
    "A sloth",
    "Your homie",
    "This cool guy my gardener met yesterday",
    "Superman",
]
p_nouns = [
    "These dudes",
    "Both of my moms",
    "All the kings of the world",
    "Some guys",
    "All of a cattery's cats",
    "The multitude of sloths living under your bed",
    "Your homies",
    "Like, these, like, all these people",
    "Supermen",
]
s_verbs = [
    "eats",
    "kicks",
    "gives",
    "treats",
    "meets with",
    "creates",
    "hacks",
    "configures",
    "spies on",
    "retards",
    "meows on",
    "flees from",
    "tries to automate",
    "explodes",
]
p_verbs = [
    "eat",
    "kick",
    "give",
    "treat",
    "meet with",
    "create",
    "hack",
    "configure",
    "spy on",
    "retard",
    "meow on",
    "flee from",
    "try to automate",
    "explode",
]
infinitives = [
    "to make a pie.",
    "for no apparent reason.",
    "because the sky is green.",
    "for a disease.",
    "to be able to make toast explode.",
    "to know more about archeology.",
]


def get_random_sentence():
    return " ".join(
        [
            random.choice(s_nouns),
            random.choice(s_verbs),
            random.choice(s_nouns).lower() or random.choice(p_nouns).lower(),
            random.choice(infinitives),
        ]
    )


def main():
    ensure_topics_exist()
    while True:
        sample_text = get_random_sentence()
        mention = Mention(
            text=sample_text,
            url="https://www.google.com",
            source="hacker-news",
            creation_date=datetime.utcnow(),
            download_date=datetime.utcnow(),
            metadata=HackerNewsMetadata(author="YOLO author"),
        )
        producer.send("hacker-news", mention.to_json())
        print(f"SENT: {sample_text}")
        time.sleep(random.uniform(0, 1))


if __name__ == "__main__":
    main()
