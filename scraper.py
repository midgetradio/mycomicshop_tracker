from bs4 import BeautifulSoup
from Issue import Issue
import requests
import json

# Methods
url = ["https://www.mycomicshop.com/search?TID=95961"]

singleIssueURL = 'https://www.mycomicshop.com/search?iid=8481991'

page = requests.get(singleIssueURL)
page_soup = BeautifulSoup(page.content, "html.parser")

#TODO: pass the MCS IID to a function to call this method for single issue parsing, pass the VOL ID for entire volume parsing
def parse_single_issue(singleIssueHTML):
    f = open("page.html", "w")
    f.write(str(singleIssueHTML))

    issue_number_title = singleIssueHTML.find(class_ = "othercolleft")
    title = issue_number_title.a.string
    issue_number = issue_number_title.strong.string

    publisher_content = singleIssueHTML.find(class_ = "othercolright").find_all("a")
    date_published = publisher_content[0].string
    publisher = publisher_content[1].string

    description_content = singleIssueHTML.find(class_ = "tabcontents")
    description = "No Description" if description_content.p is None else description_content.p.string

    price_list = []
    grade_list = []

    price_grade_list = singleIssueHTML.find_all(class_="group")
    
    for price_grade_item in price_grade_list:
        price_grade = price_grade_item.find(class_ = "addcart")
        if(price_grade != None):
            price = price_grade.a.contents[2]
            grade_unparsed = price_grade_item.find(class_ = "hasscan").contents[0]
            grade = str(grade_unparsed).replace("\n", "") #TODO: Create separate function to parse grade, check length of grade string, if 0, set to "No grade"
            price_list.append(price)
            grade_list.append(grade)


    print(title)
    print(issue_number)
    print(date_published)
    print(publisher)
    print(description)
    print(grade_list)
    print(price_list)

parse_single_issue(page_soup)

def CreateURLList(urls):
    print("Grabbing urls...")
    url_list = urls
    soup_list = []
    counter = 0
    length = len(url_list)
    for url in url_list:
        counter = counter + 1
        print("Page " + str(counter) + " of " + str(length))
        page = requests.get(url)
        soup_list.append(BeautifulSoup(page.content, "html.parser"))
    return soup_list

# list = CreateURLList(url)
# f = open("page.html", "w")
# f.write(str(list[0]))

# print(list)

def CreateIssueList(soup_list):
    
    print("Creating price list...")

    issue_list = []
    soup_list_length = len(soup_list)

    title = soup_list[0].title.string

    print(title)

    for x in range (soup_list_length):
        for issueinfo in soup_list[x].find_all("li", class_="issue"):
            # create empty price_list and grade_list arrays for each issue
            price_list = []
            grade_list = []

            # find and assign the img url
            img_html = issueinfo.find_all(class_= "img")
            img_src = "No image url" if img_html[0].img is None else img_html[0].img['src']

            # find and assign issue number
            issue_html = issueinfo.find_all(class_ = "title")
            issue_num = issue_html[0].find("strong").string[1:]

            # find and assign the publisher and publication date
            date_html = issueinfo.find_all(class_ = "othercolright")
            datePub = date_html[0].find_all("a")
            date = datePub[0].string
            publisher = datePub[1].string

            # find, format and assign the description
            description_html = issueinfo.find_all(class_ = "tabcontents")
            description = "none"
            description_text = description_html[0].find_all("p")
            if(len(description_text) > 0):
                description = description_text[-1].string
            if(description == None):
                description = "No description"

            # find and assign the mcs_id
            mcs_id = issueinfo.a['name']
            
            # find and populate the price and grade arrays
            price_grade_list = issueinfo.find_all(class_="addcart")
            max = len(price_grade_list)
            for x in range(max):
                price_list.append(price_grade_list[x].a['data-price'])
                if(len(price_grade_list[x].a.contents) > 2):
                    grade_list.append(price_grade_list[x].a.contents[2])
                else:
                    grade_list.append("No Grade")
                

            # create the issue object and append it to the issue_list array
            issue = Issue.buildIssue(issue_num, date, description, img_src, mcs_id, grade_list, price_list, title, publisher)
            issue_list.append(issue)

    # return a list of issue objects
    return issue_list

# isslist = CreateIssueList(list)

# js = json.dumps(isslist[0].__dict__)

# print(js)

# f = open("iss.json", "w")
# f.write(js)

# for x in range (0, 10):
#     print(isslist[x].issue_string())
#     print()


