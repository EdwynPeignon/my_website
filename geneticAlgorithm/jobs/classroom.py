from .group import Group
from .student import Student
import random
from operator import attrgetter


class Class:
    def __init__(self,i):
        self.groups = []
        self.students = []
        self.id = i
        self.evaluation = 0
        self.result = 0
        self.generation = 0
        self.eligible = False
        self.average = 0

    # Attribute an evaluation to the class
    def eval(self):
        gaps = []
        for group in self.groups:
            self.gap_groups_processing()
            gaps.append(group.gap)
        self.evaluation = max(gaps) - min(gaps)
        return max(gaps) - min(gaps)

    # Initialize all the groups average
    def gap_groups_processing(self):
        for group in self.groups:
            group.gap = group.group_average() - self.class_average()

    # Calculate the average of the class
    def class_average(self):
        total = 0
        for student in self.students:
            total += student.average
        self.average = total/len(self.students)
        return self.average

    # Affect to the student groups
    def groups_affecting(self,nbr_group):
        student_in_group = int(len(self.students) / nbr_group)
        id_group = 0
        left_over_bool = False
        random.shuffle(self.students)
        for i in range(len(self.students)):
            if i%student_in_group == 0 and left_over_bool is False and i != 0:
                id_group += 1
            elif left_over_bool:
                id_group += 1

            if id_group == nbr_group and left_over_bool is False:
                left_over_bool = True
                id_group = 0

            self.students[i].group = id_group

        self.creating_groups()

    # Initialize groups
    def creating_groups(self):
        count = 0
        list_student = []
        last_group = 0

        self.groups = []
        self.students = self.sort_list(self.students, "group")

        while count < len(self.students):

            if last_group == self.students[count].group:
                list_student.append(self.students[count])
            else:
                self.groups.append(Group(list_student[0].group, list_student))
                list_student = []
                last_group = self.students[count].group
                list_student.append(self.students[count])

            count += 1

        self.groups.append(Group(list_student[0].group, list_student))

    # Adapt student group number thanks to a model
    def adapting_group_after_mutating(self,class_):
        self.students = self.sort_list(self.students, "group")
        class_.students = class_.sort_list(class_.students, "group")

        for i in range(len(self.students)):
            self.students[i].group = class_.students[i].group

        self.creating_groups()

    # Sort list in function of an attribute
    @staticmethod
    def sort_list(list,key):
        new_list = []
        for student in list:
            new_list.append(student)
        new_list.sort(key=attrgetter(key))
        return new_list

    # Add a student to list of students
    def add_student(self,student):
        new_student = Student(student.id,student.average,student.name)
        new_student.group = student.group

        self.students.append(new_student)

    # Add a group to the class
    def add_group(self,group):
        new_group = Group(group.id,group.students)
        self.groups.append(new_group)

    # Fitness function with sex criteria
    def fitness_function(self):

        gaps = []
        girl_in_group = []
        girl_in_class = 0
        bonus = 0
        for group in self.groups:
            self.gap_groups_processing()
            gaps.append(group.gap)
            girl_in_group.append(group.girl_in_group())
            girl_in_class += group.girl_in_group()

        self.result = max(gaps) - min(gaps)

        reste = girl_in_class % len(self.groups)

        liste = [int(girl_in_class/len(self.groups))] * len(self.groups)

        for i in range(reste):
            liste[i] += 1

        for i in range(len(liste)):
            if(liste[i] in girl_in_group):
                girl_in_group.remove(liste[i])
                bonus += 1

        if bonus/len(self.groups) > 0.9:
           self.evaluation = self.result - self.result * 0.5
        elif bonus/len(self.groups) < 5:
            self.evaluation = self.result + self.result * 0.5

        if bonus/len(self.groups) == 1:
            self.eligible = True

        return max(gaps) - min(gaps)

    # Used to send data to ElasticSearch
    def to_dict(self):
        return dict(
            class_id = self.id,
            class_generation = self.generation,
            class_result = self.result,
            class_evaluation = self.evaluation
        )