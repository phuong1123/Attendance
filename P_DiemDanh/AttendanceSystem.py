import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
from tkinter import filedialog
import os, cv2
import tkinter.font
import string
import shutil
from unidecode import unidecode
import numpy as np
import pandas as pd

from tkinter import *

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




root = tk.Tk()
root.title('Nhận diện khuôn mặt')
root.geometry('1280x720')
root.configure(background="#0D6AB1")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)

f1.configure(background=_primary)
f2.configure(background=_primary)
f3.configure(background=_primary)

for frame in (f1, f2, f3):
    frame.grid(row=0, column=0, sticky='news')


############################################# F1
lblTitle = Label(f1, text='Hệ thống điểm danh bằng nhận diện khuôn mặt', font=(
    "Segoe UI", 30, "bold"), bg=_primary, fg=_yellow).pack(padx=170, pady=70)


btnDiemDanh = Canvas(f1, bg=_white, width=217, height=217)
btnDiemDanh.place(x=387, y=230)
imgDiemDanh = PhotoImage(file="btn_diem_danh.png")
btnDiemDanh.create_image(110, 110, anchor=CENTER, image=imgDiemDanh)


btnThemTT = Canvas(f1, bg=_white, width=217, height=217)
btnThemTT.place(x=677, y=230)
imgThemTT = PhotoImage(file="btn_them_tt.png")
btnThemTT.create_image(110, 110, anchor=CENTER, image=imgThemTT)


############################################### F2: Thêm thông tin sinh viên



lblTitle = Label(f2, text='Hệ thống điểm danh bằng nhận diện khuôn mặt', font=(
    "Segoe UI", 30, "bold"), bg=_primary, fg=_yellow).place(x=170, y=46)

lblBackground = Label(f2, text="", bg=_white, width=168,
                      height=36).place(x=52, y=127)

lblSubTitle = Label(f2, text="THÊM THÔNG TIN SINH VIÊN", font=(
    "Segoe UI", 15, "bold"), fg=_primary, bg=_white).place(x=115, y=195)



lblMaSV = Label(f2, text="Mã sinh viên", font=("Segoe UI", 15), 
                fg=_gray, bg=_white).place(x=115, y=287)
txtMaSV = tk.Entry(f2, width=40, font=("Segoe UI", 15),relief =SUNKEN, bg = _lightEntry).place(x=300, y=287)

lblLop = Label(f2, text="Lớp", font=("Segoe UI", 15),
                fg=_gray, bg=_white).place(x=115, y=358)
txtLop = Entry(f2, width=40, font=("Segoe UI", 15),relief =SUNKEN, bg = _lightEntry).place(x=300, y=358)

lblHoTen = Label(f2, text="Họ và tên", font=("Segoe UI", 15),
                 fg=_gray, bg=_white).place(x=115, y=438)
txtHoTen = Entry(f2, width=40, font=("Segoe UI", 15),relief =SUNKEN, bg = _lightEntry).place(x=300, y=438)

lblNgaySinh = Label(f2, text="Ngày sinh", font=(
                "Segoe UI", 15), fg=_gray, bg=_white).place(x=115, y=518)
txtNgaySinh = Entry(f2, width=40, font=("Segoe UI", 15),relief =SUNKEN, bg = _lightEntry).place(x=300, y=518)

def resetTT(f2):
    tkinter.messagebox.showinfo(title=None, message=None, **option)

btnReset = tk.Button(f2, text="Reset thông tin", bg=_white, relief = FLAT,
                 fg=_primary, font=("Segoe UI", 12), command = f2.resetTT).place(x=300, y=555)


lblBuoc1 = Label(f2, text="Bước 1: ", font=(
                "Segoe UI", 12), bg=_white, fg=_primary).place(x=809, y=256)
btnLayHinhAnh = Button(f2, text="Lấy hình ảnh", fg=_white,  relief=FLAT,font=(
                "Segoe UI", 15), bg=_button, width=30, command = "").place(x=809, y=284)

lblBuoc2 = Label(f2, text="Bước 2: ", font=(
                "Segoe UI", 12), bg=_white, fg=_primary).place(x=809, y=352)
btnXuLyHinhAnh = Button(f2, text="Xử lý hình ảnh", fg=_white,  relief=FLAT,font=(
                "Segoe UI", 15), bg=_button, width=30, command = "").place(x=809, y=380)

lblBuoc3 = Label(f2, text="Bước 3: ", font=(
                "Segoe UI", 12), bg=_white, fg=_primary).place(x=809, y=448)
btnLuuHinhAnh = Button(f2, text="Lưu dữ liệu hình ảnh", fg=_white,  relief=FLAT,font=(
                "Segoe UI", 15), bg=_button, width=30, command = "").place(x=809, y=476)


btnLuu = Button(f2, text="LƯU", fg=_white, bg=_lightBlue,
                font=("Segoe UI", 15), width=10, command = "").place(x=1080, y=598)
btnHuy = Button(f2, text="Hủy thao tác", fg=_primary, bg=_white, relief=FLAT,
                font=("Segoe UI", 15), command = lambda: raise_frame(f1)).place(x=915, y=598)



###################################### F3: Hiển thị thông tin sau khi quét camera
lblTitle = Label(f3, text='Hệ thống điểm danh bằng nhận diện khuôn mặt', font=(
                "Segoe UI", 30, "bold"), bg=_primary, fg=_yellow).place(x=170, y=46)


lblBackground = Label(f3, text="", bg=_white, width=168,
                                            height=36).place(x=52, y=127)


lblSubTitle = Label(f3, text="ĐIỂM DANH SINH VIÊN", font=(
                        "Segoe UI", 15, "bold"), fg=_primary, bg=_white).place(x=115, y=195)

# lblRectangel = Label(f3, bg = _lightGray, width = 40, height = 18).place(x=319, y = 270)
imgImage = Canvas(f3, bg=_white, width=245, height=245)
imgImage.place(x=319, y=270)
fileImgName = "hoa.png"
imgSample = PhotoImage(file=fileImgName)
imgImage.create_image(125, 125, anchor=CENTER, image=imgSample)


lblThongBao = Label(f3, text="ĐIỂM DANH THÀNH CÔNG", fg=_green, bg=_white, font=("Segoe UI", 15, "bold")).place(x=638, y=278)

lblMessage = Label(f3, text = "Sinh viên: Nguyễn Thị Thu Phương \n MSSV: 1151020028 \n Lớp: CNTT11-01",relief=SUNKEN,
                             font=("Segoe UI", 15, "bold"), fg= _gray,bg = _white,height = 4, width= 30).place(x=638, y = 320)

lblThoiGian = Label(f3, text="Thời gian check in:", font=("Segoe UI", 15, "bold"), 
                                fg= _gray,bg = _white, height = 1).place(x= 638, y = 440)

lblSetThoiGian = Label(f3, text = "14:00, 28/10/2020", fg=_primary, bg = _white, font=("Segoe UI", 15, "bold")).place(x=638, y=474)


btnLuu = Button(f3, text="ĐIỂM DANH", fg=_white, bg=_lightBlue, 
                font=("Segoe UI", 15), width=10, command = "").place(x=1080, y=598)

btnHuy = Button(f3, text="Trở lại trang chủ", fg=_primary, bg=_white, relief=FLAT,
                font=("Segoe UI", 15), command = lambda: raise_frame(f1)).place(x=915, y=598)


raise_frame(f2)
root.mainloop()


