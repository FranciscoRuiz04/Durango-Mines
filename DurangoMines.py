__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2021, GPS"
__credits__ = "GPS"

__version__ = "1.0.2"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#----------------------Modules--------------------
import gps_postgredb as db
from tkinter import *
from tkinter.messagebox import showinfo
import re

#--------------------Root-------------------------
window1 = Tk()
window1.geometry('675x50')
window1.resizable(1,1)
window1.config(bg='#005f00')
window1.title('Durango Mines')

#--------------------Browser----------------------
df = LabelFrame(window1, bg='#429c3d')
df.pack(fill='x', padx=6, pady=6)

#Message
lab = Label(df,
            text='Mine Name or Contract Number:',
            font=('Times New Roman', 12),
            bg='#429c3d',
            foreground='white',
            padx=10)
lab.grid(row=0, column=0)
#Entry Box
ent = Entry(df, width=40,
            font=('Times New Roman', 13),
            borderwidth=3,
            exportselection=True,
            justify='center',
            bg='#ecd6c0',fg='#2a0000')
ent.grid(row=0, column= 1, columnspan=2)


#-----------------DB Connection----------------------
mines_connection = db.Connection('pasig')


#-----------------Get Values-------------------------
def enlista(select):
    """
    Make a list with the values fetched in the function opendb()
    """
    if type(select) != list:
        return None
    #Create a list with count number
    if len(select) != 1:
        allrecords =[] 
        for tup in select:
            records = []
            for value in tup:
                records.append(value)
            allrecords.append(tuple(records))

    else:
        for tup in select:
            allrecords = []
            for value in tup:
                allrecords.append(value)

    return allrecords   #Return the list with all the count numbers to be use into another function




def consulta1(val):
    if val == None:
        return None
    cols = 'SELECT min_name, area, manager, organization, mun_table, num_contract, sign, start_date, allocation, expedition, num_exp, longitude, latitude '
    intersecs = 'FROM mines_dgo.mines_itrf2008 as geom JOIN mines_dgo.contracts as cont ON geom.fk_numcount = cont.num_contract JOIN mines_dgo.expedients as exped ON cont.fk_exp = exped.id_exp JOIN mines_dgo.dates as dat ON cont.fk_mindate = dat.id_date JOIN mines_dgo.mines as min ON cont.fk_mindate = min.id_mine JOIN mines_dgo.locations as loc ON min.fk_loc = loc.id_loc JOIN mines_dgo.mun as mun ON loc.fk_mun = mun.id_mun '
    if val.isdigit() == False:
        condition = f"WHERE min_name = '{val}';"
    else:
        condition = f"WHERE num_contract = '{val}';"
    q = cols + intersecs + condition
    mines = mines_connection.query2(q)
    mines_enlist = enlista(mines)
    return mines_enlist



#----------------------Get Materials----------------------------------------------
def content_test(text):
    patt = re.compile('Mat')
    return bool(patt.search(text))



def decorator(fn):
    def wrap(val):
        
        intersecs = 'FROM mines_dgo.mines as min JOIN mines_dgo.contracts as cont ON min.id_mine = cont.fk_mindate JOIN mines_dgo.extractions as ext ON cont.num_contract = ext.fk_numcont JOIN mines_dgo.materials as mat ON ext.fk_material = mat.id_material '
        q = fn(val).replace('?', intersecs)
 
        query = mines_connection.query2(q)
        if query == 'There is no one record':
            return query
        else:
            list_mats = []
            for tup in query:
                for value in tup:
                    list_mats.append(value)
            return list_mats

    return wrap

@decorator
def id_mats(val):
    cols = f"SELECT id_material ?WHERE num_contract = {val};"
    return cols

@decorator
def matquery(val):
    cols = f"SELECT name_material ?WHERE num_contract = '{val}';"
    return cols





#------------------------Clean Screen----------------------
def cleanframe():
    df1.destroy()
    df2.destroy()
    btn2.destroy()
    window1.geometry('675x50')



#-------------------------Show Data---------------------------
def getval():
    global df1, df2, btn2
    input = ent.get()
    data = consulta1(input)

    if data == None:
        showinfo(title='Durango Mines', message='No one record found')
    else:
        window1.geometry('735x630')
        #Atributes Frame
        df1 = LabelFrame(window1, bg='#8d4925')
        df1.pack(fill='y', pady=6, padx=6, side='left', anchor='nw')
        

        #Data Frame
        df2 = LabelFrame(window1)
        df2.pack(fill='both',expand='yes', padx=6, pady=6, anchor='ne')

        mycanvas = Canvas(df2, background='#ecd6c0')
        mycanvas.pack(fill='both', expand='yes')


        #Add Horizontal Scrollbar
        xscroll = Scrollbar(df2, orient='horizontal', command=mycanvas.xview)
        xscroll.pack(side='bottom', fill='x')
        mycanvas.configure(xscrollcommand=xscroll.set)
        mycanvas.bind('<Configure>',
                        lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
        myframe = Frame(mycanvas, bg='#ecd6c0')
        mycanvas.create_window((0,0), window=myframe, anchor='nw')


        #Fields Section
        filednames = ('Mine Name :',
                    'Area (Ha) :',
                    'Manager :',
                    'Organization :',
                    'Township :',
                    'Contract Number :',
                    'Sign Date :',
                    'Start Date :',
                    'Allocation Date :',
                    'Expedition Date :',
                    'Expedient Number :',
                    'Longitude (ITRF2008) :',
                    'Latitude (ITRF2008) :')
        for i, f in enumerate(filednames):
            fi = Label(df1, text=f,
                        font=('Times New Roman', 12),
                        bg='#8d4925',
                        fg='white',
                        pady=8,
                        padx=5)
            fi.grid(row=i)
            
            
            #Data Section
            if tuple in [type(v) for v in data]:
                for x in range(len(data)):
                    rec = Label(myframe,
                                text=data[x][i],
                                font=('Times New Roman',12),
                                bg='#ecd6c0',
                                fg='#2a0000',
                                pady=8,
                                padx=25)
                    rec.grid(row=i, column=x)


            else:
                rec2 = Label(myframe,
                                text=data[i],
                                font=('Times New Roman',12),
                                bg='#ecd6c0',
                                fg='#2a0000',
                                pady=8,
                                padx=25)
                rec2.grid(row=i)
        
        #Materials Data
        mats_field = Label(df1,
                            text='Materials :',
                            font=('Times New Roman', 12),
                            bg='#8d4925',
                            fg='white',
                            pady=8,
                            padx=5)
        mats_field.grid(row=13)
        if tuple in [type(v) for v in data]:
            for y in range(len(data)):
                materials = matquery(data[y][5])
                for m in materials:
                    if content_test(m):
                        materials = id_mats(data[y][5])
                # if type(materials) != list:
                #     allmats = 'N/A'
                # else:
                allmats = ', '.join(materials)
                watch_mats = Label(myframe,
                                    text=allmats,
                                    font=('Times New Roman', 12),
                                    bg='#ecd6c0',
                                    fg='#2a0000',
                                    padx=25,
                                    pady=8)
                watch_mats.grid(row=13, column=y)
        else:
            materials = matquery(data[5])
            for m in materials:
                    if content_test(m):
                        materials = id_mats(data[5])
            # f type(materials) != list:
            #     allmats = 'N/A'
            # else:i
            allmats = ', '.join(materials)
            watch_mats = Label(myframe,
                                text=allmats,
                                font=('Times New Roman', 12),
                                bg='#ecd6c0',
                                fg='#2a0000',
                                padx=25,
                                pady=8)
            watch_mats.grid(row=13, column=0)
        

        #Destroyer Buttom
        btn2 = Button(df,
                        text='Clean',
                        font=('Times New Roman', 12, 'bold'),
                        command=cleanframe,
                        border=3,
                        padx=4,
                        bg='#005f00',
                        fg='white')
        btn2.grid(row=0, column=4)



#------------------------Search Button--------------------------
btn1 = Button(df,
                text='Search',
                font=('Times New Roman', 12, 'bold'),
                command=getval,
                border=3,
                bg='#005f00',
                fg='white')
btn1.grid(row=0, column=3)

window1.mainloop()