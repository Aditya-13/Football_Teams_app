import requests
import json
import os
import PIL
import magic
from PIL import Image, ImageTk
from tkinter import Tk, Button, Canvas, Label, Entry

url = "https://api-football-v1.p.rapidapi.com/v3/teams"
src1 = " " # Enter the source where you want to download the Team logo (It will deleted after the program terminates)
src2 = " " # Enter the source where you want to download the Venue Image (It will deleted after the program terminates)

window = Tk()
window.geometry('600x800')
window.config(bg="white")
window.title('Football Data')

label1 = Label(window, text="Enter the name of the Team to search: ", fg="black", bg="white", font="Helvetica 14 normal")
label1.pack()

Label(window, text="").pack()

textArea = Entry(window, bg="Grey", fg="Black", font="Helvetica 14 normal")
textArea.pack()

Label(window, text="").pack()

def get_details():
    team = textArea.get()
    query_string = {"name":team}

    headers = {
        'x-rapidapi-key': "Enter your rapid api key here",
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=query_string)
    response_text = response.text

    with open("file1.json", "w") as file1:
        file1.write(response_text)
    file1.close()

    with open("file1.json","r+") as file:
        data = json.load(file)
        name = data['parameters']['name']
        country = data['response'][0]['team']['country']
        found = data['response'][0]['team']['founded']
        venue = data['response'][0]['venue']['name']
        capacity = data['response'][0]['venue']['capacity']
        city = data['response'][0]['venue']['city']
        team_logo = data['response'][0]['team']['logo']
        venue_image = data['response'][0]['venue']['image']
        print("Name: {}\nCountry: {}\nFound: {}\nVenue: {}\nCity: {}\nCapacity: {}".format(name, country, found, venue, city, capacity))
    os.remove("file1.json")

    def create_image_file(result_file1, link):
        result_file = result_file1
        ImgRequest = requests.get(link)
        with open(result_file, 'wb') as file_handler:
            file_handler.write(ImgRequest.content)
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(result_file)
        if mime_type == 'image/jpeg':
            os.rename(result_file, result_file + '.jpg')
        elif mime_type == 'image/png':
            os.rename(result_file, result_file + '.png')
        elif mime_type == 'image/gif':
            os.rename(result_file, result_file + '.gif')
        elif mime_type == 'image/bmp':
            os.rename(result_file, result_file + '.bmp')
        elif mime_type == 'image/tiff':
            os.rename(result_file, result_file + '.tiff')
        else:
            print('Not an image? %s' % mime_type)

    create_image_file('result_file1.png', team_logo)
    create_image_file('result_file2', venue_image)

    label2 = Label(window, text="Name: {}\n".format(name), fg="Black", bg="White", font="Helvetica 16 normal")
    label2.pack()

    Label(window, text="Team Logo:", font="Helvetica 12 normal").pack()

    canvas1 = Canvas(width=150, height=150, bg='white')
    canvas1.pack()
    image = Image.open(src1)
    photo = ImageTk.PhotoImage(image)
    canvas1.create_image(75, 75, image=photo)

    label3 = Label(window, text="Country: {}\n".format(country), fg="Black", bg="White", font="Helvetica 16 normal")
    label3.pack()

    label4 = Label(window, text="Found: {}\n".format(found), fg="Black", bg="White", font="Helvetica 16 normal")
    label4.pack()

    label5 = Label(window, text="Venue: {}\n".format(venue), fg="Black", bg="White", font="Helvetica 16 normal")
    label5.pack()

    Label(window, text="Venue Image:", font="Helvetica 12 normal").pack()

    canvas2 = Canvas(width=200, height=200, bg='white')
    canvas2.pack()
    image = Image.open(src2)
    photo = ImageTk.PhotoImage(image)
    canvas2.create_image(100, 100, image=photo)

    label6 = Label(window, text="Capacity: {}\n".format(capacity), fg="Black", bg="White", font="Helvetica 16 normal")
    label6.pack()

submit_button = Button(window, text="Get Details", fg="Black", bg="Grey", command=get_details, font="Helvetica 10 normal")
submit_button.pack()

Label(window, text="").pack()

window.mainloop()

os.remove("D:\\Downloads\\Complete-Python-3-Bootcamp-master\\result_file1.png.png")
os.remove("D:\\Downloads\\Complete-Python-3-Bootcamp-master\\result_file2.jpg")