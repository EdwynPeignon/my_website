from operator import attrgetter

class Group:
    def __init__(self,id,students):
        self.id = id
        self.students = students
        self.gap = -1
        self.average = 0

    def group_average(self):
        total = 0
        for student in self.students:
            total += student.average
        self.average = total/len(self.students)
        return self.average

    def worst_student(self):
        list_notes = []
        for student in self.students:
            list_notes.append(student.average)
        return list_notes.index(min(list_notes))

    def best_student(self):
        list_notes = []
        for student in self.students:
            list_notes.append(student.average)
        return list_notes.index(max(list_notes))


    def girl_in_group(self):
        new_list = list(map(attrgetter("girl"),self.students))
        return new_list.count(True)


    def __str__(self):
        string = "Group id : " + str(self.id)  + " group gap : " + str(self.gap) + "\n"
        for student in self.students:
            string += student.__str__() + "\n"
        return string