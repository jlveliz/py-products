from tkinter import ttk
from tkinter import *

import sqlite3

class Product():
    
    db_name = "database.db"
    
    def __init__(self,window):
        self.wind = window
        self.wind.title("Product App")
        
        #Creating a Frame Container
        frame = LabelFrame(self.wind, text="Register a New Product")
        frame.grid(row=0, column = 0, columnspan = 3, pady = 20)
        
        #name input
        Label(frame,text="Name:").grid(row=1,column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)
        
        #price input
        Label(frame, text="Price:").grid(row=2,column=0)
        self.price = Entry(frame)
        self.price.grid(row=2,column=1)
        
        #button
        ttk.Button(frame,text="Save Products",command= self.addProduct).grid(row=3,column=0,columnspan=3,sticky=W + E)
        
        #message
        self.message =  Label(frame,text='',fg='red')
        self.message.grid(row=4,column=0,columnspan=2,sticky=W+E)
        
        #table
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading("#0", text="Name", anchor=CENTER)
        self.tree.heading("#1", text="Price",anchor=CENTER)
        #filling table
        self.getProducts()
        
        #buttons Edit and Delete
        ttk.Button(text='Delete', command=self.deleteProduct).grid(row=5,column = 0, sticky=W + E)
        ttk.Button(text='Edit', command=self.editProduct).grid(row=5,column = 1, sticky=W + E)
        
        

    def runQuery(self,query, params = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query,params)
            conn.commit()
        return result
    
    def getProducts(self):
        #cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #select data
        query = "SELECT * from product ORDER BY name DESC"
        db_rows = self.runQuery(query)
        for row in db_rows:
            self.tree.insert('',0, text= row[1], values=row[2])
    
    def validate(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0
            
         
    def addProduct(self):
        if self.validate():
            query = "INSERT INTO product VALUES(null, ?,?)"
            parameters = (self.name.get(),self.price.get())
            self.runQuery(query,parameters)
            self.message['text'] = 'Product {} added Successfully'.format(self.name.get())
            self.name.delete(0,END)
            self.price.delete(0,END)
        else:
            self.message['text'] = 'Name and Price are required'
        
        self.getProducts()
    
    
    
    def deleteProduct(self):
        self.message['text'] = ''
        try:
            name = self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e :
            self.message['text'] = 'Please select a record'
            return 
        print(name)
        self.message['text'] = ''
        query = "DELETE FROM product WHERE name = ?"
        self.runQuery(query,(name,))
        self.message['text'] = 'Record {} deleted successfully'.format(name)
        self.getProducts()
    
    def editProduct(self):
        self.message['text'] = ''
        try:
            name = self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e :
            self.message['text'] = 'Please select a record'
            return
        self.message['text'] = ''
        
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = "Edit Wind"
        
        #Old Name
        Label(self.edit_wind,text ="Old Name: ").grid(row=0,column=1)
        Entry(self.edit_wind,textvariable = StringVar(self.edit_wind,value=name), state="readonly").grid(row=0,column=2)
        Label(self.edit_wind,text ="New Name: ").grid(row=1,column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1,column=2)
        
        #Old Price
        Label(self.edit_wind,text ="Old Price: ").grid(row=2,column=1)
        Entry(self.edit_wind,textvariable = StringVar(self.edit_wind,value=old_price), state="readonly").grid(row=2,column=2)
        Label(self.edit_wind,text ="New Price: ").grid(row=3,column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3,column=2)
        
        Button(self.edit_wind, text="Update", command=lambda:self.edit_records(new_name.get(),name, new_price.get(),old_price)).grid(row=4,column=2, sticky=W + E)
    
    def edit_records(self, new_name,name,new_price,old_price):
        query = "UPDATE product set NAME=?, price= ? WHERE name = ? AND price= ?"
        parameters = (new_name,new_price, name, old_price)
        self.runQuery(query,parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated succesfully'.format(new_name)
        self.getProducts()

if __name__ == '__main__':
    window = Tk()
    app = Product(window)
    window.mainloop()