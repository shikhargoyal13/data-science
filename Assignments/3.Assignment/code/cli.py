# string_case_converter_cli.py

def count_vowels_consonants(text):
    vowels = "aeiouAEIOU"
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    v_count = 0
    c_count = 0

    for ch in text:
        if ch in letters:
            if ch in vowels:
                v_count += 1
            else:
                c_count += 1

    return v_count, c_count

def cli_main():
    print("=== String Case Converter Tool ===")
    sentence = input("Enter a sentence:\n")

    while True:
        print("\nChoose an operation:")
        print("1. Convert to UPPER case")
        print("2. Convert to lower case")
        print("3. Convert to Title Case")
        print("4. Reverse the sentence")
        print("5. Exit")

        choice = input("Enter choice (1-5): ")

        if choice == "1":
            result = sentence.upper()
        elif choice == "2":
            result = sentence.lower()
        elif choice == "3":
            result = sentence.title()
        elif choice == "4":
            result = sentence[::-1]
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")
            continue

        print(f"\nResult: {result}")
        vowels, consonants = count_vowels_consonants(result)
        print(f"Vowels: {vowels}, Consonants: {consonants}")

if __name__ == "__main__":
    cli_main()
