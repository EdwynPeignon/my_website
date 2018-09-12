from .classroom import Class
from .student import Student
from operator import attrgetter
from elasticsearch import Elasticsearch
from functools import wraps
from .generation import Generation

import json,time,random


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        #print("Total time running %s: %s seconds" %
        #      (function.__name__, str(t1 - t0))
        #      )
        return result

    return function_timer


@fn_timer
class Genetique:
    def __init__(self,test,nbr_group=8):
        self.classes = []
        self.all_classes = []
        #print(nbr_group)
        self.nbr_group = nbr_group
        self.students = []
        self.averages = []
        self.test = test
        self.fitness = []
        self.first_student = None

    # Affect to all class the students models
    @fn_timer
    def classes_affectation(self,number_classes):
        classes_list = []
        for i in range(number_classes):
            class_ = Class(i)
            student_list = []
            id = 0
            for student in self.students:
                new_student = Student(student.id,student.average,student.name)
                student_list.append(new_student)
                id += 1
            class_.students = student_list
            self.classes.append(class_)

    # Index data to ES
    @fn_timer
    def indexing_data_elasticsearch(self,class_):
        es = Elasticsearch()
        dic = class_.to_dict()
        es.index(index="result_algo3_exemple_"+str(self.test), doc_type="classe", body=dic,id=dic["class_id"])

    # Indexe generation to ES
    @fn_timer
    def indexing_generation_elasticsearch(self,liste):
        generation_id = []
        for class_ in liste:
            generation_id.append(class_.id)

    # Rank all the classes by their evaluation
    @fn_timer
    def rank(self,liste):
        rank = []
        for classroom in liste:
            classroom.eval()
            rank.append(classroom)
        rank.sort(key=attrgetter('evaluation'))
        self.first_student = rank[0]
        return rank

    # Reproduction by crossbreeding
    @fn_timer
    def crossbreeding_function(self, liste,max_id):
        quarter = int(len(liste) / 2)
        half = int(len(liste) / 2)
        new_liste = []
        max_index = max_id + 1

        for i in range(quarter):
            new_students = []
            first_index = random.random() * half
            second_index = random.random() * half + half

            rupture_point = int(random.random() * (len(liste[0].students) - 1))

            new_specimen = Class(i + max_index)

            liste[int(first_index)].students.sort(key=attrgetter('id'))
            liste[int(second_index)].students.sort(key=attrgetter('id'))
            for student in liste[int(first_index)].students[:rupture_point] + liste[int(
                    second_index)].students[rupture_point:]:

                new_student = Student(student.id, student.average,student.name, student.group)
                new_student.girl = student.girl

                new_students.append(new_student)

            new_specimen.students = new_students

            new_specimen.generation = max(liste[int(first_index)].generation,liste[int(second_index)].generation) + 1

            new_specimen.adapting_group_after_mutating(liste[int(first_index)])

            new_liste.append(new_specimen)
        self.all_classes += new_liste

        return new_liste

    # Selection by tournament 2 specimen taken randomly has to confront
    @fn_timer
    def tournament(self):

        list_bool = [False] * len(self.classes)
        selection = []

        for i in range(int(len(self.classes)/2)):
            first_random = int(random.random() * len(self.classes))

            second_random = int(random.random() * len(self.classes))

            while(list_bool[first_random] == True):
                first_random = int(random.random() * len(self.classes))

            list_bool[first_random] = True

            while(list_bool[second_random] == True):
                second_random = int(random.random() * len(self.classes))

            list_bool[second_random] = True

            self.classes[first_random].eval()
            self.classes[second_random].eval()

            if(self.classes[first_random].evaluation > self.classes[second_random].evaluation):
                selection.append(self.classes[second_random])
            else:
                selection.append(self.classes[first_random])
        return selection

    # Reproduction by mutation
    @fn_timer
    def mutation_allele(self,liste,max_id):
        count = max_id +1
        new_liste = []
        for class_ in liste:
            new_class = Class(count)

            for student in class_.students:
                new_class.add_student(student)

            for group in class_.groups:
                new_class.add_group(group)

            first_random_index = int(random.random() * len(new_class.students))
            second_random_index = first_random_index
            while first_random_index == second_random_index:
                second_random_index = int(random.random() * len(new_class.students))


            while first_random_index==second_random_index or new_class.students[first_random_index].group==new_class.students[second_random_index].group:
                second_random_index = int(random.random() * len(new_class.students))

            variable = new_class.students[first_random_index].group

            new_class.students[first_random_index].group = new_class.students[second_random_index].group
            new_class.students[second_random_index].group = variable

            new_class.generation = class_.generation + 1

            new_class.adapting_group_after_mutating(class_)
            new_class.eval()

            new_liste.append(new_class)

            count += 1

        self.all_classes += new_liste

        return new_liste

    # Reproduce the population
    @fn_timer
    def reproduction(self):

        selection = self.tournament()
        max_id = max(list(map(attrgetter('id'), self.classes)))
        mutation_allele =  self.mutation_allele(selection[:int(len(selection)/2)],max_id)
        max_id = max(list(map(attrgetter('id'),mutation_allele)))
        crossed_list = self.crossbreeding_function(selection,max_id)
        self.classes = []
        self.classes = selection + mutation_allele + crossed_list

        for class_ in self.classes:
            class_.eval()

        self.rank(self.classes)

    # Sort the classes and set them eligible or not (for the case where sex is a criteria)
    def sort_all_classes(self,example_id):
        self.all_classes.sort(key=attrgetter("generation"))

        last_generation = 0
        classes_by_generation = []

        for class_ in self.all_classes:
            if (class_.generation != last_generation):
                generation = Generation(example_id)
                generation.import_values(list(map(attrgetter("result"),classes_by_generation)),last_generation,list(map(attrgetter("evaluation"),classes_by_generation)))
                classes_by_generation = []
                classes_by_generation.append(class_)
                last_generation = class_.generation
            else:
                if class_.eligible:
                    classes_by_generation.append(class_)