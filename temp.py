### インポート
import tkinter

from numpy.core.fromnumeric import var

### メイン画面作成
main = tkinter.Tk()

### 画面サイズ設定
main.geometry("640x400")

### メニューバー作成
menubar = tkinter.Menu(master=main)

### ファイルメニュー作成
filemenu = tkinter.Menu(master=menubar, tearoff=0)
filemenu.add_command(label="開く")
filemenu.add_command(label="閉じる")
filemenu.add_separator()
filemenu.add_command(label="終了", command=main.quit)

### 編集メニュー作成
editmenu = tkinter.Menu(master=menubar, tearoff=0)
editmenu.add_command(label="切り取り")
editmenu.add_command(label="コピー")
editmenu.add_command(label="貼り付け")
editmenu.add_separator()

### 設定メニュー作成
setmenu = tkinter.Menu(master=menubar, tearoff=0)
setmenu.add_checkbutton(label="チェックボタン１")
setmenu.add_checkbutton(label="チェックボタン２")
setmenu.add_checkbutton(label="チェックボタン３")
setmenu.add_separator()
action = tkinter.IntVar()
action.set(1)
setmenu.add_radiobutton(label="ラジオボタン１", variable=action, value=0)
setmenu.add_radiobutton(label="ラジオボタン２", variable=action, value=1)

### 各メニューを設定
menubar.add_cascade(label="ファイル", menu=filemenu)
menubar.add_cascade(label="編集", menu=editmenu)
editmenu.add_cascade(label="設定", menu=setmenu)

### メニューバー配置
main.config(menu=menubar)

### イベントループ
main.mainloop()
