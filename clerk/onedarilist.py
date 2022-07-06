from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from functools import partial
import time
import threading
import pickle
import socket
from comutil import ComUnit
from menu import Menu




#orderNumList = [100, 200, 300, 400, 500]
#orderNumToonedariNum = {100:1, 200:2, 300:3, 400:4, 500:5}
orderNumList = []
orderNumToonedariNum = {}
orderNumToContent = []
menuIdDic = {0:["karaage", 500], 1:["edamame", 300], 2:["beer", 200]}
menu = Menu()

#注文を提供したらオーダーリストから消してリストを更新
def clear_order(orderNum) :
    if orderNum not in orderNumList :
        return
    nextList = []
    selected = tree.get_children()
    for i in selected :
        nextList.append(tree.item(i, 'values'))
    for i in selected :
        tree.delete(i)
    
    index = 0
    for i in range(len(nextList)) :
        if int(nextList[i][0]) == orderNumToonedariNum[orderNum] :
            orderNumList.pop(orderNumList.index(orderNum))
            continue

        index += 1
        tree.insert(parent='', index='end', iid=i, values=(i, nextList[i][1], nextList[i][2], nextList[i][3], nextList[i][4]))
    
    orderNumToonedariNum.clear()
    for i in range(len(orderNumList)) :
        orderNumToonedariNum[orderNumList[i]] = i + 1
    


#注文が届いたら新たに行を追加
def catch_order(tree, orderNum,iid, zaseki, name, num, cost) :
    onedariNum = len(orderNumList)+1
    orderNumList.append(orderNum)
    tree.insert(parent='', index='end', iid=iid, values=(onedariNum, zaseki,name, num, cost))
    orderNumToonedariNum[orderNum] = onedariNum

def Create_onedariList() :
    #列の識別名を指定
    column = ("orderNum", "zaseki", "Name", "num", "cost")
    #メインウインドウの生成
    root = tk.Tk()
    root.title("おねだりリスト")
    root.geometry('600x300')

    #Treeviewの生成
    tree1 = ttk.Treeview(root, columns = column)

    #列の設定
    tree1.column("#0", width=0, stretch="no")
    tree1.column('orderNum', anchor='center', width=80)
    tree1.column('zaseki', anchor='center', width=80)
    tree1.column('Name',anchor='center', width=100)
    tree1.column('num', anchor='center', width=80)
    tree1.column('cost', anchor='center', width=80)
    # 列の見出し設定
    tree1.heading('#0',text='')
    tree1.heading('orderNum', text='注文番号',anchor='center')
    tree1.heading('zaseki', text='座席番号',anchor='center')
    tree1.heading('Name', text='商品名', anchor='center')
    tree1.heading('num', text='個数',anchor='center')
    tree1.heading('cost',text='価格', anchor='center')
    # レコードの追加
    """
    tree1.insert(parent='', index='end', iid=0 ,values=(1, 1, 'ビール', 1, 400))
    tree1.insert(parent='', index='end', iid=1 ,values=(2, 2,'からあげ', 2, 350))
    tree1.insert(parent='', index='end', iid=2, values=(3, 3,'枝豆', 1, 300))
    tree1.insert(parent='', index='end', iid=3, values=(4, 1,'からあげ', 2, 350))
    tree1.insert(parent='', index='end', iid=4, values=(5, 3,'ビール', 3, 400))

    # Buttonの生成
    button_subWindow = Button(root, text='catch_order', command=sub_window)
    button = Button(root, text='Increment Price', command=partial(clear_order, 300 ))
    button_catchOrder = Button(root, text='catch_order', command=sub_window)
    #button_changeWindow = Button(root, text='catch_window', command=change_window)
"""

    # Styleの設定
    style = ttk.Style()
    style.theme_use("default")
    style.map("Treeview")
    # ウィジェットの配置
    #notebook.pack(expand=True, fill="both", padx=10, pady=10)
    tree1.pack(pady=10)
    #tree2.pack(pady=10)
    global tree
    tree = tree1

    #button_subWindow.pack()
    #button.pack()
    #button_catchOrder.pack()

    root.mainloop()


#button_changeWindow.pack()
tree = ""
#おねだりリスト表示用スレッド
thread1 = threading.Thread(target=Create_onedariList)
#スタッフ用表示用スレッド
#thread1 = threading.Thread(target=Create_orderList)
thread1.start()

time.sleep(10)

tree.focus_set()


#注文を受信したらオーダーリストに追加
#catch_order(tree, 6, 1, "bi-ru", 2, 300)

class Client():
    def __init__(self, ip, tree):
        self.CLIENTIP = ip
        self.SERVERIP = '192.168.0.3'
        self.PORT = 334
        self.BUFFER_SIZE = 1024
        self.orderId = 0
        self.tree = tree
        self.iid = 5

    def prepareSocket(self):
        sock = socket.socket(socket.AF_INET)
        sock.connect((self.SERVERIP, self.PORT))
        self.sock = sock

    # データ受信関数
    def recvData(self):
        while True:
            try:
                data = self.sock.recv(self.BUFFER_SIZE)
                if data == b"":
                    break
                content = pickle.loads(data)
                print(f'new order({content.key}):', 'menu:', content.menuId, 'num:', content.num, 'mode', content.mode)
                print(type(content.mode))
                
                #おねだりリストに追加
                if int(content.mode) == 3 :
                    print("mode3")
                    catch_order(self.tree, content.orderId, self.iid, content.sender, menuIdDic[int(content.menuId)][0], content.num, menuIdDic[int(content.menuId)][1])
                    self.iid += 1
                    orderNumToContent.append(content)
                elif int(content.mode) == 1 :
                    #注文が受理された旨をスタッフ、客に通知
                    content_onedari = orderNumToContent[content.menuId-1]
                    orderNumToContent.pop(content.menuId-1)
                    #おねだりリストを更新
                    clear_order(content_onedari.orderId)
                    #客に対して送信
                    msg = ComUnit(4,content_onedari.sender, content_onedari.menuId, content_onedari.num)
                    self.send(msg, content.sender)
                    #スタッフに対して送信
                    msg = ComUnit(4,"192.168.0.5", content.menuId, content.num)
                    self.send(msg)

            except ConnectionResetError:
                break

        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        
    def run(self):
        # ?f?[?^??M???T?u?X???b?h????s
        thread = threading.Thread(target=self.recvData)
        thread.start()

    def send(self, unit, sender=None):
        # ?f?[?^?????[?v
        try:
            if sender is None:
                unit.sender = self.CLIENTIP
            else:
                unit.sender = sender
            unit.key = self.orderId
            self.sock.send(pickle.dumps(unit))
            self.orderId += 1
        except ConnectionResetError:
            pass

    def disconnect(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

ip = "192.168.0.1"
client = Client(ip, tree)
client.prepareSocket()
client.run()

