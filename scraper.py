import csv
import re

# read the data into a list split by lines
rawData = open("data/raw.txt", "r").read().splitlines()

# Now take that data and put it into a list of lists (aka an associative array)
parsedData = []
i = -1
for row in rawData:
    if row == "Date: 03-05-2019":
        i += 1
        parsedData.append([])
    parsedData[i].append(row)


# This is the parse function for pre-k
# NOTE: varicella and MMR are both on 2 different lines.
# ASSUMPTION: combine the totals
def parse_pre_k(entry, pageNumber):
    return {
        "school": re.search("(?<=Calendar: )(.*)(?= Grade\/group)", entry[5]).group(1),
        "grade": format_grade(
            re.search("(?<=Grade\/group being reported: )(.*)", entry[5]).group(1)
        ),
        "kpop": re.search("(\d+)(?!.*\d)", entry[8]).group(1),
        "DTAP": re.search("(\d+)(?!.*\d)", entry[16]).group(1),
        "Polio": re.search("(\d+)(?!.*\d)", entry[17]).group(1),
        "HepB": re.search("(\d+)(?!.*\d)", entry[19]).group(1),
        "MMR": int(re.search("(\d+)(?!.*\d)", entry[23]).group(1))
        + int(re.search("(\d+)(?!.*\d)", entry[26]).group(1)),
        "Varicel": int(re.search("(\d+)(?!.*\d)", entry[24]).group(1))
        + int(re.search("(\d+)(?!.*\d)", entry[27]).group(1)),
        "HepA": re.search("(\d+)(?!.*\d)", entry[21]).group(1),
        "missing": re.search("(?<=file\? )(.*)(?= << CLICK)", entry[10]).group(1),
        "page": pageNumber + 1,
    }


# This is the parse function for the elementary schools
def parse_elementary(entry, pageNumber):
    return {
        "school": re.search("(?<=Calendar: )(.*)(?= Grade\/group)", entry[5]).group(1),
        "grade": format_grade(
            re.search("(?<=Grade\/group being reported: )(.*)", entry[5]).group(1)
        ),
        "kpop": re.search("(\d+)(?!.*\d)", entry[8]).group(1),
        "DTAP": re.search("(\d+)(?!.*\d)", entry[16]).group(1),
        "Polio": re.search("(\d+)(?!.*\d)", entry[17]).group(1),
        "HepB": re.search("(\d+)(?!.*\d)", entry[18]).group(1),
        "MMR": re.search("(\d+)(?!.*\d)", entry[19]).group(1),
        "Varicel": re.search("(\d+)(?!.*\d)", entry[20]).group(1),
        "HepA": re.search("(\d+)(?!.*\d)", entry[21]).group(1),
        "missing": re.search("(?<=file\? )(.*)(?= << CLICK)", entry[10]).group(1),
        "page": pageNumber + 1,
    }


# This is the parse function for the middle and high schools
# NOTE: hepB appears on two lines
# ASSUMPTION: the total appears to be combined on line 25, but not positive
def parse_middle_and_high(entry, pageNumber):
    return {
        "school": re.search("(?<=Calendar: )(.*)(?= Grade\/group)", entry[5]).group(1),
        "grade": format_grade(
            re.search("(?<=Grade\/group being reported: )(.*)", entry[5]).group(1)
        ),
        "kpop": re.search("(\d+)(?!.*\d)", entry[8]).group(1),
        "tdap": re.search("(\d+)(?!.*\d)", entry[16]).group(1),
        "tdBooster": re.search("(\d+)(?!.*\d)", entry[17]).group(1),
        "MCV": re.search("(\d+)(?!.*\d)", entry[18]).group(1),
        "HepB": re.search("(\d+)(?!.*\d)", entry[25]).group(1),
        "MMR": re.search("(\d+)(?!.*\d)", entry[26]).group(1),
        "HepA": re.search("(\d+)(?!.*\d)", entry[27]).group(1),
        "Varicel": re.search("(\d+)(?!.*\d)", entry[28]).group(1),
        "missing": re.search("(?<=file\? )(.*)(?= << CLICK)", entry[10]).group(1),
        "page": pageNumber + 1,
    }


# Convert text based grade to a more concise/numerical one
def format_grade(grade):
    numericalGrades = [
        "First Grade",
        "Second Grade",
        "Third Grade",
        "Fourth Grade",
        "Fifth Grade",
        "Sixth Grade",
        "Seventh Grade",
        "Eighth Grade",
        "Ninth Grade",
        "Tenth Grade",
        "Eleventh Grade",
        "Twelfth Grade",
    ]
    if grade == "Daycare/Head Start/Preschool":
        return "pre-k"
    if grade == "Kindergarten":
        return "k"
    if grade in numericalGrades:
        return numericalGrades.index(grade) + 1


# Setup our temporary holders for each category of our parsed data
csvPreK = []
csvElementary = []
csvMiddleAndHigh = []


# Loop through each entry(page) of our parsedData, figure out which grade we're in, then
# call the appropriate function to parse the data out of that entry and add it to our temp holder
for pageNumber, entry in enumerate(parsedData):
    grade = re.search("(?<=Grade\/group being reported: )(.*)", entry[5]).group(1)
    if grade in ["Daycare/Head Start/Preschool"]:
        csvPreK.append(parse_pre_k(entry, pageNumber))
    if grade in [
        "Kindergarten",
        "First Grade",
        "Second Grade",
        "Third Grade",
        "Fourth Grade",
        "Fifth Grade",
    ]:
        csvElementary.append(parse_elementary(entry, pageNumber))
    if grade in [
        "Sixth Grade",
        "Seventh Grade",
        "Eighth Grade",
        "Ninth Grade",
        "Tenth Grade",
        "Eleventh Grade",
        "Twelfth Grade",
    ]:
        csvMiddleAndHigh.append(parse_middle_and_high(entry, pageNumber))



# Write pre-k data
with open("output/pre-k.csv", "w", newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, csvPreK[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(csvPreK)


# Write elementary data
with open("output/elementary.csv", "w", newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, csvElementary[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(csvElementary)


# Write middle and highschool data
with open("output/middle-and-high.csv", "w", newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, csvMiddleAndHigh[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(csvMiddleAndHigh)
