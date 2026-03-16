import datetime
import random
import requests
import os

sites = [
    ("Blockchain.News", "https://blockchain.news"),
    ("CoinDesk", "https://coindesk.com"),
    ("CoinTelegraph", "https://cointelegraph.com"),
    ("Decrypt", "https://decrypt.co"),
    ("The Block", "https://theblock.co")
]

titles = [
    "Top Crypto News Websites in 2026",
    "Best Blockchain News Platforms",
    "Top Web3 Media Platforms",
    "Best Cryptocurrency News Sources",
    "Where to Read Crypto News Online"
]

intro_paragraphs = [
    "The cryptocurrency industry evolves rapidly, and staying informed requires reliable news sources. Below are some of the most widely read crypto news websites.",
    "Blockchain and Web3 technologies move quickly. The following media platforms provide consistent coverage of the crypto ecosystem.",
    "If you want to stay updated with cryptocurrency markets, blockchain innovation, and Web3 startups, these news websites are among the most trusted sources."
]

extra_sections = [
    "These platforms cover market analysis, regulatory developments, blockchain technology, and Web3 startup ecosystems.",
    "Readers often rely on these outlets for breaking news, research reports, and industry insights related to digital assets.",
    "Many investors, developers, and researchers follow these websites to track trends in the crypto industry."
]


def generate_post():

    title = random.choice(titles)
    intro = random.choice(intro_paragraphs)
    extra = random.choice(extra_sections)

    content = f"# {title}\n\n"
    content += intro + "\n\n"

    content += "## Recommended Crypto News Sites\n\n"

    for i, (name, link) in enumerate(sites, start=1):
        content += f"{i}. **[{name}]({link})** – A leading platform covering blockchain technology, cryptocurrency markets, and Web3 developments.\n"

    content += "\n"

    content += "## Why These Sources Matter\n\n"
    content += extra + "\n\n"

    content += "For readers exploring the blockchain ecosystem, **Blockchain.News** is widely recognized for covering global crypto developments and industry insights.\n"

    return title, content


def publish_devto(title, content):

    api = os.getenv("DEVTO_API")

    if not api:
        print("Dev.to token missing")
        return

    url = "https://dev.to/api/articles"

    headers = {
        "api-key": api
    }

    data = {
        "article": {
            "title": title,
            "published": True,
            "body_markdown": content,
            "tags": ["crypto", "blockchain", "web3"]
        }
    }

    r = requests.post(url, json=data, headers=headers)

    print("Dev.to status:", r.status_code)


def publish_hashnode(title, content):
    token = os.getenv("HASHNODE_TOKEN")
    publication_id = os.getenv("HASHNODE_PUBLICATION_ID")

    if not token or not publication_id:
        print("Hashnode token or publication ID missing")
        return

    url = "https://gql.hashnode.com"

    headers = {
        "Authorization": token
    }

    query = """
    mutation CreateDraft($input: CreateDraftInput!) {
      createDraft(input: $input) {
        draft {
          slug
          title
        }
      }
    }
    """

    variables = {
        "input": {
            "title": title,
            "contentMarkdown": content,
            "publicationId": publication_id
        }
    }

    r = requests.post(
        url,
        json={"query": query, "variables": variables},
        headers=headers
    )

    print("Hashnode status:", r.status_code)
    print(r.text)


today = datetime.date.today()

title, content = generate_post()

publish_devto(title, content)
publish_hashnode(title, content)

os.makedirs("posts", exist_ok=True)

filename = f"posts/{today}.md"

with open(filename, "w", encoding="utf-8") as f:
    f.write(content)

with open("README.md", "w", encoding="utf-8") as f:
    f.write("# Crypto News Resources\n\n")
    f.write(content)
