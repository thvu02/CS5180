from bs4 import BeautifulSoup
from pymongo import MongoClient

if __name__ == '__main__':
    # Connect to MongoDB
    DB_NAME = "CPP"
    DB_HOST = "localhost"
    DB_PORT = 27017
    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        pages = db['pages']
        professors = db['professors']
    except:
        print("Database not connected successfully")

    # Retrieve the faculty HTML page from pages collection
    faculty = pages.find_one({"url": "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"})
    bs = BeautifulSoup(faculty['html'], 'html.parser')
    tracker = {} # Store faculty info in dict; key = name, value = [title, office, phone, email, website]
    for h2_tag in bs.find('section', {'class': 'text-images'}).find_all('h2'):
        # Extract faculty's name from h2 tag
        name = h2_tag.get_text(strip=True)
        tracker[name] = []

        # Get the next sibling until reach p tag
        next_sibling = h2_tag.find_next_sibling()
        while next_sibling and next_sibling.name != 'p':
            next_sibling = next_sibling.find_next_sibling()

        # Extract content from p tag
        if next_sibling and next_sibling.name == 'p':
            for strong_tag in next_sibling.find_all('strong'):
                value = ""
                next_sibling = strong_tag.next_sibling
                while next_sibling and next_sibling.name != 'br':
                    # CASE: plain text (title, office, phone)
                    if isinstance(next_sibling, str):
                        # some entries have a leading ": " that needs to be removed
                        value += next_sibling.get_text(strip=True).lstrip(': ')
                    # CASE: href (email, website)
                    elif next_sibling.name == 'a':
                        value += next_sibling.get_text(strip=True)
                    next_sibling = next_sibling.next_sibling
                tracker[name].append(value)
    
    # Create a document for each professor in the professors collection
    for professor in tracker:
        entry = {
            'name': professor,
            'title': tracker[professor][0],
            'office': tracker[professor][1],
            'phone': tracker[professor][2],
            'email': tracker[professor][3],
            'website': tracker[professor][4]
        }
        professors.insert_one(entry)