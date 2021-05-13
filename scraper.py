from bs4 import BeautifulSoup
from Issue import Issue
import requests
import json

# Methods
# url = ["https://www.mycomicshop.com/search?TID=95961"]
# singleIssueURL = 'https://www.mycomicshop.com/search?iid=8481991'

baseURL_singleIssue = "https://www.mycomicshop.com/search?iid="
baseURL_series = "https://www.mycomicshop.com/search?tid="
mcs_id = "8481991"

def buildURL(id, baseURL):
    return baseURL + id

def getPageContent(url):
    page = requests.get(url)
    page_soup = BeautifulSoup(page.content, "html.parser")
    return page_soup

def parse_grade(grade_unparsed):
    grade = "No Grade"
    if(len(str(grade_unparsed)) > 0):
        grade = str(grade_unparsed).replace("\n", "")
    return grade

#TODO: pass the MCS IID to a function to call this method for single issue parsing, pass the VOL ID for entire volume parsing
def parse_single_issue(singleIssueHTML):

    # Get the issue number and title
    issue_number_title = singleIssueHTML.find(class_ = "othercolleft")
    title = issue_number_title.a.string
    issue_number = issue_number_title.strong.string

    # Get the publisher and date published
    publisher_content = singleIssueHTML.find(class_ = "othercolright").find_all("a")
    date_published = publisher_content[0].string
    publisher = publisher_content[1].string

    # Get the description
    description_content = singleIssueHTML.find(class_ = "tabcontents")
    description = "No Description" if description_content.p is None else description_content.p.string

    # Get the image url
    img_url = singleIssueHTML.find(class_ = "fancyboxthis")['href']

    # Get the mcs id
    mcs_id = singleIssueHTML.find(class_ = "fancyboxthis")['id']
    
    # Get the prices/grades
    price_list = []
    grade_list = []

    price_grade_list = singleIssueHTML.find_all(class_="group")
    
    for price_grade_item in price_grade_list:
        price_grade = price_grade_item.find(class_ = "addcart")
        if(price_grade != None):
            price = price_grade.a.contents[2]
            grade_unparsed = price_grade_item.find(class_ = "hasscan").contents[0]
            grade = parse_grade(grade_unparsed)
            price_list.append(price)
            grade_list.append(grade)

    issue = Issue.buildIssue(issue_number, date_published, description, img_url, mcs_id, grade_list, price_list, title, publisher)

    return issue


urlTest = "https://www.mycomicshop.com/search?TID=95961"
page = getPageContent(urlTest)

# f = open("page.html", "w")
# f.write(str(page))

remaining_page_numbers = page.find(class_ = "paginate")
remaining_pages = remaining_page_numbers.find_all("a")
rp = []

for remaining in remaining_pages:
    if(remaining.string == "Next"):
        continue
    rp.append(urlTest + "&pgi=" + remaining.string)

print(rp)

issue_soup_list = page.find_all(class_ = "issue")
issue = parse_single_issue(issue_soup_list[49])
# print(issue.issue_string())


# url = buildURL(mcs_id, baseURL_singleIssue)
# page = getPageContent(url)
# issue = parse_single_issue(page)

# print(issue.issue_string())












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


