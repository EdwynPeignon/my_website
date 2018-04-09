import random
class Student:
    def __init__(self, number_id, average,name, group=-1):
        self.id = number_id
        self.average = average
        self.group = group
        self.girl = None
        self.name = name

    def distribution_sex(self):
        alea = random.random()
        if(alea <= 0.1):
            self.girl = True
        else:
            self.girl = False

    def __str__(self):
        return "Etudiant id : " + str(self.id) + " average : " + str(self.average) + " group number : " + str(self.group) + " nom : " + str(self.name)

