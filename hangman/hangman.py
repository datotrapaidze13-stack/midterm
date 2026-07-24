import random
import sys

# ტერმინალში ქართული ტექსტის სწორად საჩვენებლად/მისაღებად
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

# სიტყვები ინახება dict-ის სახით (word -> hint), რომ თითოეულ სიტყვას თან ახლდეს მინიშნება
WORDS = {
    "python": "პროგრამირების ენა, სახელად გველისა",
    "computer": "მოწყობილობა, რომელზეც ამ თამაშსაც თამაშობ",
    "keyboard": "ხელსაწყო ღილაკებით, ტექსტის ასაწერად",
    "developer": "ადამიანი, რომელიც წერს პროგრამულ კოდს",
    "internet": "გლობალური ქსელი ვებგვერდების სანახავად",
}

# მაქსიმალური არასწორი მცდელობების რაოდენობა
MAX_ATTEMPTS = 6


def choose_word():
    # list(WORDS.keys()) გვაძლევს ყველა სიტყვას (key-ებს) სიის სახით
    # random.choice ირჩევს ერთ შემთხვევით სიტყვას ამ სიიდან
    word = random.choice(list(WORDS.keys()))
    hint = WORDS[word]   # ამ სიტყვის შესაბამისი მინიშნება, dict-იდან [key]-ით
    return word, hint    # ვაბრუნებთ ორივეს ერთად, tuple-ის სახით


def display_progress(word, guessed_letters):
    # სიტყვის ყოველ ასოზე: თუ უკვე გამოცნობილია -> ვაჩვენოთ თვითონ ასო
    # თუ არა -> ვაჩვენოთ ტირე "_"
    # " ".join(...) აერთებს ყველა სიმბოლოს space-ით გამოყოფილ ერთ სტრიქონად
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)


def get_guess(guessed_letters):
    # ვთხოვთ მომხმარებელს ასოს, სანამ ვალიდურ და ახალ ასოს არ მივიღებთ
    while True:
        guess = input("გამოიცანით ასო: ").strip().lower()

        # ვალიდაცია: ზუსტად ერთი ასო უნდა იყოს
        if len(guess) != 1 or not guess.isalpha():
            print("გთხოვთ, შეიყვანოთ ერთი ასო.")
            continue

        # ეს ასო უკვე ნათქვამი აქვს მომხმარებელს
        if guess in guessed_letters:
            print("ეს ასო უკვე გამოცნობილი გაქვთ. სცადეთ სხვა ასო.")
            continue

        return guess


def play_hangman():
    word, hint = choose_word()         # მალული სიტყვა და მისი მინიშნება (tuple-ის დაშლა)
    guessed_letters = set()            # უკვე ნათქვამი ასოების ერთობლიობა (სეტი)
    attempts_left = MAX_ATTEMPTS       # დარჩენილი მცდელობები

    print("\n=== Hangman ===")
    print(f"სიტყვას აქვს {len(word)} ასო.")
    print(f"მინიშნება: {hint}")

    # მთავარი თამაშის ციკლი: სანამ მცდელობები დარჩენილია
    while attempts_left > 0:
        print("\n" + display_progress(word, guessed_letters))
        print(f"დარჩენილი მცდელობები: {attempts_left}")

        guess = get_guess(guessed_letters)
        guessed_letters.add(guess)     # ვინიშნავთ, რომ ეს ასო უკვე ითქვა

        if guess in word:
            # "in" აქ ამოწმებს, შედის თუ არა ეს სიმბოლო სტრიქონში
            print(f"სწორია! ასო '{guess}' არის სიტყვაში.")
        else:
            attempts_left -= 1
            print(f"არასწორია. ასო '{guess}' არ არის სიტყვაში.")

        # გამარჯვების შემოწმება: სიტყვის ყველა ასო უკვე გამოცნობილია?
        if all(letter in guessed_letters for letter in word):
            print(f"\nგილოცავთ! თქვენ გამოიცანით სიტყვა: {word}")
            return  # თამაშის დასრულება - გამარჯვება

    # ციკლიდან გამოსვლა მოხდა მცდელობების ამოწურვის გამო (წაგება)
    print(f"\nთქვენი მცდელობები ამოიწურა. სწორი სიტყვა იყო: {word}")


def main():
    # გარე ციკლი - საშუალებას გვაძლევს რამდენჯერმე ვითამაშოთ ზედიზედ
    while True:
        play_hangman()
        again = input("\nგსურთ თამაშის თავიდან დაწყება? (დიახ/არა): ").strip().lower()
        if again not in ("დიახ", "yes", "y", "დ"):
            print("მადლობა თამაშისთვის!")
            break


# პროგრამა რეალურად აქედან იწყება, თუ ფაილი პირდაპირ გავუშვით
if __name__ == "__main__":
    main()
