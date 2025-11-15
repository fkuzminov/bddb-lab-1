import os
import random

import faker
import psycopg2


Faker = faker.Faker("en_GB")


FACULTIES_AND_COURSES = {
        "Mathematics": ["Applied Math", "Pure Math"],
        "Physics": ["Theoretical Physics", "Experimental Physics"],
        "Chemistry": ["Organic Chemistry", "Inorganic Chemistry"],
        "Biology": ["Microbiology", "Genetics"],
        "Computer Science": ["Software Engineering", "Data Science"],
        "History": ["Ancient History", "Modern History"],
        "Literature": ["Classical Literature", "Contemporary Literature"],
        "Philosophy": ["Ethics", "Metaphysics"],
        "Economics": ["Microeconomics", "Macroeconomics"],
        "Psychology": ["Clinical Psychology", "Cognitive Psychology"],
}
YEARS = [2018, 2019, 2020, 2021, 2022, 2023]


def get_dns() -> str:
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "127.0.0.1")
    port = os.getenv("POSTGRES_PORT", 5432)
    dbname = os.getenv("POSTGRES_DB", "students")
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


def create_faculties_and_groups_and_courses(c: psycopg2.extensions.cursor) -> tuple[dict[str, int], dict[str, int]]:
    created_courses = {}
    created_groups = {}
    for name, courses in FACULTIES_AND_COURSES.items():
        c.execute(
            """
            INSERT INTO faculties (faculty_name)
            VALUES (%s)
            ON CONFLICT (faculty_name) DO NOTHING
            RETURNING id
            """,
            (name, )
        )
        result = c.fetchone()
        if result:
            id_ = result[0]
        else:
            c.execute("SELECT id FROM faculties WHERE faculty_name = %s", (name, ))
            id_ = c.fetchone()[0]

        for year in YEARS:
            group_name: str = f"Group {year} of {name}"
            c.execute(
                """
                INSERT INTO groups (group_name, faculty_id)
                VALUES (%s, %s)
                ON CONFLICT (group_name) DO NOTHING
                RETURNING id
                """,
                (group_name, id_)
            )
            result = c.fetchone()
            if result:
                created_groups[group_name] = result[0]
            else:
                c.execute("SELECT id FROM groups WHERE group_name = %s", (group_name, ))
                created_groups[group_name] = c.fetchone()[0]

        for course_name in courses:
            c.execute(
                """
                INSERT INTO courses (course_name, credits)
                VALUES (%s, %s)
                ON CONFLICT (course_name) DO NOTHING
                RETURNING id
                """,
                (course_name, random.choice([1,2,3,4,5]))
            )
            result = c.fetchone()
            if result:
                course_id = result[0]
            else:
                c.execute("SELECT id FROM courses WHERE course_name = %s", (course_name, ))
                course_id = c.fetchone()[0]
            created_courses[course_name] = course_id
        # For query 9
        c.execute(
            """
            INSERT INTO courses (course_name, credits)
            VALUES (%s, %s)
            ON CONFLICT (course_name) DO NOTHING
            """,
            ("Empty Course", 5)
        )
    return created_courses, created_groups


def create_students(c: psycopg2.extensions.cursor, grps: dict[str, int]) -> list[str]:
    c.execute("DELETE FROM students")
    nums = list(range(10, 25))
    students_ids = []
    for group_name, group_id in grps.items():
        for _ in range(random.choice(nums)):
            name = Faker.name()
            enrollment_year = group_name.split(" ")[1]
            c.execute(
                """
                INSERT INTO students (full_name, group_id, enrollment_year)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (name, group_id, enrollment_year)
            )
            result = c.fetchone()
            students_ids.append(result[0])
    return students_ids


def create_enrollments(c: psycopg2.extensions.cursor, students: list[str], courses: dict[str, int]) -> None:
    c.execute("DELETE FROM enrollments")
    # [1:] for query 6
    for student_id in students[1:]:
        selected_courses = random.sample(list(courses.values()), k=random.randint(4, 7))
        for course_id in selected_courses:
            c.execute(
                """
                INSERT INTO enrollments (student_id, course_id, grade)
                VALUES (%s, %s, %s)
                """,
                (student_id, course_id, random.choice([3, 4, 5]))
            )


def create_lecturers_and_teachings(c: psycopg2.extensions.cursor, courses: dict[str, int]) -> None:
    c.execute("DELETE FROM lecturers")
    lecturer_ids = []
    for _ in range(50):
        name = Faker.name()
        c.execute(
            """
            INSERT INTO lecturers (full_name, department)
            VALUES (%s, %s)
            RETURNING id
            """,
            (name, random.choice(list(FACULTIES_AND_COURSES.keys())))
        )
        result = c.fetchone()
        lecturer_ids.append(result[0])

    for lecture_id in lecturer_ids:
        selected_courses = random.sample(list(courses.values()), k=random.randint(3, 5))
        for course_id in selected_courses:
            c.execute(
                """
                INSERT INTO teaching (lecturer_id, course_id, semester)
                VALUES (%s, %s, %s)
                """,
                (lecture_id, course_id, random.choice(list(range(1, 9))))
            )


def main() -> None:
    conn = psycopg2.connect(dsn=get_dns())
    cursor = conn.cursor()
    courses, groups = create_faculties_and_groups_and_courses(cursor)
    conn.commit()
    students = create_students(cursor, groups)
    conn.commit()
    create_enrollments(cursor, students, courses)
    conn.commit()
    create_lecturers_and_teachings(cursor, courses)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
