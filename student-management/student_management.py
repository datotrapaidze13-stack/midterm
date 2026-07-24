import json   # JSON ფაილის წასაკითხად/ჩასაწერად, სტუდენტების მუდმივად შესანახად
import os     # ფაილის გზის ასაწყობად
import sys

# ტერმინალში ქართული ტექსტის სწორად საჩვენებლად/მისაღებად
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

# სტუდენტების მუდმივი შესანახი ფაილი (იმავე საქაღალდეში, სადაც ეს .py ფაილია)
# os.path.abspath გამოიყენება იმისთვის, რომ ფაილის მდებარეობა არ იცვლებოდეს
# იმის მიხედვით, თუ საიდან (რომელი working directory-დან) გაეშვება სკრიპტი
STUDENTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.json")

QUIT_COMMAND = "/q"


class QuitProgram(Exception):
    # სპეციალური გამონაკლისი: აღინიშნება, როცა მომხმარებელი ნებისმიერი კითხვისას წერს /q-ს.
    # ის "ბუშტივით" ადის ზემოთ ნებისმიერი ფუნქციიდან, სანამ main() მას არ დაიჭერს.
    pass


def read_input(prompt):
    # ჩვეულებრივი input()-ის ნაცვლად ყველგან ამას ვიყენებთ, რომ /q ნებისმიერ დროს იმუშაოს
    value = input(prompt)
    if value.strip().lower() == QUIT_COMMAND:
        raise QuitProgram()
    return value


class Person:
    # ბაზისური კლასი - ინახავს სახელს/გვარს ყველა "ადამიანისთვის" (მემკვიდრეობის საწყისი წერტილი)
    def __init__(self, first_name, last_name):
        self.first_name = first_name   # იყენებს ქვემოთა setter-ს, ვალიდაციისთვის
        self.last_name = last_name

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        # ინკაფსულაცია: სახელის ცვლილება ყოველთვის გადის ამ ვალიდაციაზე
        if not value or not value.strip():
            raise ValueError("სახელი არ შეიძლება იყოს ცარიელი.")
        value = value.strip()
        if not value.isalpha():
            raise ValueError("სახელი უნდა შეიცავდეს მხოლოდ ასოებს, ციფრების ან სიმბოლოების გარეშე.")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        # ინკაფსულაცია: გვარის ცვლილება ყოველთვის გადის ამ ვალიდაციაზე
        if not value or not value.strip():
            raise ValueError("გვარი არ შეიძლება იყოს ცარიელი.")
        value = value.strip()
        if not value.isalpha():
            raise ValueError("გვარი უნდა შეიცავდეს მხოლოდ ასოებს, ციფრების ან სიმბოლოების გარეშე.")
        self._last_name = value

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"სახელი: {self.full_name}"


class Student(Person):
    # Student "მემკვიდრეობით იღებს" Person-ისგან სახელი/გვარის ლოგიკას (inheritance)
    VALID_GRADES = ("A", "B", "C", "D", "F")

    def __init__(self, first_name, last_name, roll_number, grade):
        super().__init__(first_name, last_name)   # Person-ის კონსტრუქტორის გამოძახება სახელი/გვარის დასაყენებლად
        self.roll_number = roll_number   # setter-ით ვალიდაცია
        self.grade = grade                # setter-ით ვალიდაცია

    @property
    def roll_number(self):
        return self._roll_number

    @roll_number.setter
    def roll_number(self, value):
        # ინკაფსულაცია: სიის ნომერი უნდა იყოს დადებითი მთელი რიცხვი
        if not isinstance(value, int) or value <= 0:
            raise ValueError("სიის ნომერი უნდა იყოს დადებითი მთელი რიცხვი.")
        self._roll_number = value

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        # ინკაფსულაცია: შეფასება უნდა იყოს ერთ-ერთი დაშვებული ასო
        value = value.strip().upper()
        if value not in Student.VALID_GRADES:
            raise ValueError(f"შეფასება უნდა იყოს ერთ-ერთი: {', '.join(Student.VALID_GRADES)}.")
        self._grade = value

    def __str__(self):
        # პოლიმორფიზმი: Student თავისებურად "გადაწერს" (override) Person-ის __str__-ს
        return f"სიის ნომერი: {self.roll_number} | სახელი: {self.full_name} | შეფასება: {self.grade}"


def load_students():
    # კითხულობს students.json ფაილს და თითოეული ჩანაწერიდან ქმნის ნამდვილ Student ობიექტს
    if not os.path.exists(STUDENTS_FILE):
        return []   # ფაილი ჯერ არ არსებობს (პირველი გაშვება) - ვიწყებთ ცარიელი სიით

    with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)   # JSON -> სია, სადაც თითო ელემენტი არის dict

    # თითოეულ dict-ს ("first_name", "last_name", "roll_number", "grade") ვაქცევთ ნამდვილ Student ობიექტად
    return [
        Student(item["first_name"], item["last_name"], item["roll_number"], item["grade"])
        for item in raw_data
    ]


def save_students(students):
    # თითოეულ Student ობიექტს ვაქცევთ უბრალო dict-ად, რომ JSON-მა შეძლოს მისი ჩაწერა
    raw_data = [
        {
            "first_name": s.first_name,
            "last_name": s.last_name,
            "roll_number": s.roll_number,
            "grade": s.grade,
        }
        for s in students
    ]

    with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=4)


def input_first_name():
    # ვთხოვთ სახელს, სანამ არ დაწერენ მხოლოდ ასოებისგან შემდგარ, ერთსიტყვიან, არაცარიელ მნიშვნელობას
    while True:
        first_name = read_input("შეიყვანეთ სტუდენტის სახელი: ").strip()
        if not first_name:
            print("სახელი არ შეიძლება იყოს ცარიელი.")
        elif len(first_name.split()) > 1:
            print("თქვენ ორი სიტყვა შეიყვანეთ — როგორც ჩანს, სახელთან ერთად გვარიც დაწერეთ. გთხოვთ, აქ მხოლოდ სახელი მიუთითეთ.")
        elif not first_name.isalpha():
            print("სახელი უნდა შეიცავდეს მხოლოდ ასოებს, ციფრების ან სიმბოლოების გარეშე.")
        else:
            return first_name


def input_last_name():
    # ვთხოვთ გვარს, სანამ არ დაწერენ მხოლოდ ასოებისგან შემდგარ, ერთსიტყვიან, არაცარიელ მნიშვნელობას
    while True:
        last_name = read_input("შეიყვანეთ სტუდენტის გვარი: ").strip()
        if not last_name:
            print("გვარი არ შეიძლება იყოს ცარიელი.")
        elif len(last_name.split()) > 1:
            print("თქვენ ორი სიტყვა შეიყვანეთ — გთხოვთ, აქ მხოლოდ გვარი მიუთითეთ.")
        elif not last_name.isalpha():
            print("გვარი უნდა შეიცავდეს მხოლოდ ასოებს, ციფრების ან სიმბოლოების გარეშე.")
        else:
            return last_name


def input_roll_number(students, exclude=None):
    # ვთხოვთ სიის ნომერს, სანამ ვალიდურ და თავისუფალ ნომერს არ მივიღებთ
    while True:
        raw = read_input("შეიყვანეთ სიის ნომერი: ").strip()

        if not raw.isdigit():
            print("სიის ნომერი უნდა იყოს დადებითი მთელი რიცხვი.")
            continue

        roll_number = int(raw)

        # ვამოწმებთ, ხომ არ არის ეს ნომერი უკვე დაკავებული სხვა სტუდენტის მიერ
        taken = any(s.roll_number == roll_number for s in students if s is not exclude)
        if taken:
            print("ეს სიის ნომერი უკვე დაკავებულია სხვა სტუდენტის მიერ.")
            continue

        return roll_number


def input_grade():
    # ვთხოვთ შეფასებას, სანამ ერთ-ერთ დაშვებულ ასოს არ მივიღებთ
    options = "/".join(Student.VALID_GRADES)
    while True:
        grade = read_input(f"შეიყვანეთ შეფასება ({options}): ").strip().upper()
        if grade in Student.VALID_GRADES:
            return grade
        print(f"არასწორი შეფასება. დაშვებულია მხოლოდ: {options}")


def find_student(students, roll_number):
    # ვეძებთ სტუდენტს სიის ნომრით, ჩვეულებრივი ციკლით
    for student in students:
        if student.roll_number == roll_number:
            return student
    return None


def add_student(students):
    print("\n--- ახალი სტუდენტის დამატება ---")
    first_name = input_first_name()
    last_name = input_last_name()
    roll_number = input_roll_number(students)
    grade = input_grade()
    students.append(Student(first_name, last_name, roll_number, grade))
    save_students(students)   # განახლებულ სიას მაშინვე ვინახავთ JSON ფაილშიც, სამუდამოდ
    print("სტუდენტი წარმატებით დაემატა.")


def view_all_students(students):
    print("\n--- ყველა სტუდენტი ---")
    if not students:
        print("სტუდენტები ჯერ არ არის დამატებული.")
        return
    for student in students:
        print(student)   # print ავტომატურად იძახებს student-ის __str__-ს


def search_student(students):
    print("\n--- სტუდენტის ძებნა სიის ნომრით ---")
    raw = read_input("შეიყვანეთ საძებნი სიის ნომერი: ").strip()

    if not raw.isdigit():
        print("არასწორი ნომერი.")
        return

    student = find_student(students, int(raw))
    if student:
        print(student)
    else:
        print("ასეთი სიის ნომრით სტუდენტი ვერ მოიძებნა.")


def update_student_grade(students):
    print("\n--- სტუდენტის შეფასების განახლება ---")
    raw = read_input("შეიყვანეთ იმ სტუდენტის სიის ნომერი, ვისი შეფასების განახლებაც გსურთ: ").strip()

    if not raw.isdigit():
        print("არასწორი ნომერი.")
        return

    student = find_student(students, int(raw))
    if not student:
        print("ასეთი სიის ნომრით სტუდენტი ვერ მოიძებნა.")
        return

    new_grade = input_grade()
    student.grade = new_grade   # ვიყენებთ setter-ს, ავტომატური ვალიდაციით
    save_students(students)     # განახლებულ შეფასებას მაშინვე ვინახავთ JSON ფაილშიც
    print("შეფასება წარმატებით განახლდა.")


def print_menu():
    print("\n=== სტუდენტების მართვის სისტემა ===")
    print("1. ახალი სტუდენტის დამატება")
    print("2. ყველა სტუდენტის ნახვა")
    print("3. სტუდენტის ძებნა სიის ნომრით")
    print("4. სტუდენტის შეფასების განახლება")
    print("5. გასვლა")
    print(f"({QUIT_COMMAND} - პროგრამიდან გამოსვლა ნებისმიერ დროს)")


def main():
    students = load_students()   # პროგრამის დაწყებისას ვტვირთავთ უკვე შენახულ სტუდენტებს ფაილიდან

    try:
        while True:
            print_menu()
            choice = read_input("აირჩიეთ მოქმედება (1-5): ").strip()

            if choice == "1":
                add_student(students)
            elif choice == "2":
                view_all_students(students)
            elif choice == "3":
                search_student(students)
            elif choice == "4":
                update_student_grade(students)
            elif choice == "5":
                print("ნახვამდის!")
                break
            else:
                print("არასწორი არჩევანი, სცადეთ თავიდან.")
    except QuitProgram:
        print("\nნახვამდის!")


if __name__ == "__main__":
    main()
