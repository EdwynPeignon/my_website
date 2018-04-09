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
    def eval(self):
        gaps = []
        for group in self.groups:
            self.gap_groups_processing()
            gaps.append(group.gap)
        self.evaluation = max(gaps) - min(gaps)
        return max(gaps) - min(gaps)

    def get_groups(self):
        return self.groups

    def get_students(self):
        return self.students

    def set_groups(self,groups):
        self.groups = groups

    def set_students(self,students):
        self.students = students

    def gap_groups_processing(self):
        for group in self.groups:
            group.gap = group.group_average() - self.class_average()

    def class_average(self):
        total = 0
        for student in self.students:
            total += student.average
        self.average = total/len(self.students)
        return self.average

    #Genetique 2

    # Checked
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


    def adapting_group_after_mutating(self,class_):
        self.students = self.sort_list(self.students, "group")
        class_.students = class_.sort_list(class_.students, "group")
        """
        print(class_.groups)
        for group in class_.groups:
            print(group)
        print("Self")
        for group in self.groups:
            print(group)
        """
        for i in range(len(self.students)):
            self.students[i].group = class_.students[i].group

        self.creating_groups()

    def sort_list(self,liste,key):
        new_list = []
        for student in liste:
            new_list.append(student)
        new_list.sort(key=attrgetter(key))
        return new_list

    def add_student(self,student):
        new_student = Student(student.id,student.average,student.name)
        new_student.group = student.group

        self.students.append(new_student)

    def add_group(self,group):
        new_group = Group(group.id,group.students)
        #new_group.gap = group.gap
        self.groups.append(new_group)

    def fitness_function(self):

        #print("~~~ FITNESS FUNCTION ~~~")
        gaps = []
        girl_in_group = []
        girl_in_class = 0
        bonus = 0
        """
        print("Begin generation : " + str(self.id))
        for group in self.groups:
            print(group)
        """
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

    def to_dict(self):
        return dict(
            class_id = self.id,
            class_generation = self.generation,
            class_result = self.result,
            class_evaluation = self.evaluation
        )