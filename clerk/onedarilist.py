from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from functools import partial
import time
import threading
import pickle
import socket
import os
import sys
sys.path.append(os.pardir)
from comutil import ComUnit
from srvclt import Client
from menu import Menu

orderNumList = []
orderNumToonedariNum = {}
orderNumToContent = []
menu = Menu()
price = [int(i) for i in menu.price]
menuIdDict = list(zip(menu.name,price))
ipToseatNum = {"192.168.0.2":1, "192.168.0.4":2, "192.168.0.6":3}
menu = Menu()
iid = 5

#注文を提供したらオーダーリストから消してリストを更新
def clear_order(orderNum) :
    if orderNum not in orderNumList :
        return
    nextList = []
    selected = tree.get_children()
    for i in selected :
        t = tree.item(i, 'values')
        nextList.append(t)
        print(t)
        print("aaa"+t[1])
    for i in selected :
        tree.delete(i)
    
    ii = 1
    for i, nl in enumerate(nextList) :
        if int(nl[0]) == orderNumToonedariNum[orderNum] :
            orderNumList.pop(orderNumList.index(orderNum))
            continue

        
        tree.insert(parent='', index='end', iid=i, values=(ii, nl[1], nl[2], nl[3], nl[4]))
        ii += 1
    
    orderNumToonedariNum.clear()
    for i, val in enumerate(orderNumList) :
        orderNumToonedariNum[val] = i + 1
        
    return 
    


#注文が届いたら新たに行を追加
def catch_order(tree, orderNum,iid, zaseki, name, num, cost) :
    onedariNum = len(orderNumList)+1
    orderNumList.append(orderNum)
    tree.insert(parent='', index='end', iid=iid, values=(onedariNum, zaseki,name, num, cost*num))
    orderNumToonedariNum[orderNum] = onedariNum

def inverse_lookup(d, x) :
    for k, v in d.items() :
        if x == v :
            return k
        
def checkOut(content) :
    nextList = []
    selected = tree.get_children()
    for i in selected :
        nextList.append(tree.item(i, 'values'))
        
    for i in selected :
        tree.delete(i)
    ii = 1
    orderNumList_tmp = []
    global orderNumList
    for i, nl in enumerate(nextList) :
        if int(nl[1]) == ipToseatNum[content.sender] :
            #orderNumList.pop(orderNumList[int(nl[0])-1])
            continue

        orderNumList_tmp.append(orderNumList[int(nl[0])-1])
        tree.insert(parent='', index='end', iid=i, values=(ii, nl[1], nl[2], nl[3], nl[4]))
        ii += 1
    
    
    orderNumList = orderNumList_tmp
    orderNumToonedariNum.clear()
    for i, val in enumerate(orderNumList) :
        orderNumToonedariNum[val] = i + 1
        
    return 
    

def Create_onedariList() :
    #列の識別名を指定
    column = ("orderNum", "zaseki", "Name", "num", "cost")
    #メインウインドウの生成
    root = tk.Tk()
    root.title("おねだりリスト")
    root.geometry('600x300')

    #Treeviewの生成
    tree1 = ttk.Treeview(root, columns = column, height = 600)

    #列の設定
    tree1.column("#0", width=0, stretch="no")
    tree1.column('orderNum', anchor='center', width=200)
    tree1.column('zaseki', anchor='center', width=200)
    tree1.column('Name',anchor='center', width=200)
    tree1.column('num', anchor='center', width=200)
    tree1.column('cost', anchor='center', width=200)
    # 列の見出し設定
    tree1.heading('#0',text='')
    tree1.heading('orderNum', text='注文番号',anchor='center')
    tree1.heading('zaseki', text='座席番号',anchor='center')
    tree1.heading('Name', text='商品名', anchor='center')
    tree1.heading('num', text='個数',anchor='center')
    tree1.heading('cost',text='価格', anchor='center')

    # Styleの設定
    style = ttk.Style()
    style.theme_use("default")
    style.map("Treeview")
    # ウィジェットの配置
    tree1.pack(pady=10)
    global tree
    tree = tree1

    root.mainloop()


tree = ""
#おねだりリスト表示用スレッド
thread1 = threading.Thread(target=Create_onedariList)
#スタッフ用表示用スレッド
#thread1 = threading.Thread(target=Create_orderList)
thread1.start()

time.sleep(10)

tree.focus_set()

def recvMethod(content) :
    #おねだりリストに追加
    if int(content.mode) == 3 :
        print("mode3")
        global iid
        catch_order(tree, content.orderId, iid, ipToseatNum[content.sender], menuIdDict[int(content.menuId)][0], int(content.num), menuIdDict[int(content.menuId)][1])
        iid += 1
        orderNumToContent.append(content)
    elif int(content.mode) == 1 :
        if len(orderNumToContent) == 0 :
            return
        content.menuId = int(content.menuId)
        #注文が受理された旨をスタッフ、客に通知
        content_onedari = orderNumToContent.pop(content.menuId-1)
        #おねだりリストを更新
        menu = clear_order(content_onedari.orderId)
        #客に対して送信
        msg = ComUnit(4,content.sender, content_onedari.menuId, content_onedari.num)
        msg.orderId = content.orderId
        client.send(msg)
        msg = ComUnit(4,content_onedari.sender, content_onedari.menuId, content_onedari.num)
        msg.orderId = content_onedari.orderId
        client.send(msg, content.sender)
        #スタッフに対して送信
        msg.reciever = "192.168.0.5"
        client.send(msg, content_onedari.sender)
    elif int(content.mode) == 6 :
        checkOut(content)


ip = "192.168.0.1"
client = Client(ip)
client.prepareSocket()
client.run()
client.setMsgHandler(recvMethod)