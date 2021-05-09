# SAMPLE Input #

# family_names = ['Justin', 'Jake', 'Nguele','Anson', 'Jackson', 'Smith', 'Williams', 'Brown', 'Jones']
# attendees = [3,1,5,3,4,2,2,1,4]
# adult_attendees = [2,1,2,3,2,2,1,1,50]
# child_attendees = [1,0,2,0,2,0,1,0,1]
# priority = [4,2,3,1,5,2,3,5,0]


class Party:
    # Task 0.1
    def __init__(self):
        self.info_attendees = {}
        self.detailed_info_attendees = {}
        
    # Task 0.2
    def add_attendees(self, family_name, number_of_attendees):
        self.info_attendees[family_name] = number_of_attendees

    # Task 1.1
    def detailed_attendees(self, family_names, adult_attendees, child_attendees):
        for n,a,c in zip(family_names, adult_attendees, child_attendees):
            self.detailed_info_attendees[n] = [a,c]
    # Task 1.2
    def check_and_resolve(self):
        for n in self.detailed_info_attendees:
            self.add_attendees(n, self.detailed_info_attendees[n][0] + self.detailed_info_attendees[n][1])
                
    # Task 2.1
    def get_total_attendees(self):
        total_attendees = 0
        for i in self.info_attendees.values():
            total_attendees += i
        return total_attendees
    
    # Task 2.2
    def filter_attendees(self):
        self.problem_families = set()
        for n in self.info_attendees:
            if self.info_attendees[n] > 2 or self.detailed_info_attendees[n][1] != 0:
                self.problem_families.add(n)
        return self.problem_families

    # Task 3
    def covid_changes(self):
        self.filter_attendees
        if self.get_total_attendees() > 50:
            self.filter_attendees()
            print('Please tell the following families to only bring 2 adults and no children: ',self.problem_families)
            for n in self.problem_families:
                self.detailed_info_attendees[n][0] = 2
                self.detailed_info_attendees[n][1] = 0
                self.info_attendees[n] = self.detailed_info_attendees[n][0] + self.detailed_info_attendees[n][1]
          
    # Task 4.1
    def include_priority(self, family_names, priority):
        for n,p in zip(family_names, priority):
            self.detailed_info_attendees[n].append(p)

    # Task 4.2
    def filter_priorities(self, p):
        low_priority = []
        for n in self.detailed_info_attendees:
            if self.detailed_info_attendees[n][2] < p:
                low_priority.append(n)
        return low_priority


####### For Checking 
p = Party()
# p.detailed_attendees(family_names,adult_attendees,child_attendees)
# print(p.detailed_info_attendees)
# p.check_and_resolve()
# print(p.info_attendees)
# print(p.get_total_attendees())
# print(p.filter_attendees())
# p.covid_changes()
# print(p.info_attendees)
# print(p.detailed_info_attendees)
# p.include_priority(family_names, priority)
# print(p.filter_priorities(4))


# ?????????? 
def exercise_2(inputs): # DO NOT CHANGE THIS LINE

    output = Party
   
    return output       # DO NOT CHANGE THIS LINE
