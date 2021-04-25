## SAMPLE INPUT  (Please use p, q, r variables)

# p = list of teachers names
p = ['Teacher Justin', 'Teacher Mack', 'Teacher Sasayama']

#q = list of student names in string
q = ['Student Kevin', 'Student Champ', 'Student Raisa', 'Student Marcel']

#r = dictionary of lecture id (string) as keys and Teacher Names (String), Student Names (List of strings) as value. 
r = { 'l101':['Teacher Justin', ['Student Kevin', 'Student Champ']],
    'l102': ['Teacher Sasayama',['Student Marcel', 'Student Champ', 'Student Raisa']], 
    'l103':['Teacher Justin',['Student Champ']],
    'l104':['Teacher Sasayama',['Student Champ', 'Student Jason']],
    'l105':['Teacher Mack',['Student Marcel','Student Raisa']]
    }

def exercise_1(p,q,r): # DO NOT CHANGE THIS LINE
    from abc import ABC, abstractmethod
    import itertools

    ### NOTE ####
    # For + operator, please use format lec[** Insert lecture ID**] + stu[** Insert studet ID**]

    class Person(ABC):
        def __init__(self, n):
            self.name = n

        @abstractmethod
        def get_attributes(self):
                pass


    s_id = 100
    class Student(Person):
        s_counter = itertools.count()   #used for assigning ID

        def __init__(self, n):
            self.name = n
            self.lecture_enrolled = set()
            self.student_id = 'S' + str(s_id + next(Student.s_counter))

        def get_attributes(self):
            pass

        def __add__(self, x):
            print('\n\nError: Format is incorrect, please use format lec[** Insert lecture ID**] + stu[** Insert studet ID**]')


    t_id = 100
    class Teacher(Person):
        t_counter = itertools.count()
        def __init__(self, n):
            self.name = n
            self.lecture_taught = None
            self.teacher_id = 'T'+ str(t_id + next(Teacher.t_counter))

        def get_attributes(self):
            pass


    class Lecture():

        def __init__(self, n):
            self.lecture_id = n 
            self.student = set()
            self.teacher_assigned = None

        def assign_teacher(self,x):
            if self.teacher_assigned == None and x.lecture_taught == None:
                self.teacher_assigned = x.name
                x.lecture_taught = self.lecture_id   
            if self.teacher_assigned != None and x.lecture_taught == None:   ## when a teacher is assigned to a lecture that already has a teahcer assigned
                print(x.name, 'cannot be assigned to class', self.lecture_id, 'because a teacher is already assigned to that class')
            if self.teacher_assigned == None and x.lecture_taught != None:   ## when a teacher is assigned to teach more than one lecture, give an error
                print(x.name, 'cannot be assigned to class', self.lecture_id, 'because that teacher is already teaching another class')
        def assign_student(self,y):
            if len(y.lecture_enrolled) < 3:
                y.lecture_enrolled.add(self.lecture_id)
                self.student.add(y.name)
            else:
                print( y.name,  "cannot take more than 3 classes")

        def get_teacher(self):
            print("Lecturer of:", self.lecture_id, ':', self.teacher_assigned)

        def get_student(self):
            if self.student == set():
                print('No students taking this class')
            else:
                print("Students in", self.lecture_id, ':', self.student)

        def __add__(self, s):
                if s.name in q:
                    return self.assign_student(s)
                else:
                    print('\n\nError: Student not found in Database"' )






    ## Create Student objects and save them in dictionary with names as the key
    stu = {}
    for i in q:
        stu[i] = Student(i)


    ## Create Teacher objects and save them in dictionary with names as the key
    tea = {}
    for i in p:
        tea[i] = Teacher(i)


    ## Create Lecture objects and save them in dictionary with Lecture ID as the key
    lec = {}
    for i in r.keys():
        lec[i] = Lecture(i)





    ## Printing the Output

    print("\n\nISSUES (Task 4) (if any):")    
    for n in r.keys():
        for c in r[n][1]:
            if c in q:
                lec[n].assign_student(stu[c])
            else:
                print(c, 'is not in the database')
        if r[n][0] in p:
            lec[n].assign_teacher(tea[r[n][0]])

        else:
            print(r[n][0], 'is not in database')




    ## Printing of output

    print('\nOutputs: (This is the printed version, there is also a dictionary output returned)')
    ## Task 1
    print('\n\nTask 1: List of People')
    for i in stu:
        if isinstance(stu[i], Person):    ## Use isinstance to check if the objects are instances of People or not
            print(stu[i].name)
    for i in tea:
        if isinstance(tea[i], Person):
            print(tea[i].name)

    ## Task 2
    print('\nTask 2:')
    print('\nList of Students:')
    for n in stu:
        print(stu[n].name, 'ID:', stu[n].student_id)

    print('\nList of Teachers:')
    for n in tea:
        print(tea[n].name, 'ID:', tea[n].teacher_id)


    print('\nTask 3:')
    print('List of Lectures with details:\n')
    for n in lec:
        print(lec[n].lecture_id)
        lec[n].get_teacher()
        lec[n].get_student()

    print('\n\nTask 6:')
    print("The unique ID for students and teachers are the following:")
    for i in stu:
        print(stu[i].name, 'has ID:', stu[i].student_id)
    for i in tea:
        print(tea[i].name, 'has ID:', tea[i].teacher_id)
        
    
    output = {
        1:[Person],
        2:[Student, stu, Teacher, tea],
        3:[Lecture, lec],
        4:[Lecture, lec],
        5:[Student, stu, Teacher, tea]
    }
    return output
        
## Running 
exercise_1(p,q,r)
