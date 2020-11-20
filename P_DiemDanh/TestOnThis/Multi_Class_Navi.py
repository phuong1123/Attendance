import tkinter as tk
import csv

_primary = "#0D6AB1"
_white = "#fff"
_yellow = "#FDEB02"
_lightBlue = "#26A1FF"
_gray = "#606060"
_green = "#06D938"
_lightGray = "#D8D8D8"
_button = "#FAA128"
_lightEntry = "#eeeeee"

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Home)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class Home(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        filePath = 'ListClass/listClass.csv'
        File = open(filePath)
        Reader = csv.reader(File)
        Data = list(Reader)
        del(Data[0])

        list_of_entries = []
        for x in list(range(0, len(Data))):
            list_of_entries.append(Data[x][1])

        # print(list_of_entries)
        listbox = tk.Listbox(self)
        for x, y in enumerate(list_of_entries):
            listbox.insert(x,y)
            listbox.select_set(0)
        listbox.pack()

        def update():
            index = listbox.curselection()[0]
            ok = Data[index][1]
            txtTest.configure(text = ok)
            return None


        
        btn03 = tk.Button(self, text="Lấy Tên lớp từ listbox",
                    command=lambda: update()).pack()
        btn01 = tk.Button(self, text="Thêm thông tin",
                    command=lambda: master.switch_frame(ThemTT)).pack()
        btn02 = tk.Button(self, text="Điểm danh",
                    command=lambda: master.switch_frame(DiemDanh)).pack()

        txtTest = tk.Label(self, text = "Kết quả hiển thị ở đây")
        txtTest.pack()

class ThemTT(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        lblTitle = tk.Label(self, text='Hệ thống điểm danh bằng nhận diện khuôn mặt', font=(
                    "Segoe UI", 30, "bold"), bg=_primary, fg=_yellow).pack(padx=170, pady=70)

        lblBackground = tk.Label(self, text="", bg=_white, width=168, height=36).place(x=52, y=127)

        lblSubTitle = tk.Label(self, text="THÊM THÔNG TIN SINH VIÊN", font=(
                    "Segoe UI", 15, "bold"), fg=_primary, bg=_white).place(x=115, y=195)
              
        lblMaSV = tk.Label(self, text="Mã sinh viên", font=("Segoe UI", 15), 
                        fg=_gray, bg=_white).pack()
        txtMaSV = tk.Entry(self, width=40, font=("Segoe UI", 15),bg = _lightEntry)
        txtMaSV.pack()

        lblLop = tk.Label(self, text="Lớp", font=("Segoe UI", 15),
                        fg=_gray, bg=_white).pack()
        txtLop = tk.Entry(self, width=40, font=("Segoe UI", 15),bg = _lightEntry).pack()

        lblHoTen = tk.Label(self, text="Họ và tên", font=("Segoe UI", 15),
                        fg=_gray, bg=_white).pack()
        txtHoTen = tk.Entry(self, width=40, font=("Segoe UI", 15),bg = _lightEntry).pack()

        lblNgaySinh = tk.Label(self, text="Ngày sinh", font=(
                        "Segoe UI", 15), fg=_gray, bg=_white).pack()
        txtNgaySinh = tk.Entry(self, width=40, font=("Segoe UI", 15), bg = _lightEntry).pack()
     
        btnReset = tk.Button(self, text="Reset thông tin", bg=_white, 
                        fg=_primary, font=("Segoe UI", 12), command = lambda: resetTT()).pack()


        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(Home)).pack()

        def resetTT():
            txtMaSV.delete(0, 'end')


class DiemDanh(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page two").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(Home)).pack()

if __name__ == "__main__":
    app = SampleApp()
    app.geometry("600x400")
    app.mainloop()