import random

from .jobs.genetic import Genetique
from .jobs.student import Student

def main(names,marks,number_groups,numberGeneration):
    print("LAUNCH")

    gen = Genetique(0,number_groups)
    averages = []
    student_example = []

    for i in range(len(marks)):
        student = Student(i,marks[i],names[i])

        student_example.append(student)

        #averages.append(random.random() * 21)

    gen.students = student_example

    gen.classes_affectation(256)


    for class_ in gen.classes:
        class_.groups_affecting(gen.nbr_group)

    gen.rank(gen.classes)

    #generation = Generation(example_id)

    gen.all_classes = gen.classes

    #liste = list(map(attrgetter("evaluation"),gen.classes))

    #generation.import_values(liste,0)

    max_reproduction = 0
    while(max_reproduction < numberGeneration):
        gen.reproduction()
        for class_ in gen.classes:
            if class_.generation > max_reproduction:
                max_reproduction = class_.generation

    for group in gen.first_student.groups:
        print(group)

    return gen.first_student
    #print("First class : " + str(gen.first_student.evaluation))
