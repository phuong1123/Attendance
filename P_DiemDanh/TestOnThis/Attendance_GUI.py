from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
import os, cv2
import tkinter.font
import string
import shutil
import csv
import time
import datetime
from unidecode import unidecode
import numpy as np
import pandas as pd
from tkcalendar import *
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


_primary = "#0D6AB1"
_white = "#fff"
_yellow = "#FDEB02"
_lightBlue = "#26A1FF"
_gray = "#606060"
_green = "#06D938"
_lightGray = "#D8D8D8"
_button = "#FAA128"
_lightEntry = "#eeeeee"


def raise_frame(frame):
    frame.tkraise()

#xóa/làm mới thông tin mới nhập ở entry
def resetTT():
    txtMaSV.delete(0, 'end')
    txtHoTen.delete(0, 'end')
    txtLop.select_set(0)
    txtNgaySinh.delete(0, 'end')
    lblBuoc1.configure(text = "Bước 1:", fg= _primary)
    lblBuoc2.configure(text = "Bước 2:", fg= _primary)
    lblBuoc3.configure(text = "ĐIỂM DANH", fg= _primary)

# để dữ liệu nhập vào ô nhập tên là viết thường
def getName():
    name = txtHoTen.get()
    translator = str.maketrans('', '', string.punctuation)
    name = name.translate(translator)
    name = unidecode(name)
    name = name.replace(" ", ".")
    return name

#kiểm tra xem kiểu dữ liệu nhập vào có phải số không
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

#lấy hình ảnhs
def TakeImmages():
    index = txtLop.curselection()[0]
    Id = (txtMaSV.get())
    name = getName()
    lop =  dataLop[index][1]
    dob = (txtNgaySinh.get_date())

    if(Id == ""):
        s = "Nhập Mã sinh viên"
        lblBuoc1.configure(text=s, fg=_button)
    
    else:
        if(is_number(Id) and name.isalpha()):
            cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            harcascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for(x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum+1
                    filenameAut = "TrainingImages/"+ name + "." + Id + '.' + str(sampleNum) + ".png"
                    cv2.imwrite(filenameAut , gray[y:y+h, x:x+w])
                    cv2.imshow('Get Image data train', img)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif sampleNum > 60:
                    break
            cam.release()
            cv2.destroyAllWindows()
            res = "Đã lưu: "+ Id + " - " + name
            row = [Id, name, dob, lop]
            with open('StudentDetails/studentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            lblBuoc1.configure(text=res, fg=_green)            
            csvFile.close()
        else:        
            if(is_number(Id)):
                res = "Nhập tên"
                lblBuoc1.configure(text=res, fg=_button)
            if(name.isalpha()):
                res = "Nhập mã sinh viên"
                lblBuoc1.configure(text=res, fg=_button)


def TrainImages():
    # Path for face image database   
    path = "TrainingImages/"
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    # function to get the images and label data    
    print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
    faces,ids = getImagesAndLabels(detector, path)
    recognizer.train(faces, np.array(ids))
    # Save the model into trainer/trainer.yml
    recognizer.write('TrainingImageLabel/Trainner.yml') 
    # Print the numer of faces trained and end program
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
    # res = "Image Trainned"+",".join(str(f) for f in ids)
    res = "Xử lý dữ liệu thành công"
    lblBuoc2.configure(text=res, fg = _green)



def getImagesAndLabels(detector, path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
        faceSamples=[]
        ids = []
        for imagePath in imagePaths:
            PIL_image = Image.open(imagePath)
            PIL_img= PIL_image.convert('L') 
            img_numpy = np.array(PIL_img,'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
        return faceSamples,ids



def acceptAttendance():
    indexOption = txtOption.curselection()[0]
    res = dataLop[indexOption][1]
    resOption = "Bạn có xác nhận điểm danh lớp " + res + " không?"
    messageboxOption = messagebox.askquestion("Xác nhận", resOption)
    if messageboxOption == 'yes':
        TrackImages()
    else:
        raise_frame(f1)


def  returnTenLop():
    indexOption = txtOption.curselection()[0]
    res = dataLop[indexOption][1]
    return res


def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create() 
    recognizer.read("TrainingImageLabel"+os.sep+"Trainner.yml")
    harcascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("StudentDetails"+os.sep+"studentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    ##
    col_info = ['Id', 'Name', 'Dob', 'Lop']
    info = pd.DataFrame(columns=col_info)

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)


        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

            if(conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values[0]
                tt = str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                ###
                infoName = df.loc[df['Id'] == Id]['Name'].values[0]
                inforLop = df.loc[df['Id'] == Id]['Lop'].values[0]
                inforDob = df.loc[df['Id'] == Id]['Dob'].values[0]
                info.loc[len(attendance)] = [Id, infoName, inforDob, inforLop]
                   
                resInfor = "Sinh viên: " + infoName + "\n MSSV: " + str(Id) + "\n Lớp: " + inforLop
                lblMessage.configure(text = resInfor)


            else:
                Id = 'Unknown'
                resInfor = "Sinh viên: " + str(Id) + "\n MSSV: " + str(Id) + "\n Lớp: " + str(Id)
                lblMessage.configure(text = resInfor)             
                res= "ĐIỂM DANH KHÔNG THÀNH CÔNG"
                lblThongBao.configure(text = res, fg= _button)  
                tt = str(Id)
                if(conf > 75):
                    noOfFile = len(os.listdir("ImagesUnknown"))+1
                    cv2.imwrite("ImagesUnknown"+os.sep+"Image"+str(noOfFile) +
                                ".png", im[y:y+h, x:x+w])

            cv2.putText(im, str(tt), (x, y+h), font, 1, (255, 255, 255), 2)

        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        info = info.drop_duplicates(subset=['Id'], keep='first')


        cv2.imshow('Diem danh', im)
        if (cv2.waitKey(1) == ord('q')):
            break
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")

        fileName = "Attendance"+os.sep+returnTenLop()+"_"+date+"_"+Hour+".csv"
        attendance.to_csv(fileName, index=False)
        res= "ĐIỂM DANH THÀNH CÔNG"
        lblThongBao.configure(text = res, fg = _green)
 
    cam.release()
    cv2.destroyAllWindows() 
    resTime = Hour + ":" + Minute + ", " + date
    lblSetThoiGian.configure(text = resTime)
    raise_frame(f3)


#chuyển sang màn thêm sinh thông tin sv
def naviThemTT():
    raise_frame(f2)

#chuyển sang màn điểm sanh
def naviDiemDanh():
    raise_frame(f3)


def updateImg():
    fileUnkonwn = "hoa.png"
    imgUnknown = PhotoImage(file=fileUnkonwn)
    imgImage.itemconfig(imgOnCanvas, image=imgUnknown)

################################################################################################
################################################################################################
################################################################################################

root = tk.Tk()
root.title('Nhận diện khuôn mặt')
root.geometry('1280x720')
root.configure(background="#0D6AB1")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)

f1.configure(background=_primary)
f2.configure(background=_primary)
f3.configure(background=_primary)
f4.configure(background=_primary)

for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')




################################################################################################
################################################################################################
################################################################################################
############################################# F1: trang chủ

lblTitle = Label(f1, text='Hệ thống điểm danh bằng nhận diện khuôn mặt', font=(
    "Segoe UI", 30, "bold"), bg=_primary, fg=_yellow).pack(padx=170, pady=70)


btnDiemDanh = Button(f1, bg = _white, width  = 217 , height = 217, command=lambda:raise_frame(f4))
btnDiemDanh.place(x=387, y=230)
miDiemDanh = PhotoImage(file = "btn_diem_danh.png")
tmiDiemDanh = miDiemDanh.subsample(1,1)
btnDiemDanh.config(image = tmiDiemDanh, compound = RIGHT)


btnThemTT = Button(f1, bg=_white, width=217, height=217, command=lambda:raise_frame(f2))
btnThemTT.place(x=677, y=230)
miThemTT = PhotoImage(file="btn_them_tt.png")
tmiThemTT = miThemTT.subsample(1,1)
btnThemTT.config(image = tmiThemTT, compound = RIGHT)


################################################################################################
################################################################################################
################################################################################################
############################################### F2: Thêm thông tin sinh viên



lblTitle = Label(f2, text='Hệ thống điểm danh bằng nhận diện khuôn mặt', font=(
                "Segoe UI", 30, "bold"), bg=_primary, fg=_yellow).place(x=170, y=46)


lblBackground = Label(f2, text="", bg=_white, width=168,
                      height=36).place(x=52, y=127)


lblSubTitle = Label(f2, text="THÊM THÔNG TIN SINH VIÊN", font=(
                "Segoe UI", 15, "bold"), fg=_primary, bg=_white).place(x=115, y=195)



lblMaSV = Label(f2, text="Mã sinh viên", font=("Segoe UI", 15), 
                fg=_gray, bg=_white).place(x=115, y=287)
txtMaSV = tk.Entry(f2, width=40, font=("Segoe UI", 15),relief =SUNKEN, bg = _lightEntry)
txtMaSV.place(x=300, y=287)


lblHoTen = Label(f2, text="Họ và tên", font=("Segoe UI", 15),
                 fg=_gray, bg=_white).place(x=115, y=358)
txtHoTen = Entry(f2, width=40, font=("Segoe UI", 15),relief =SUNKEN, bg = _lightEntry)
txtHoTen.place(x=300, y=358)


lblNgaySinh = Label(f2, text="Ngày sinh", font=(
                "Segoe UI", 15), fg=_gray, bg=_white).place(x=115, y=438)
txtNgaySinh = DateEntry(f2, width=38, font=("Segoe UI", 15),relief =SUNKEN, bg = _lightEntry)
txtNgaySinh.place(x=300, y=438)


lblLop = Label(f2, text="Lớp", font=("Segoe UI", 15),
                fg=_gray, bg=_white).place(x=115, y=518)
# txtLop = Entry(f2, width=40, font=("Segoe UI", 15),relief =SUNKEN, bg = _lightEntry)
# txtLop.place(x=300, y=518)

filePathLop = 'ListClass/listClass.csv'
fileLop = open(filePathLop)
readerLop = csv.reader(fileLop)
dataLop = list(readerLop)
del(dataLop[0])

list_lop= []
for x in list(range(0, len(dataLop))):
    list_lop.append(dataLop[x][1])
    
txtLop = Listbox(f2, width = 30, height = 5, font=("Segoe UI", 12))
for x, y in enumerate(list_lop):
    txtLop.insert(x,y)
    txtLop.select_set(0)
txtLop.place(x=300, y = 518)

################################################################################################
btnReset = tk.Button(f2, text="Reset thông tin", bg=_white, relief = FLAT,
                 fg=_primary, font=("Segoe UI", 12), command = resetTT).place(x=620, y=510)


lblBuoc1 = Label(f2, text="Bước 1: ", font=(
                "Segoe UI", 12), bg=_white, fg=_primary)
lblBuoc1.place(x=809, y=256)
btnLayHinhAnh = Button(f2, text="Lấy hình ảnh", fg=_white,  relief=FLAT,font=(
                "Segoe UI", 15), bg=_button, width=30, command = TakeImmages).place(x=809, y=284)


lblBuoc2 = Label(f2, text="Bước 2: ", font=(
                "Segoe UI", 12), bg=_white, fg=_primary)
lblBuoc2.place(x=809, y=352)


btnXuLyHinhAnh = Button(f2, text="Xử lý hình ảnh", fg=_white,  relief=FLAT,font=(
                "Segoe UI", 15), bg=_button, width=30, command = TrainImages).place(x=809, y=380)


lblBuoc3 = Label(f2, text="ĐIỂM DANH", font=(
                "Segoe UI", 12), bg=_white, fg=_primary)
lblBuoc3.place(x=809, y=448)
btnLuuHinhAnh = Button(f2, text="Test", fg=_white,  relief=FLAT,font=(
                "Segoe UI", 15), bg=_button, width=30, command = TrackImages).place(x=809, y=476)


btnHuy = Button(f2, text="Trở lại", fg=_primary, bg=_white, relief=FLAT,
                 font=("Segoe UI", 15), command = lambda:raise_frame(f1)).place(x=1080, y=598)


################################################################################################
################################################################################################
################################################################################################
###################################### F3: Hiển thị thông tin sau khi quét camera
lblTitle = Label(f3, text='Hệ thống điểm danh bằng nhận diện khuôn mặt', font=(
                "Segoe UI", 30, "bold"), bg=_primary, fg=_yellow).place(x=170, y=46)


lblBackground = Label(f3, text="", bg=_white, width=168,
                                            height=36).place(x=52, y=127)


lblSubTitle = Label(f3, text="ĐIỂM DANH SINH VIÊN", font=(
                        "Segoe UI", 15, "bold"), fg=_primary, bg=_white).place(x=115, y=195)


imgImage = Canvas(f3, bg=_white, width=245, height=245)
imgImage.place(x=319, y=270)
fileName = "unknown3.png"
imgSample = PhotoImage(file=fileName)
imgOnCanvas = imgImage.create_image(125, 125, anchor=CENTER, image=imgSample)


lblThongBao = Label(f3, text="ĐIỂM DANH THÀNH CÔNG", fg=_green, bg=_white, font=("Segoe UI", 15, "bold"))
lblThongBao.place(x=638, y=278)

lblMessage = Label(f3, text = "Sinh viên: Nguyễn Thị Thu Phương \n MSSV: 1151020028 \n Lớp: CNTT11-01",relief=SUNKEN,
                             font=("Segoe UI", 15, "bold"), fg= _gray,bg = _white,height = 4, width= 30)
lblMessage.place(x=638, y = 320)

lblThoiGian = Label(f3, text="Thời gian check in:", font=("Segoe UI", 15, "bold"), 
                                fg= _gray,bg = _white, height = 1)
lblThoiGian.place(x= 638, y = 440)

lblSetThoiGian = Label(f3, text = "14:00, 28/10/2020", fg=_primary, bg = _white, font=("Segoe UI", 15, "bold"))
lblSetThoiGian.place(x=638, y=474)


btnLuu = Button(f3, text="ĐIỂM DANH", fg=_white, bg=_lightBlue, 
                font=("Segoe UI", 15), width=10, command = lambda:raise_frame(f4)).place(x=1080, y=598)

btnHuy = Button(f3, text="Trở lại trang chủ", fg=_primary, bg=_white, relief=FLAT,
                font=("Segoe UI", 15), command = lambda:raise_frame(f1)).place(x=915, y=598)



################################################################################################
################################################################################################
################################################################################################
###################################### F4: First Option
lblTitle = Label(f4, text='Hệ thống điểm danh bằng nhận diện khuôn mặt', font=(
                "Segoe UI", 30, "bold"), bg=_primary, fg=_yellow).place(x=170, y=46)


lblBackground = Label(f4, text="", bg=_white, width=168,
                                            height=36).place(x=52, y=127)


lblSubTitle = Label(f4, text="Lựa chọn lớp: ", font=(
                        "Segoe UI", 15), bg=_white).place(x=115, y=195)


txtOption = Listbox(f4, width = 40, height = 6, font = ("Segoe UI", 12))
for x, y in enumerate(list_lop):
    txtOption.insert(x,y)
    txtOption.select_set(0)
txtOption.place(x = 300, y = 195)


btnSelect = Button(f4, text = "Xác nhận", bg = _primary, fg = _white, width = 20,
                 font = ("Segoe UI", 12), command= lambda: acceptAttendance())
btnSelect.place(x = 750, y = 195)

btnBackToHome = Button(f4, text="Hủy", fg=_primary, bg=_white, relief=FLAT,
                font=("Segoe UI", 15), command = lambda:raise_frame(f1))
btnBackToHome.place(x=915, y=598)




################################################################################################
################################################################################################
################################################################################################
raise_frame(f1)
root.mainloop()


