import xml.etree.ElementTree as ET
import re
from collections import Counter
from tkinter import *
import os.path
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk


global textbox
def set_text(text):
    yol_label_text.delete(0,END)
    yol_label_text.insert(0,text)
    return

def prefences():
    filetypes = (
        ('text files', '*.xml'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title="Open a file",
        initialdir="./",
        filetypes=filetypes
    )
    set_text(filename)

def check(text):
    textbox.config(state="normal")
    if len(text) == 0:
        messagebox.showinfo("Hata","Dosya alanı boş")
    if not os.path.isfile(text):
        messagebox.showinfo("Dizin Yanlış", "Girdiğiniz dizinde dosya bulunamadı")
    else:
        control(text)
        textbox.config(state="disabled")
def control(fileName):
    global bool
    print()
    with open(fileName, "r") as reader:
        try:
            data = reader.read()
            tree = ET.fromstring(data)
            bool = False
            textbox.insert("1.0", "Bir problem bulunamadı veya sorunlar çözüldü"+ "\n")
        except NameError as err:
            textbox.insert("1.0",err +"\n")
        except SyntaxError as err:
            e = str(err).split(":")
            if e[0] == "XML or text declaration not at start of entity":
                textbox.insert("1.0","Sorun: XML başlığında hata var" + "\n")
                with open("6-1.xml", "r") as f:
                    data = f.read()
                    arr = data.split("\n")
                    head = "Bulunamadı"
                    order = 0
                    for i in range(len(arr)):
                        try:
                            if arr[i][arr[i].index("<"):arr[i].index("l") + 1] == "<?xml":
                                head = arr[i]
                                order = i
                                break
                        except:
                            print("yok")
                    if head == "Bulunamadı":
                        head = "<?xml version=1.0 ?>"
                        arr[0] = head
                    else:
                        arr[0] = head
                        arr[order] = ""
                    arr = removeSpaces(arr)
                    with open("6-1.xml", "r+") as reader:
                        reader.truncate(0)
                        reader.write(arr)
            elif e[0] == "XML declaration not well-formed" or e[0] == "not well-formed (invalid token)":
                textbox.insert("1.0","Sorun: Bazı xml düzenlemeleri hatalı" + "\n")
                with open("6-1.xml", "r") as f:
                    data = f.read()
                    arr = data.split("\n")
                    arr = removeSpaces(arr)

                    arr = arr.split("\n")
                    arr = addApostroph(arr)
                    arr = arr.split("\n")
                    arr = addSpaces(arr)

                    with open("6-1.xml", "r+") as reader:
                        reader.truncate(0)
                        reader.write(arr)
            elif e[0] == "mismatched tag":
                textbox.insert("1.0","Sorun: Tag hiyerarşisinde sorun var" + "\n")
                with open("6-1.xml", 'r') as reader:
                    data = reader.read()
                    arr = data.split("\n")
                    tags = []
                    closingTags = []
                    controls = []
                    if len(arr):
                        for s in range(len(arr)):
                            ns = re.findall("(?<=<)([^A]*?)(?=>)",arr[s])
                            if len(ns) == 1:
                                if ns[0].split()[0] != "?xml":
                                    if "/" in ns[0].split()[0]:
                                        closingTags.append(ns[0].split()[0])
                                    else:
                                        tags.append(ns[0].split()[0])
                            elif len(ns) == 2:
                                tags.append(ns[0].split()[0])
                                closingTags.append(ns[1])
                        for a,b in zip(Counter(sorted(tags)),Counter(sorted(closingTags))):
                           if Counter(sorted(closingTags))[b] != Counter(sorted(tags))[a] or not Counter(sorted(closingTags))["/"+a]:
                               controls.append(a)
                               bool = False
                        r = ", ".join(controls)
                        textbox.insert("1.0", "Lütfen " + r + " tag'ını kontrol edin" + "\n")
                        reader.close()
            else:
                textbox.insert("1.0", str(e))
        except TypeError as err:
            textbox.insert("1.0",err +"\n")
            bool = False
        except FileExistsError as err:
            textbox.insert("1.0", err +"\n")
            bool = False
        except:
            textbox.insert("1.0","Başka hata var. Program yazılımcısı ile iletişime geçin" +"\n")
            bool = False
    reader.close()
    while (bool):
        control(fileName)
def removeSpaces(arr):
    new = []
    for a in range(len(arr)):
        c = list(set(arr[a].split("\t")))
        if len(c) == 1 and c[0] == "":
            pass
        else:
            new.append(arr[a])
    return "\n".join(new)
def Convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct

def addApostroph(arr):
    new = []
    for i in range(len(arr)):
        s = arr[i].split(" ")
        for str in range(len(arr[i])):
            if arr[i][str] == "=":
                if arr[i][str + 1] != "\"":
                    for o in range(len(s)):
                        if s[o].find("\"") == -1 and s[o].find("=") != -1:
                            s[o] = s[o].split("=")[0] + "=" + "\"" + s[o].split("=")[1] + "\""
        arr[i] = " ".join(s)
    return "\n".join(arr)

def addSpaces(arr):
    for a in range(len(arr)):
        z = arr[a].split(" ")
        for i in range(len(z)):
            if len(z[i].split("\"")) > 3:
                n = z[i].split("\"")
                n = list(filter(None, n))
                for c in range(len(n)):
                    if (c + 1) % 2 == 0:
                        n[c] = n[c - 1] + "\"" + n[c] + "\""
                        n[c - 1] = ""
                n = list(filter(None, n))
                z[i] = " ".join(n)
        arr[a] = " ".join(z)
    return "\n".join(arr)


main_renk = "#add8e6"

bool = True

master = Tk()
root = master
root.title('Xml Kontrol')
canvas = Canvas(master, height=450, width=750)
canvas.pack()

main_frame = Frame(master, bg="#add8e6")
main_frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

yol_label = Label(main_frame, bg=main_renk, text="Yolu giriniz", font="Verdana 12 bold")
yol_label.pack(padx=10,pady=10)

yol_label_text = Entry(main_frame, font="Verdana 8", width=50)
yol_label_text.pack()

button_frame = Frame(main_frame, bg=main_renk)
button_frame.place(relx=0.325, rely=0.2, relwidth=0.15, relheight=0.15)

button_frame2 = Frame(main_frame, bg=main_renk)
button_frame2.place(relx=0.525, rely=0.2, relwidth=0.15, relheight=0.15)

text_frame = Frame(main_frame, bg=main_renk)
text_frame.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.3)

btn_file = ttk.Button(button_frame, text="Dosya seç", command=prefences)
btn_file.pack(expand=True, padx=10, pady=10)

btn_ok = ttk.Button(button_frame2, text="Kontrol et", command=lambda:check(yol_label_text.get()))
btn_ok.pack(expand=True, padx=10, pady=10)

textbox = Text(text_frame, width=100, height=10, yscrollcommand=True, font="Verdana 10")
textbox.pack()
master.mainloop()


# [arr[s].count("\t"), arr[s][arr[s].count("\t") + 1:har], arr[s][arr[s].find(">") + 1:arr[s].find("/") - 1], Convert(list(itertools.chain(*[[a.replace("\"", "") for a in s.split("=")] for s in arr[s][arr[s].find(" "):arr[s].find(">")].split()])))]
