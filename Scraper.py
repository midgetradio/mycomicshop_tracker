from bs4 import BeautifulSoup
from Issue import Issue
import requests
import json

mcs_id = "8481991"
vol_id = "82151"

class Scraper():
    
    baseURL_singleIssue = "https://www.mycomicshop.com/search?iid="
    baseURL_series = "https://www.mycomicshop.com/search?tid="

    def buildURL(self, id, baseURL):
        return baseURL + id

    def getPageContent(self, url):
        page = requests.get(url)
        page_soup = BeautifulSoup(page.content, "html.parser")
        return page_soup

    def parse_price(self, price_unparsed):
        price = "No price"
        if(len(str(price_unparsed)) > 0):
            price = str(price_unparsed).replace("\n", "")
        return price.strip()

    def parse_grade(self, grade_unparsed):
        grade = "No Grade"
        if(len(str(grade_unparsed)) > 0):
            grade = str(grade_unparsed).replace("\n", "")
        return grade.strip()

    def parse_single_issue(self, singleIssueHTML):
        # Get the issue number and title
        issue_number_title = singleIssueHTML.find(class_ = "othercolleft")
        
        title = "No title" if issue_number_title.a is None else issue_number_title.a.string

        issue_number = "No number" if issue_number_title.strong.string is None else issue_number_title.strong.string

        # Get the publisher and date published
        publisher_content = singleIssueHTML.find(class_ = "othercolright").find_all("a")
        
        date_published = "NO date" if publisher_content[0] is None else publisher_content[0].string
        
        publisher = "No publisher" if publisher_content[1] is None else publisher_content[1].string

        # Get the description
        description_content = singleIssueHTML.find(class_ = "tabcontents")
        description = "No Description" if description_content.p.string is None else description_content.p.string

        # Get the image url
        img_url = "No img url" if singleIssueHTML.find(class_ = "fancyboxthis")['href'] is None else singleIssueHTML.find(class_ = "fancyboxthis")['href']

        # Get the mcs id
        mcs_id = "No mcs_id" if singleIssueHTML.find(class_ = "fancyboxthis")['id'] is None else singleIssueHTML.find(class_ = "fancyboxthis")['id']

        # Get the prices/grades
        price_list = []
        grade_list = []

        price_grade_list = singleIssueHTML.find_all(class_="group")
        
        for price_grade_item in price_grade_list:
            price_grade = price_grade_item.find(class_ = "addcart")
            if(price_grade != None):
                price_unparsed = price_grade_item.find(class_ = "hasscan").contents[0]
                grade_unparsed = price_grade.a.contents[2]
                price = self.parse_price(price_unparsed)
                grade = self.parse_grade(grade_unparsed)
                price_list.append(price)
                grade_list.append(grade)

        issue = Issue.buildIssue(issue_number, date_published, description, img_url, mcs_id, grade_list, price_list, title, publisher)

        return issue

    def get_each_page_for_volume(self, id, page):
        page_containing_indices = page.find(class_ = "paginate")
        list_of_indices = page_containing_indices.find_all("a")
        vol_urls_list = []
        for page_index in list_of_indices:
            if(page_index.string == "Next"):
                continue
            vol_urls_list.append(self.baseURL_series + str(id) + "&pgi=" + page_index.string)
        return vol_urls_list
    
    def get_issue_blocks(self, page):
        issue_blocks = page.find_all(class_ = "issue")
        return issue_blocks