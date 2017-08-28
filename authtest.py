import requests, lxml.html
from bs4 import BeautifulSoup as soup


#Starting a session to stay maintain authorized state
s = requests.session()
#creating csv file for storing alum info
fileName = "alums.csv"
f = open(fileName, "w")
headers = "alum_name, class_year, major, email_address, address\n"
f.write(headers)
#variables to store alum info
num_alums = 0
num_emails = 0
num_addresses = 0
#looping over all class years we want the information from
for year in range(1950,2018):
    #link to the authorization page
    alum_url = 'https://apps.carleton.edu/login/?dest_page=https%3A%2F%2Fapps.carleton.edu%2Falumni%2Fdirectory%2F%3Fclass_years%3D'+ str(year) +'%26living_only%3D1&msg_uname=alumni_directory_login_msg'
    login = s.get(alum_url)
    login_html = lxml.html.fromstring(login.text)
    hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
    #username and password for logging in
    form['username'] = ''
    form['password'] = ''
    response = s.post(alum_url, data=form)
    page_html =  response.content
    #parsing html in the returned page
    page_soup = soup(page_html, "html.parser")
    #all alums on a page are in a 'ul' element
    container = page_soup.find("ul",{"class":"results"})

    #each div with inside the list with class living is an alive person
    alums = container.findAll("div", {"class":"person"})
    num_alums = num_alums + len(alums)
    #looping over all alums from a class year
    for alum in alums:
        name = alum.find("h3").text.encode('ascii', 'ignore')
        alum_year = alum.find("span", {"class":"year"}).text.encode('ascii', 'ignore')
        major = alum.find("span", {"class":"major"}).text.encode('ascii', 'ignore')
        if alum.find("p", {"class":"email"}) != None:
            email = alum.find("p", {"class":"email"}).text.encode('ascii', 'ignore')
            num_emails = num_emails + 1
        else:
            email = "(No email address found)"
        if alum.find("p", {"class":"address"}) != None:
            address = alum.find("p", {"class":"address"}).text.encode('ascii', 'ignore').replace(',', ' ')
            num_addresses = num_addresses + 1
        else:
            address = "(No email address found)"
        #writing attributes to the csv file
        f.write(name + "," + alum_year + "," + major + "," + email + "," + address + "\n" )
#printing stats at the end of a run
print "number of alums: " + str(num_alums) + "\n" + "number of emails: " + str(num_emails) + "\n" + "number of addresses: " + str(num_addresses)
f.close()