import re

class LinkProcessor:
    def __init__(self, filename='links.txt', rtf_filename=None):
        self.filename = filename
        self.rtf_filename = rtf_filename  # Optional RTF filename
        self.links = []  # Stores all extracted links
        self.twitter_links = []  # Stores links containing "twitter"
        self.youtube_links = []  # Stores links containing "youtube"
        self.wiki_links = []  # Stores links containing "wikipedia"
        self.book_links = []  # Stores links to Goodreads
        self.other_links = []  # Stores all other links

    def extract_links(self, text):
        """Extracts URLs from text using regular expressions."""
        url_pattern = r'https?://[^\s]+'
        return re.findall(url_pattern, text)

    def extract_hyperlinks_from_rtf(self):
        """Extracts hyperlinks from an RTF file."""
        if self.rtf_filename:
            hyperlink_pattern = r'HYPERLINK\s*"([^"]+)"'
            with open(self.rtf_filename, 'r', errors='ignore') as file:
                content = file.read()
                extracted_hyperlinks = set(re.findall(hyperlink_pattern, content))
                for link in extracted_hyperlinks:
                    self.categorize_link(link)
        else:
            print("No RTF filename provided.")

    def categorize_link(self, link):
        """Categorizes a single link."""
        if "twitter" in link:
            self.twitter_links.append(link)
        elif "youtube" in link:
            self.youtube_links.append(link)
        elif "wikipedia" in link:
            self.wiki_links.append(link)
        elif "goodreads" in link:
            self.book_links.append(link)
        else:
            self.other_links.append(link)

    def read_links(self):
        """Reads and categorizes links from a text file."""
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    extracted_links = self.extract_links(line)
                    for link in extracted_links:
                        self.categorize_link(link)
        except FileNotFoundError:
            print(f"The file {self.filename} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def print_links(self):
        """Prints all the links stored in respective lists."""
        categories = [
            ("Twitter Links:", self.twitter_links),
            ("YouTube Links:", self.youtube_links),
            ("Wikipedia Links:", self.wiki_links),
            ("Goodreads Links:", self.book_links),
            ("Other Links:", self.other_links),
        ]
        for title, links in categories:
            print(title)
            for link in links:
                print(link)

# Example usage
if __name__ == "__main__":
    processor = LinkProcessor(rtf_filename='hypers.rtf')  # Specify the RTF file here
    processor.extract_hyperlinks_from_rtf()
    processor.print_links()