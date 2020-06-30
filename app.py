from flask import Flask, render_template, request

import time
import json
from datetime import datetime
import pandas as pd 
from plyer import notification
import urllib.request
from bs4 import BeautifulSoup
import re
#from download import download
from urllib.request import urlretrieve
from urllib.parse import quote,urlencode

# def notifyMe(title,message):
#     notification.notify(
# 		title = title,
# 		message = message,
# 		#=app_icon = "path_to_ico"          # use .ico image file
# 		timeout = 5
# 	) 




local_server = True
app = Flask(__name__)


df = pd.read_excel("s.xlsx")
categories = df["English Package Name"]






@app.route("/")
def home():
    
    return render_template('index.html', categories=set(categories))







@app.route("/<string:category>")
def category(category):
    books  = df[df["English Package Name"]==category]["Book Title"]
    return render_template('index2.html', books= set(books) )




def pdf(liel):
     if "/content/pdf" in liel:
         return True






@app.route("/category/<string:boook>")
def boook(boook):
    try:
        url  = str(df[df["Book Title"]==boook]["OpenURL"]).split("...")
        isb =  str(df[df["Book Title"]==boook]["Print ISBN"])
        u = re.sub(" +"," ",url[0])
        uu = u.split(" ")
        lin = uu[1]
        lin = lin+"bn="
        isb = re.sub(" +"," " ,isb)
        isbb = isb.split(" ")[1]
        finall = lin + isbb
        fi = finall.split("\n")
        res = urllib.request.urlopen(fi[0])
        htmls = res.read()
        soup = BeautifulSoup(htmls,'html.parser')
        tags = soup('a')
        li=[]
        for tag in tags:
            li.append(tag.get('href',None))
        f_list = list(filter(pdf, li))

        go = f_list[0].split("/")
        link = "link.springer.com/content/pdf/"+go[3]
        #notifyMe("Hello","Your Downlaod will start in 3 seconds")
        co = link.split("content")

        urll = "https://" + link
        pathh = "content" 

        return render_template("final.html",ur = urll)
    
    except:
        return render_template("index2.html", categories=set(categories))
     



if __name__ == '__main__':
    app.run(debug=True)


