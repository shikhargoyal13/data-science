# text_splitter_cli.py
def split_text(text, mode, custom_char=None):
    if mode == "1":
        return text.split(".")
    elif mode == "2":
        return text.split()
    elif mode == "3" and custom_char:
        return text.split(custom_char)
    else:
        return [text]

def cli_main():
    print("=== Text Splitter CLI Tool ===")
    paragraph = input("Enter a paragraph:\n")

    print("\nHow do you want to split the text?")
    print("1. By sentence (period '.')")
    print("2. By word (space ' ')")
    print("3. By custom character")
    mode = input("Enter choice (1/2/3): ")

    custom_char = None
    if mode == "3":
        custom_char = input("Enter custom character to split by: ")

    split_items = split_text(paragraph, mode, custom_char)
    split_items = [item.strip() for item in split_items if item.strip()]

    print(f"\nSplit Result ({len(split_items)} items):")
    for i, item in enumerate(split_items, 1):
        print(f"{i}. {item}")

    search = input("\nDo you want to search for a word? (y/n): ")
    if search.lower() == "y":
        keyword = input("Enter word to search: ")
        found = False
        for item in split_items:
            if keyword.lower() in item.lower():
                found = True
                break
        print(f"'{keyword}' found in list: {found}")

if __name__ == "__main__":
    cli_main()
