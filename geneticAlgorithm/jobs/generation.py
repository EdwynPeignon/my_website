from elasticsearch import Elasticsearch

class Generation:

    def __init__(self,example_id):
        self.result_min = -1
        self.min_evaluation = -1
        self.result_max = -1
        self.average = -1
        self.example_id = example_id
        self.generation = -1

    def import_values(self,resultat,generation,evaluation=[]):

        average = 0

        self.min_evaluation = min(evaluation)

        self.generation = generation

        self.result_min = min(resultat)

        print("Generation : " + str(generation) + " result min : " + str(self.result_min) + " evaluation : " + str(self.min_evaluation))

        self.result_max = max(resultat)

        for x in resultat:
            average += x

        self.average = average/len(resultat)

        self.send_to_elastic()

    def send_to_elastic(self):
        es = Elasticsearch()

        dic = self.__dict__()

        es.index(index="result_generation_algo_distribution_girl",doc_type="generation",body=dic)

    def __str__(self):
        return "Resultat min : " + str(self.result_min) + "\nResultat max : " \
               + str(self.result_max) + "\nAverage : " + str(self.average) + "\nExample ID : " \
               + str(self.example_id) + "\nGeneration : " + str(self.generation)

    def __dict__(self):
        return dict(
            result_min = self.result_min,
            result_max = self.result_max,
            average = self.average,
            generation = self.generation,
            example_id = self.example_id,
            min_evaluation = self.min_evaluation
        )