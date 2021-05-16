from Scraper import Scraper
import json

def process_volume(url, id, scraper):
    issues_list = []

    page = scraper.getPageContent(url)
    list_urls = scraper.get_each_page_for_volume(id, page)
    
    for i in range(0, len(list_urls) + 1):
        issue_blocks = scraper.get_issue_blocks(page)
        
        for issue_block in issue_blocks:
            issue = scraper.parse_single_issue(issue_block)
            issues_list.append(issue)
        
        print("processing page " + str(i + 1) + " of " + str(len(list_urls) + 1) + " title: " + issues_list[-1].volume_title)

        if(i < len(list_urls)):
            page = scraper.getPageContent(list_urls[i])

    return issues_list

def main():
    scraper = Scraper()
    volume_urls = []
    singles_urls = []
    issues_list = []
    volume_ids = []
    single_ids = []

    # read from the json file
    json_file = open("issue_tracking.json")
    data = json.load(json_file)

    volumes = data['volumes']
    singles = data['singles']

    for volume in volumes.values():
        volume_ids.append(volume)

    for single in singles.values():
        single_ids.append(single)

    # if single => process single, if volume => process volume
    for id in volume_ids:
        url = scraper.buildURL(str(id), scraper.baseURL_series)
        volume_urls.append(url)
    
    for id in single_ids:
        url = scraper.buildURL(str(id), scraper.baseURL_singleIssue)
        singles_urls.append(url)

    # process single issues
    for x in range(len(singles_urls)):
        page = scraper.getPageContent(singles_urls[x])
        issue = scraper.parse_single_issue(page)
        issues_list.append(issue)
        print("processed " + issues_list[-1].volume_title + "...")

    # process volumes
    for x in range(len(volume_urls)):
        volume = process_volume(volume_urls[x], volume_ids[x], scraper)
        issues_list.extend(volume)

    # print
    print(issues_list[-1])

main()