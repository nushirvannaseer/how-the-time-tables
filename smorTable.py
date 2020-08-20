class course:
    def __init__(self, name, startHour, startMin, endHour, endMin):
        self.name = name
        self.startHour = startHour
        self.startMin = startMin
        self.endHour = endHour
        self.endMin = endMin


def compareTimes(prevEndHour, startHour):
    if (prevEndMin < 0):
        return False
    if prevEndHour < 8:
        prevEndHour += 12
    if startHour < 8:
        startHour += 12
    return prevEndHour > startHour


def createTable(table, file):
    file = open("timeTable.csv", "r")
    line = file.readlines()
    dayOfTheWeek = ""

    for i in range(4, len(line)):
        list = line[i].split(";")
        hrCount = 0
        count = 0
        startHour = 8
        startMin = 0
        endHour = 0
        endMin = 0
        if list[0] != "":
            days = list[0].split(" ")
            dayOfTheWeek = days[0]
        for j in range(6, len(list)):
            if list[j] != "":
                duration = 0
                if list[j].find("Lab") != -1:
                    endMin = startMin
                    endHour = (startHour + 3) % 12
                    #duration += 180

                elif list[j].find("English") != -1:
                    endMin = startMin
                    endHour = (startHour + 2) % 12
                    #duration += 120

                else:
                    # duration += 90
                    endMin = (startMin + 30) % 60
                    if endMin == 0:
                        endHour = startHour + 2
                    else:
                        endHour = startHour + 1

                    if endHour > 12:
                        endHour -= 12

                c = course(list[j], startHour, startMin, endHour, endMin)
                if (table[dayOfTheWeek][count] == None):
                    table[dayOfTheWeek][count] = []
                    table[dayOfTheWeek][count].append(c)
                else:
                    table[dayOfTheWeek][count].append(c)
            count += 1
            if hrCount == 5:
                startHour += 1
                if startHour > 12:
                    startHour -= 12
                startMin = 0
                hrCount = 0
            else:
                startMin = (startMin + 10) % 60
                hrCount += 1


if __name__ == "__main__":
    table = {
        "Monday": [None] * 10000,
        "Tuesday": [None] * 1000,
        "Wednesday": [None] * 1000,
        "Thursday": [None] * 1000,
        "Friday": [None] * 1000,
    }
    filename = input("Enter the csv file's name or path: ")
    outputFile = open("OutputTimeTable.txt", "a+")
    separator = "#####################################\n#####################################\n#####################################\n"
    createTable(table, filename)

    while True:
        prevEndHour = -1
        prevEndMin = -1
        coursesStr = str(
            input(
                "Enter your courses separated by a forward slash (Type 'exit' to close the program): "
            ))
        #coursesStr = "Theory of Automata (BCS-5C)/Software Design & Analysis (BCS-5C)/Numerical Computing (BCS-5C)/Computer Networks (BCS-5C)/Computer Networks Lab  (BCS-5C1, BCS-5C2)"
        if coursesStr == "exit": break

        outputFile.write(coursesStr + '\n\n')
        print('\n\n')
        coursesList = coursesStr.split("/")

        i = 0
        days = 0
        courses = [""] * 5
        for key in table:
            print("####################################\n")
            print(key + ":\n")
            outputFile.write("####################################\n")
            outputFile.write(key + ":\n")

            prevEndMin = prevEndHour = -1
            for i in range(len(table[key])):
                if table[key][i] != None:
                    clashCount = 0
                    for j in range(len(table[key][i])):
                        if table[key][i][j].name in coursesList:
                            tempCourse = table[key][i][j]
                            clashCount += 1
                            if (compareTimes(
                                    prevEndHour + float(prevEndMin / 60),
                                    tempCourse.startHour +
                                    float(tempCourse.startMin / 60))):
                                clashCount += 1

                            prevEndHour = tempCourse.endHour
                            prevEndMin = tempCourse.endMin

                            courses[days] += str(
                                tempCourse.name) + '\nStart: ' + str(
                                    tempCourse.startHour) + ":" + str(
                                        tempCourse.startMin) + '\nEnd: ' + str(
                                            tempCourse.endHour) + ":" + str(
                                                tempCourse.endMin) + '\n'
                    if clashCount > 1:
                        courses[days] += "<<<CLASH EXISTS>>>\n\n"

            if courses[days] != "":
                print(courses[days] + '\n')
                outputFile.write(courses[days] + '\n')
            days += 1
        print(separator)
        outputFile.write(separator)
