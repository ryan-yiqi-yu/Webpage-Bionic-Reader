from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
#from docx import Document
import html


url = 'https://en.wikipedia.org/wiki/Welsh_Corgi'
text_file = 'sitedata.txt'

def tag_visible(element):
    #if element is in any of the following headers it returns false
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:

        return False
    #if element is a comment, ignore it as well (false)
    if isinstance(element, Comment):

        return False
    #Element cannot be any of those headers or a comment
    return True

def bold_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True) #This gets inside HTML tags to get the text
    for data in filter(tag_visible, texts):
        if data.isspace():
            continue
        #new_tag = soup.new_tag("a", href="http://www.example.com")
        #print(type(soup.b))
        #soup.b.append(new_tag)
        #new_tag.string = "Link text."
        #data.decompose()
        data.replace_with(bold_words_html(data))
        #print(soup.prettify(formatter=None))
    with open("output1.html", "w") as file:
        file.write(soup.prettify(formatter=None))



def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True) #This gets inside HTML tags to get the text
    visible_texts = list(filter(tag_visible, texts))  #Filters the text
    #good = (visible_texts)

    #return " ".join(t.strip() for t in visible_texts)
    #print(u" ".join(g.strip() for g in visible_texts))
    text_to_doc = []
    with open (text_file, 'a') as goods: #Appends to the file rather than overwriting
        for g in visible_texts: #goes through all the texts found
            if not g.isspace(): #filters out all the whitespace
                #print("/////////////////////")
                bold_words_html(g)



                goods.write("\n\n") #goods is the file, write two spaces to file
                try:
                    goods.write(str(g.strip()))
                    break_up(str(g.strip()))  #sends to break up string into list to bold it
                except UnicodeEncodeError:
                    pass
                    #goods.write(str((g.strip()).encode('utf-8')))

def bold_words_html(str):
    words_list = []
    for word in str.strip().split(" "):
        #if word.isalnum():
        if word:
            word = "<b>" + word[:len(word)//2] + "</b>" + word[len(word)//2:]
        words_list.append(word)
    sentence = " ".join(words_list)
    return sentence



def break_up(stuff):
    string = stuff
    x = string.split(" ")
    bold(x) #makes stuff bold
    #print("This is x: ",x)

def bold(stuff):
    temp = []
    for words in stuff:
        first = '\033[1m' + words[:len(words)//2] + '\033[0m' #this bolds the first half of the word
        last = words[len(words)//2:]    #last half of word
        good_word = first + last        #Combines the bolded first half and the last half
        temp.append(good_word)          #puts the modified word into a list
    sentence = " ".join(temp)           #joins all the stuff in the list into a sentence
    #print(sentence)                     #Outputs the sentence

def word_doc(bold):
    doc = Document()
    doc._body.clear_content()
    doc.save("out.docx")

def init(): #supposed to spawn file, and make it blank for new data

    with open(text_file, 'w') as f:
        f.truncate(0)

    #Gets contents of webpage and can bypass common bot detectors
    page = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    #Reads html stuff from the contents
    html = urlopen(page).read()
    return html

def main():
    webpage_stuff = init() #Gets contents of webpage
    #html = urllib.request.urlopen('https://www.yahoo.com/').read()

    bold_html(webpage_stuff) #Extracts text from the webpage contents hopefully
    #word_doc()

main()
'''
with open('sitedata.txt', 'w') as f:
    f.write(str(stuff.encode("utf-8")))
'''
