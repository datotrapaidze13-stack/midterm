import json   # JSON ფაილების წასაკითხად და ჩასაწერად
import os     # ფაილის გზების ასაწყობად (საქაღალდე + ფაილის სახელი)
import sys    # ტერმინალის კოდირების (encoding) დასაყენებლად

# ტერმინალში ქართული ტექსტის სწორად საჩვენებლად/მისაღებად (განსაკუთრებით Windows-ზე საჭირო)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

# ლექსიკონების (JSON ფაილების) საქაღალდის სრული გზა.
# __file__ = ამ ფაილის (translator.py) მდებარეობა; dirname აძლევს მხოლოდ საქაღალდეს, ფაილის სახელის გარეშე.
# os.path.join სწორად აერთებს გზას ნებისმიერ ოპერაციულ სისტემაზე (Windows/Mac/Linux)
DICTIONARIES_DIR = os.path.join(os.path.dirname(__file__), "dictionaries")

# მენიუს ნომერი -> (საწყისი ენა საჩვენებლად, სამიზნე ენა საჩვენებლად, შესაბამისი JSON ფაილის სახელი)
# თითოეული value არის tuple (3 მნიშვნელობა ერთად, უცვლელი)
LANGUAGE_PAIRS = {
    "1": ("ქართული", "ინგლისური", "ka_en.json"),
    "2": ("ქართული", "რუსული", "ka_ru.json"),
    "3": ("ინგლისური", "ქართული", "en_ka.json"),
    "4": ("რუსული", "ქართული", "ru_ka.json"),
}


def dictionary_path(filename):
    # აწყობს კონკრეტული ლექსიკონის სრულ გზას (საქაღალდე + ფაილის სახელი)
    return os.path.join(DICTIONARIES_DIR, filename)


def load_dictionary(filename):
    # კითხულობს JSON ფაილს დისკიდან და აბრუნებს პითონის dict-ს (key -> value ფორმატში)
    path = dictionary_path(filename)

    # თუ ფაილი ჯერ არ არსებობს (მაგ. სულ პირველად გაშვებისას), ვაბრუნებთ ცარიელ ლექსიკონს
    if not os.path.exists(path):
        return {}

    # "r" = ფაილის გახსნა წასაკითხად. encoding="utf-8" აუცილებელია ქართული/რუსული ტექსტისთვის.
    # "with ... as f" ავტომატურად ხურავს ფაილს ბლოკის დამთავრებისთანავე, თუნდაც შეცდომა მოხდეს
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)   # json.load: JSON ტექსტი ფაილში -> ნამდვილი პითონის dict


def save_dictionary(filename, translations):
    # იღებს dict-ს (translations) და მთლიანად ხელახლა წერს მას JSON ფაილში
    path = dictionary_path(filename)

    # "w" = ფაილის გახსნა ჩასაწერად (გადაწერს/თავიდან წერს მთელ ფაილს)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            translations,
            f,
            ensure_ascii=False,   # ქართული/რუსული ასოები დარჩეს რეალურ ტექსტად, არა \u10xx კოდებად
            indent=4,             # ლამაზი, ადამიანისთვის წასაკითხი ფორმატირება (4-სივრცული შეწევა)
            sort_keys=True,       # key-ები ალფაბეტურად დალაგებული, ფაილში ადვილად საძებნელად
        )


def choose_language_pair():
    # ვაჩვენებთ მენიუს ყველა შესაძლო ენების წყვილით, LANGUAGE_PAIRS dict-იდან
    print("\nაირჩიეთ ენების წყვილი:")
    for key, (src, dst, _) in LANGUAGE_PAIRS.items():
        # .items() გვაძლევს (key, value) წყვილებს ერთდროულად ციკლში გასავლელად.
        # value თავად არის tuple (src, dst, filename) - ეს ავტომატურად "იშლება" 3 ცვლადში.
        # "_" ნიშნავს "ეს მნიშვნელობა (ფაილის სახელი) აქ არ გვჭირდება, მაგრამ ადგილი უნდა დავიჭიროთ"
        print(f"  {key}. {src} -> {dst}")

    # ვთხოვთ მომხმარებელს არჩევანს, სანამ ვალიდურ (არსებულ) ნომერს არ აირჩევს
    while True:
        choice = input("თქვენი არჩევანი: ").strip()
        if choice in LANGUAGE_PAIRS:        # "in" dict-თან ამოწმებს: არსებობს თუ არა ეს key?
            return LANGUAGE_PAIRS[choice]   # ვაბრუნებთ მთელ tuple-ს: (src, dst, filename)
        print("არასწორი არჩევანი, სცადეთ თავიდან.")


def translate_word(src_lang, dst_lang, filename):
    # ვტვირთავთ არჩეული ენების წყვილის ლექსიკონს JSON ფაილიდან, dict-ის სახით (memory-ში)
    translations = load_dictionary(filename)

    # მთავარი ციკლი: ვთარგმნით სიტყვებს, სანამ მომხმარებელი არ დაწერს "გასვლა"
    while True:
        word = input(f"\nშეიყვანეთ სიტყვა ან ფრაზა {src_lang}ზე (ან 'გასვლა' დასასრულებლად): ").strip()

        # გამოსვლის პირობა - მომხმარებელს სურს ამ ენების წყვილიდან გასვლა
        if word.lower() in ("გასვლა", "exit", "quit"):
            break

        # ცარიელი შეყვანა (მომხმარებელმა უბრალოდ Enter დააჭირა) - ისევ ვკითხოთ
        if not word:
            continue

        # საძებნი key ყოველთვის პატარა ასოებით ვინახავთ, რომ დიდ/პატარა ასოს მნიშვნელობა არ ჰქონდეს
        key = word.lower()

        if key in translations:
            # "in" dict-თან: არსებობს თუ არა ეს სიტყვა, როგორც key, ლექსიკონში?
            # თუ კი - პირდაპირ ვიღებთ თარგმანს [key]-ით
            print(f"თარგმანი ({dst_lang}): {translations[key]}")
        else:
            # სიტყვა ვერ მოიძებნა ლექსიკონში - ვთავაზობთ მომხმარებელს ახლის დამატებას
            print("სამწუხაროდ, ეს სიტყვა ლექსიკონში ვერ მოიძებნა.")
            answer = input("გსურთ დაამატოთ თარგმანი ლექსიკონში? (დიახ/არა): ").strip().lower()

            if answer in ("დიახ", "yes", "y", "დ"):
                new_translation = input(f"შეიყვანეთ თარგმანი {dst_lang}ზე: ").strip()
                if new_translation:
                    translations[key] = new_translation      # ვამატებთ ახალ key-value წყვილს dict-ში (memory)
                    save_dictionary(filename, translations)   # და მაშინვე ვინახავთ JSON ფაილშიც, სამუდამოდ
                    print("დამატებულია ლექსიკონში.")


def main():
    print("=== თარჯიმანი ===")

    # გარე ციკლი - მომხმარებელს შეუძლია რამდენჯერმე შეცვალოს ენების წყვილი, გასვლის გარეშე
    while True:
        # choose_language_pair() აბრუნებს tuple-ს 3 მნიშვნელობით - აქვე ვშლით 3 ცალკე ცვლადში
        src_lang, dst_lang, filename = choose_language_pair()

        translate_word(src_lang, dst_lang, filename)

        again = input("\nგსურთ სხვა ენების წყვილის არჩევა? (დიახ/არა): ").strip().lower()
        if again not in ("დიახ", "yes", "y", "დ"):
            print("ნახვამდის!")
            break


# ეს ხაზი უზრუნველყოფს, რომ main() გაეშვას მხოლოდ მაშინ, თუ ეს ფაილი პირდაპირ გავუშვით
# (და არა მაშინ, თუ ეს ფაილი სხვა ფაილიდან იქნა "შემოტანილი" - import-ით)
if __name__ == "__main__":
    main()
