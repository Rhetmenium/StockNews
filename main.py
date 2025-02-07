import feedparser
import pyperclip

def get_news_from_sources(sources, keyword, max_results=30):
    all_news = []
    
    for rss_url in sources:
        feed = feedparser.parse(rss_url)
        
        filtered_news = [
            entry for entry in feed.entries
            if keyword.lower() in getattr(entry, 'title', '').lower() or
               keyword.lower() in getattr(entry, 'summary', '').lower() or
               keyword.lower() in getattr(entry, 'link', '').lower()
        ]
        
        all_news.extend(filtered_news)
    
    all_news = all_news[:max_results]
    
    if all_news:
        print(f"Latest news about '{keyword}':\n")
        for idx, entry in enumerate(all_news, start=1):
            print(f"{idx}. {getattr(entry, 'title', 'No title available')}")
            published_date = getattr(entry, 'published', 'No publication date available')
            print(f"   Published: {published_date}")
            print(f"   Link: {getattr(entry, 'link', 'No link available')}\n")
        
        copy_request = input("\nWould you like to copy the news? (Yes/No): ").strip().lower()
        if copy_request == 'yes':
            news_text = "\n".join([f"{getattr(entry, 'title', 'No title available')} - {getattr(entry, 'link', 'No link available')}" for entry in all_news])
            news_text += f"\n\nBased on these news, is it more likely for '{keyword}' to rise or fall in the future?"
            pyperclip.copy(news_text)
            print("\nThe news data has been copied to the clipboard.")
    else:
        print(f"No news found for '{keyword}'.")

def load_sources_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            sources = [line.strip() for line in file.readlines()]
        return sources
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []

if __name__ == "__main__":
    sources_file = 'rss_sources.txt'
    sources = load_sources_from_file(sources_file)
    
    if sources:
        keyword = input("What topic would you like to get news about? (e.g., Tesla, Apple): ")
        get_news_from_sources(sources, keyword)
    else:
        print("No sources were loaded, please check your sources file.")
