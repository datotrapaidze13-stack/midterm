import sys

# ტერმინალში ქართული ტექსტის სწორად საჩვენებლად/მისაღებად
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")


class Person:
    # ბაზისური კლასი - ინახავს სახელს ყველა "ადამიანისთვის" (მემკვიდრეობის საწყისი წერტილი)
    def __init__(self, name):
        self.name = name   # იყენებს ქვემოთა setter-ს, ვალიდაციისთვის

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # ინკაფსულაცია: სახელის ცვლილება ყოველთვის გადის ამ ვალიდაციაზე
        if not value or not value.strip():
            raise ValueError("სახელი არ შეიძლება იყოს ცარიელი.")
        self._name = value.strip()

    def __str__(self):
        return f"სახელი: {self.name}"


class Student(Person):
    # Student "მემკვიდრეობით იღებს" Person-ისგან სახელის ლოგიკას (inheritance)
    VALID_GRADES = ("A", "B", "C", "D", "F")

    def __init__(self, name, roll_number, grade):
        super().__init__(name)     # Person-ის კონსტრუქტორის გამოძახება სახელის დასაყენებლად
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
        return f"სიის ნომერი: {self.roll_number} | სახელი: {self.name} | შეფასება: {self.grade}"


def input_name():
    # ვთხოვთ სახელს, სანამ ცარიელს არ დაწერენ
    while True:
        name = input("შეიყვანეთ სტუდენტის სახელი: ").strip()
        if name:
            return name
        print("სახელი არ შეიძლება იყოს ცარიელი.")


def input_roll_number(students, exclude=None):
    # ვთხოვთ სიის ნომერს, სანამ ვალიდურ და თავისუფალ ნომერს არ მივიღებთ
    while True:
        raw = input("შეიყვანეთ სიის ნომერი: ").strip()

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
        grade = input(f"შეიყვანეთ შეფასება ({options}): ").strip().upper()
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
    name = input_name()
    roll_number = input_roll_number(students)
    grade = input_grade()
    students.append(Student(name, roll_number, grade))
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
    raw = input("შეიყვანეთ საძებნი სიის ნომერი: ").strip()

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
    raw = input("შეიყვანეთ იმ სტუდენტის სიის ნომერი, ვისი შეფასების განახლებაც გსურთ: ").strip()

    if not raw.isdigit():
        print("არასწორი ნომერი.")
        return

    student = find_student(students, int(raw))
    if not student:
        print("ასეთი სიის ნომრით სტუდენტი ვერ მოიძებნა.")
        return

    new_grade = input_grade()
    student.grade = new_grade   # ვიყენებთ setter-ს, ავტომატური ვალიდაციით
    print("შეფასება წარმატებით განახლდა.")


def print_menu():
    print("\n=== სტუდენტების მართვის სისტემა ===")
    print("1. ახალი სტუდენტის დამატება")
    print("2. ყველა სტუდენტის ნახვა")
    print("3. სტუდენტის ძებნა სიის ნომრით")
    print("4. სტუდენტის შეფასების განახლება")
    print("5. გასვლა")


def main():
    students = []   # ყველა დამატებული Student ობიექტი ინახება აქ

    while True:
        print_menu()
        choice = input("აირჩიეთ მოქმედება (1-5): ").strip()

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


if __name__ == "__main__":
    main()
