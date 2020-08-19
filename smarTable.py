class course:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end


def createTable(table, file):
    file = open("timeTable.csv", "r")
    line = file.readlines()
    dayofTheWeek = ""

    for i in range(4, len(line)):
        list = line[i].split(",")
        count = 0
        time = 0
        if list[0] != "":
            days = list[0].split(" ")
            dayOfTheWeek = days[0]
        for j in range(3, len(list)):
            if list[j] == "":
                count += 1
                time += 10
            else:
                end = time
                # for k in range(j + 1, len(list)):
                #     if list[k] != "":
                #         break
                #     end += 10
                if list[j].find("Lab") != -1:
                    end += 170
                else:
                    end += 80
                c = course(list[j], time, end)
                if (table[dayOfTheWeek][count] == None):
                    table[dayOfTheWeek][count] = []
                    table[dayOfTheWeek][count].append(c)
                else:
                    table[dayOfTheWeek][count].append(c)
                count += 1
                time += 10


if __name__ == "__main__":
    table = {
        "Monday": [None] * 10000,
        "Tuesday": [None] * 1000,
        "Wednesday": [None] * 1000,
        "Thursday": [None] * 1000,
        "Friday": [None] * 1000,
    }

    createTable(table, "timeTable.csv")

    #coursesStr = input("Enter your courses separated by a comma:")
    coursesList = ["Operating Systems (BCS-5D)", "Data Science"]
    print(coursesList)
    print(table.keys)
    i = 0
    for key in table:
        for i in range(len(table[key])):
            if table[key][i] != None:
                for j in range(len(table[key][i])):
                    if table[key][i][j].name in coursesList:
                        print(key + ": " + str(table[key][i][j].name) + '\n' +
                              str(table[key][i][j].start) + '\n' +
                              str(table[key][i][j].end))
