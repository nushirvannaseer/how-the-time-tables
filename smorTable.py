import math


class course:
    def __init__(self, name, startMin, endMin):
        self.name = name
        self.startMin = startMin
        self.endMin = endMin


def toHoursAndMinutes(time):
    hours = int((time * 10) / 60)
    minutes = int(60 * (float((time * 10) / 60) - hours))
    if hours > 12:
        hours -= 12
    return str(hours) + ":" + str(minutes)


def createTable(table, file, courseList):
    file = open("t1.csv", "r")
    line = file.readlines()
    dayOfTheWeek = ""

    for i in range(4, len(line)):
        list = line[i].split(";")
        count = 0
        startMin = 48
        endMin = 0
        if list[0] != "":
            days = list[0].split(" ")
            if days[0] == "" or days[0] == " ":
                days[0] = days[1]
            dayOfTheWeek = days[0]

        for j in range(6, len(list)):

            if list[j] != "" and not list[j].isdigit() and not list[j].isspace(
            ):
                # add course name to completeCourseList
                if list[j] not in courseList:
                    courseList.append(list[j])

                duration = 1
                while list[duration + j] == "":
                    duration += 1
                if duration >= 18:
                    if list[j].find("Lab") > -1:
                        duration = 18
                    elif list[j].find("english") > -1:
                        duration = 12
                    else:
                        duration = 9
                endMin = startMin + duration

                c = course(list[j], startMin, endMin)
                if (table[dayOfTheWeek][count] == None):
                    table[dayOfTheWeek][count] = []
                    table[dayOfTheWeek][count].append(c)
                else:
                    table[dayOfTheWeek][count].append(c)
            count += 1
            startMin += 1


def printTimeTable(outputTimeTable, outputFile=None):
    for key in outputTimeTable:
        print("\n**********************************")
        print(str(key).upper() + ":\n")
        if outputFile != None:
            outputFile.write("\n**********************************\n" +
                             str(key).upper() + ":\n")
        for obj in outputTimeTable[key]:
            name = obj.name
            start = toHoursAndMinutes(obj.startMin)
            end = toHoursAndMinutes(obj.endMin)
            print("\t" + name + "\t" + start + " to " + end)
            if outputFile != None:
                outputFile.write("\t" + name + "\t" + start + " to " + end)
                outputFile.write("\n")


def printClashTable(Table, outputFile=None):
    for key in Table:
        print("\n**********************************")
        print(str(key).upper() + ":")
        if outputFile != None:
            outputFile.write("\n**********************************\n" +
                             str(key).upper() + ":\n")
        for obj in Table[key]:
            name = obj.name
            start = toHoursAndMinutes(obj.startMin)
            end = toHoursAndMinutes(obj.endMin)
            print("\t-> " + name + "\t" + start + " to " + end)
            if outputFile != None:
                outputFile.write("\t-> " + name + "\t" + start + " to " + end)
                outputFile.write("\n")


#!experimental
def findSuggestedCourse(OutputTimeTable, clashingCourses,
                        clashingCoursesAlternatives):
    suggestions = []
    for key in clashingCourses:
        for clashingCourse in clashingCourses[key]:
            temp = clashingCourse.name.split(" (")
            # getting the clashing course's name without the section
            clashingCourseName = temp[0]
            # now partially match the clashing course name with one of the names
            # in the alternatives list
            for key2 in clashingCoursesAlternatives:
                for alt in clashingCoursesAlternatives[key2]:

                    if alt.name.find(clashingCourseName) > -1:
                        altRejected = False
                        for key3 in OutputTimeTable:
                            if altRejected == True:
                                break
                            for desiredCourse in OutputTimeTable[key3]:
                                if desiredCourse.name != clashingCourse.name:
                                    # if alt.startMin<desiredCourse.start and alt.endMin<desiredCourse.startMin:

                                    x = range(alt.startMin + 1, alt.endMin - 1)
                                    y = range(desiredCourse.startMin,
                                              desiredCourse.endMin)
                                    xs = set(x)
                                    intersect = xs.intersection(y)
                                    # if the time of alt course interescts that of existing,
                                    # then reject that alt course
                                    if len(intersect) > 0:
                                        altRejected = True
                                        break
                    # altRejected = False

                if altRejected == False and alt.name.find(
                        clashingCourseName) > -1:
                    string = "Try using "+alt.name+" instead of "+clashingCourse.name+"\n" +\
                        "(" + toHoursAndMinutes(alt.startMin)+") to (" + \
                        toHoursAndMinutes(alt.endMin)+") on "+key
                    suggestions.append(string)
    return suggestions


if __name__ == "__main__":
    table = {
        "Monday": [None] * 100,
        "Tuesday": [None] * 100,
        "Wednesday": [None] * 100,
        "Thursday": [None] * 100,
        "Friday": [None] * 100,
    }
    completeCourseList = []

    # filename = input("Enter the csv file's name or path: ")
    filename = "timeTable.csv"
    outputFile = open("OutputTimeTable.txt", "a+")
    # separator = "#####################################\n#####################################\n#####################################\n"
    createTable(table, filename, completeCourseList)
    completeCourseList.sort()

    while True:
        clashingCourses = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
        }
        clashingCoursesAlternatives = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
        }

        OutputTimeTable = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
        }
        print("\nComplete Courses List:\n")

        x = 1
        for courseName in completeCourseList:
            print(str(x) + ". " + courseName)
            x += 1
        giveSuggestions = False
        getAlternatives = False
        print("\n")

        while True:
            gs = input(
                "Do you want to get suggestions for clash resolution? (Experimental) y/n:"
            )
            if gs == "n" or gs == "N":
                giveSuggestions = False
                break
            elif gs == "y" or gs == "Y":
                giveSuggestions = True
                break
        while True:
            gs = input(
                "Do you want to print a list of alternative courses? (Experimental) y/n:"
            )
            if gs == "n" or gs == "N":
                getAlternatives = False
                break
            elif gs == "y" or gs == "Y":
                getAlternatives = True
                break

        prevEndMin = -1
        coursesStr = str(
            input(
                "Enter the numbers corresponding to the courses you want separated by a comma(Type 'exit' to close the program): "
            ))
        # coursesStr = "Theory of Automata (BCS-5C)/Software Design & Analysis (BCS-5C)/Numerical Computing (BCS-5C)/Computer Networks (BCS-5C)/Computer Networks Lab  (BCS-5C1, BCS-5C2)"
        if coursesStr == "exit":
            break

        courseNamesWithoutSections = []
        print('\n\n')
        coursesList = coursesStr.split(",")
        selectedCourses = []
        st = "SELECTED COURSES"
        st = st.center(80, "-")
        print(st)
        print("\n")
        for index in coursesList:
            ind = int(index)
            if (ind >= len(completeCourseList) - 1):
                print("<!ERROR!> Enter a number in range! <!ERROR!>")
                exit()
            selectedCourses.append(completeCourseList[ind - 1])
            temp = completeCourseList[ind - 1].split(" (")
            courseNamesWithoutSections.append(temp[0])
            outputFile.write(completeCourseList[ind - 1] + "; ")
            print("\t-> " + completeCourseList[ind - 1])
        outputFile.write("\n\n")
        print("\n")

        i = 0
        clashingCourseIndex = -1
        for key in table:
            clashingCourseIndex = -1
            prevEndMin = -1
            for i in range(len(table[key])):
                if table[key][i] != None:
                    clashCount = 0
                    for j in range(len(table[key][i])):
                        tempCourse = None
                        if table[key][i][j].name in selectedCourses:
                            tempCourse = table[key][i][j]
                            clashCount += 1
                            clashingCourseIndex += 1
                            OutputTimeTable[key].append(tempCourse)

                            if prevEndMin > tempCourse.startMin:
                                clashingCourses[key].append(tempCourse)
                                length = len(OutputTimeTable[key]) - 2
                                clashingCourses[key].append(
                                    OutputTimeTable[key][length])
                            elif clashCount > 1:
                                clashingCourses[key].append(tempCourse)

                            prevEndMin = tempCourse.endMin

                        else:
                            for cnwoc in courseNamesWithoutSections:
                                if table[key][i][j].name.rfind(cnwoc) > -1:
                                    if table[key][i][
                                            j] not in clashingCoursesAlternatives[
                                                key]:
                                        clashingCoursesAlternatives[
                                            key].append(table[key][i][j])

        text = "TIME TABLE"
        text = text.center(80, "-")
        print(text)
        outputFile.write(text)
        outputFile.write("\n\n")
        printTimeTable(OutputTimeTable, outputFile)
        print("\n\n")
        outputFile.write("\n\n")
        st = "CLASHES"
        newStr = st.center(80, "-")
        print(newStr)
        outputFile.write(newStr)
        outputFile.write("\n\n")
        printClashTable(clashingCourses, outputFile)

        if giveSuggestions == True:
            print("\n\n")
            st = "SUGGESTIONS"
            st = st.center(80, "-")
            print(st)
            print("\n")
            outputFile.write(st)
            outputFile.write("\n\n")
            suggestions = findSuggestedCourse(OutputTimeTable, clashingCourses,
                                              clashingCoursesAlternatives)
            for s in suggestions:
                print("-> " + s)

        if getAlternatives == True:
            print("\n\n")
            st = "ALTERNATIVES"
            st = st.center(80, "-")
            print(st)
            print("\n")
            outputFile.write(st)
            outputFile.write("\n\n")
            printTimeTable(clashingCoursesAlternatives, outputFile)
            outputFile.write("\n\n\n")

        while True:
            cont = input("\nContinue? y/n:")
            if cont == "n" or cont == "N":
                exit()
            elif cont == "y" or cont == "Y":
                break
