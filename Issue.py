class Issue(object):
    
    # Grade/Price Arrays
    grade_list = []
    price_list = []

    def __init__(self, **kwargs):
        self.issue_num = kwargs['iss_num']
        self.publication_date = kwargs['pub_date']
        self.description = kwargs['des']
        self.img_url = kwargs['i_url']
        self.mcs_id = kwargs['mcs']
        self.grade_list = kwargs['l1']
        self.price_list = kwargs['l2']
        self.volume_title = kwargs['voltitle']
        self.publisher = kwargs['pub']
    
    @classmethod
    def buildIssue(cls, issue_num, publication_date, description, img_url, mcs_id, grade_list, price_list, volume_title, publisher):
        #kind = 1
        return cls(iss_num=issue_num, pub_date=publication_date, des=description, i_url=img_url, mcs=mcs_id, l1 = grade_list, l2=price_list, voltitle=volume_title, pub=publisher)

    def __str__(self):
        return "Issue Number:\t\t" + str(self.issue_num) + "\n" + \
               "Volume Title:\t\t" + self.volume_title + "\n" + \
               "Publisher:\t\t" + self.publisher + "\n" + \
               "Publication Date:\t" + self.publication_date + "\n" + \
               "Image URL:\t\t" + self.img_url + "\n" + \
               "Description:\t\t" + self.description + "\n" + \
               "MCS_ID:\t\t\t" + str(self.mcs_id) + "\n" + \
               "Grade List:\t\t" + str(self.grade_list) + "\n" + \
               "Price List:\t\t" + str(self.price_list)

    def dump(self):
        return {    "Title": self.volume_title,
                    "Issue Number": self.issue_num,
                    "Publisher": self.publisher,
                    "Publication Date": self.publication_date,
                    "Image URL": self.img_url,
                    "Description": self.description,
                    "MCS_ID": self.mcs_id,
                    "Grade List": self.grade_list,
                    "Price List": self.price_list   }