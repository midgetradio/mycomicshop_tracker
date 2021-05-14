from Scraper import Scraper

def main():
    scraper = Scraper()

    id = "82151"

    # process single issues

    # process volumes

    url = scraper.buildURL(id, scraper.baseURL_series)
    page = scraper.getPageContent(url)

    # print(page)

    list_urls = scraper.get_each_page_for_volume(id, page)
    list_urls.insert(0, url)
    
    # print(list_urls)
    issue_pages = []

    # create list of pages
    for url in list_urls:
        page = scraper.getPageContent(url)
        issue_pages.append(page)

    # print(issue_pages)

    issues_object_list = []
    # create list of issues
    for issue_page in issue_pages:
        issue_list = issue_page.find_all(class_ = "issue")
        for issue in issue_list:
            iss = scraper.parse_single_issue(issue)
            issues_object_list.append(iss)


    print(len(issues_object_list))
    print(issues_object_list[0])

main()