import re

cmd_exit = "exit"
cmd_add_students = "add students"
cmd_back = "back"
cmd_add_points = "add points"
cmd_list = "list"
cmd_find = "find"
cmd_stats = "statistics"
cmd_notify = "notify"

students = []


class Course:
    def __init__(self, name, points_to_finish):
        self.name = name
        self.points_to_finish = points_to_finish
        self.attendees = []

    def add_attendee(self, attendee):
        self.attendees.append(attendee)

    def enrolled_students(self):
        return len(list(filter(lambda a: a.is_enrolled(), self.attendees)))

    def student_activity(self):
        return sum(map(lambda a: a.submissions, self.attendees))

    def student_points(self):
        return sum(map(lambda a: a.points, self.attendees))

    def average_score(self):
        return 0 if self.student_activity() == 0 else self.student_points() / self.student_activity()

    def __str__(self):
        return self.name


python = Course("Python", 600)
algorithms = Course("DSA", 400)
databases = Course("Databases", 480)
flask = Course("Flask", 550)


class Statistics:
    def __init__(self, courses):
        self.courses = courses

    def most_popular_course(self):
        popularity_max = max(map(lambda c: c.enrolled_students(), self.courses))
        filtered = list(filter(lambda c: c.enrolled_students() == popularity_max, self.courses))
        return [] if popularity_max == 0 else filtered

    def least_popular_course(self, most_popular):
        popularity_min = min(map(lambda c: c.enrolled_students(), self.courses))
        filtered = list(filter(lambda c: c.enrolled_students() == popularity_min, self.courses))
        return [] if len(most_popular) == 0 else list(filter(lambda c: c not in most_popular, filtered))

    def highest_activity_course(self):
        activity_max = max(map(lambda c: c.student_activity(), self.courses))
        filtered = list(filter(lambda c: c.student_activity() == activity_max, self.courses))
        return [] if activity_max == 0 else filtered

    def lowest_activity_course(self, highest_activity):
        activity_min = min(map(lambda c: c.student_activity(), self.courses))
        filtered = list(filter(lambda c: c.student_activity() == activity_min, self.courses))
        return [] if len(highest_activity) == 0 else list(filter(lambda c: c not in highest_activity, filtered))

    def easiest_course(self):
        score_max = max(map(lambda c: c.average_score(), self.courses))
        filtered = list(filter(lambda c: c.average_score() == score_max, self.courses))
        return [] if score_max == 0 else filtered

    def hardest_course(self, easiest):
        score_min = min(map(lambda c: c.average_score(), self.courses))
        filtered = list(filter(lambda c: c.average_score() == score_min, self.courses))
        return [] if len(easiest) == 0 else list(filter(lambda c: c not in easiest, filtered))

    def print_overview(self):
        most_popular = self.most_popular_course()
        print(f"Most popular: {self.format_cources(most_popular)}")
        least_popular = self.least_popular_course(most_popular)
        print(f"Least popular: {self.format_cources(least_popular)}")

        highest_activity = self.highest_activity_course()
        print(f"Highest activity: {self.format_cources(highest_activity)}")
        lowest_activity = self.lowest_activity_course(highest_activity)
        print(f"Lowest activity: {self.format_cources(lowest_activity)}")

        easiest = self.easiest_course()
        print(f"Easiest course: {self.format_cources(easiest)}")
        hardest = self.hardest_course(easiest)
        print(f"Hardest course: {self.format_cources(hardest)}")

    def format_cources(self, courses):
        if len(courses) < 1:
            return "n/a"
        else:
            return ', '.join(list(map(lambda c: c.name, courses)))


statistics = Statistics([python, algorithms, databases, flask])


class Attendance:
    def __init__(self, course, student):
        self.course = course
        self.student = student
        self.points = 0
        self.submissions = 0
        self.notified = False
        course.add_attendee(self)

    def earn_points(self, points):
        self.points += points
        self.submissions += 1

    def is_enrolled(self):
        return self.submissions > 0

    def completed(self):
        return round(self.points / self.course.points_to_finish * 100, 1)

    def is_completed(self):
        return self.points >= self.course.points_to_finish

    def is_notified(self):
        return self.notified

    def notify(self):
        if self.is_completed() and not self.is_notified():
            print(f"To: {self.student.mail}")
            print("Re: Your Learning Progress")
            print(f"Hello, {self.student.full_name()}! You have accomplished our {self.course.name} course!")
        self.notified = True


class Student:
    def __init__(self, first_name, last_name, mail):
        self.id = str(hash(mail))
        self.first_name = first_name
        self.last_name = last_name
        self.mail = mail
        self.python = Attendance(python, self)
        self.algorithms = Attendance(algorithms, self)
        self.databases = Attendance(databases, self)
        self.flask = Attendance(flask, self)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def attendance(self):
        return [self.python, self.algorithms, self.databases, self.flask]

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.mail

    def __hash__(self):
        return hash(id)

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.id == other.id
        return False


def take_input():
    usr_input = input("")
    if usr_input.strip() == "":
        print("No input")
        take_input()
    elif usr_input == cmd_exit:
        print("Bye!")
    elif usr_input == cmd_add_students:
        add_student()
    elif usr_input == cmd_add_points:
        add_points()
    elif usr_input == cmd_back:
        go_back()
    elif usr_input == cmd_list:
        list_students()
    elif usr_input == cmd_find:
        find_student()
    elif usr_input == cmd_stats:
        print_stats()
    elif usr_input == cmd_notify:
        notify_students()
    else:
        print("Error: unknown command!")
        take_input()


def add_student(prt_msg=True):
    if prt_msg:
        print("Enter student credentials or 'back' to return:")

    credentials = input()
    if credentials == cmd_back:
        go_back()
    elif len(credentials.split(" ")) < 3:
        print("Incorrect credentials")
        add_student(False)
    else:
        split_string = credentials.rsplit(' ', 1)
        first_name = split_string[0].split(' ', 1)[0]
        last_name = split_string[0].split(' ', 1)[1]
        mail = split_string[1]
        if not check_name(first_name):
            print("Incorrect first name.")
            add_student(False)
        elif not check_last_name(last_name):
            print("Incorrect last name.")
            add_student(False)
        elif not check_mail(mail):
            print("Incorrect email.")
            add_student(False)
        elif any(s.mail == mail for s in students):
            print("This email is already taken.")
            add_student(False)
        else:
            students.append(Student(first_name, last_name, mail))
            print(f"The student has been added.")
            add_student(False)


def check_name(name):
    return re.fullmatch("[A-Za-z]+['-.]?[A-Za-z]+", name) is not None


def check_last_name(last_name):
    return any(check_name(part) for part in (last_name.split()))


def check_mail(mail):
    return re.fullmatch("[A-Za-z0-9.-]*@[A-Za-z0-9-]*\\.[A-Za-z0-9]*", mail) is not None


def go_back():
    print(f"Total {len(students)} students have been added.")
    print("Enter 'exit' to exit the program")
    take_input()


def add_points(prt_msg=True):
    if prt_msg:
        print("Enter an id and points or 'back' to return:")

    points = input()
    if points == cmd_back:
        take_input()
    elif not check_points(points):
        print("Incorrect points format.")
        add_points(False)
    else:
        parts = points.split()
        student_id = parts[0]
        student = next((s for s in students if s.id == student_id), None)
        if student is None:
            print(f"No student is found for id={student_id}.")
            add_points(False)
        else:
            student.python.earn_points(int(parts[1]))
            student.algorithms.earn_points(int(parts[2]))
            student.databases.earn_points(int(parts[3]))
            student.flask.earn_points(int(parts[4]))
            print("Points updated.")
            add_points(False)


def check_points(points):
    return re.fullmatch("[-A-Za-z0-9]+ [0-9]+ [0-9]+ [0-9]+ [0-9]+", points) is not None


def list_students():
    if len(students) == 0:
        print("No students found.")
    else:
        print("Students:")
        for student in students:
            print(student.id)
    take_input()


def find_student(prt_msg=True):
    if prt_msg:
        print("Enter an id or 'back' to return")

    student_id = input()
    if student_id == cmd_back:
        take_input()
    else:
        student = next((s for s in students if s.id == student_id), None)
        if student is None:
            print(f"No student is found for id={student_id}.")
            find_student(False)
        else:
            py = student.python.points
            dsa = student.algorithms.points
            db = student.databases.points
            flk = student.flask.points
            print(f"{student.id} points: Python={py}; DSA={dsa}; Databases={db}; Flask={flk}")
            find_student(False)


def print_stats(prt_msg=True):
    courses = [python, algorithms, databases, flask]
    if prt_msg:
        print("Type the name of a course to see details or 'back' to quit:")
        statistics.print_overview()

    course_name = input()
    if course_name == cmd_back:
        take_input()
    else:
        course = next(filter(lambda c: c.name.lower() == course_name.lower(), courses), None)
        if course is None:
            print("Unknown course")
        else:
            print(course_name)
            table_format = "{:<20} {:<10} {:5}"
            print(table_format.format("id", "points", "completed"))
            attendees = sorted(course.attendees, key=lambda a: (a.points, int(a.student.id) * -1), reverse=True)
            for s in attendees:
                print(table_format.format(s.student.id, s.points, f"{s.completed()}%"))
        print_stats(False)


def notify_students():
    notified_students = 0
    for student in students:
        notified = False
        for attendee in student.attendance():
            if attendee.is_completed() and not attendee.is_notified():
                attendee.notify()
                notified = True
        if notified:
            notified_students += 1
    print(f"Total {notified_students} students have been notified.")
    take_input()


print("Learning Progress Tracker")
take_input()
