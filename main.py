import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
from win10toast import ToastNotifier
import numpy as np

toaster = ToastNotifier()

st.set_page_config(page_title="Employee Management System", page_icon="pageicon.png")


def add_bg_from_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
                  background:#D3D3D3 ;
                  secondary_background:#777777;


                  background: linear-gradient(to left, #ffffff,#ffff49 );
                  font: Serif

         }}
         </style>
         """,
        unsafe_allow_html=True
    )


add_bg_from_url()

st.title("Employee Management System")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns([3, 2, 1])
st.sidebar.image("sidebar.png")
with st.sidebar:
    selected = option_menu(menu_title=None, options=["Home", "Employees", "Admin", "Contact", "About"],
                           icons=["house", "file-earmark-person", "file-earmark-person-fill", "telephone-inbound",
                                  "book-half"])

if (selected == "Home"):
    st.write("This Application is Developed by Saurabh as a part of Training Project")
    st.image("employee.png")

elif (selected == "Employees"):

    if 'login' not in st.session_state:
        st.session_state['login'] = False
    id_emp = st.text_input("Enter Employee Id:")
    emp_pass = st.text_input("Enter Password:", type="password")
    btn = st.button("Login")
    if btn:
        mydb = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@', database='employee')
        c = mydb.cursor()
        c.execute("select * from emp_pass")
        for row in c:
            if (row[0] == id_emp and row[1] == emp_pass):
                st.session_state['login'] = True
                toaster.show_toast("Successful", "You are now logged in", duration=2)
                break

        if (st.session_state['login'] == False):
            toaster.show_toast("Login Unsuccessful", "Incorrect ID or Password", duration=2)

    if (st.session_state['login'] == True):
        logout_button = col6.button("Logout")
        if logout_button:
            st.session_state['login'] = False

        else:

            selected = option_menu(
                menu_title=None,
                options=["Employee Database", "Projects", "Messages"],
                orientation='horizontal')

            if selected == "Employee Database":
                choice = st.selectbox("Features", ("None", "Search in Database", "Show all"))
                if choice == "Search in Database":

                    mydb2 = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',
                                                    database='employee')
                    e = mydb2.cursor()
                    e.execute("select * from emp_data")
                    l = []
                    for i in e:
                        l.append(i)

                    df2 = pd.DataFrame(data=l, columns=['emp_id', 'emp_name', 'emp_email', 'emp_phone', 'emp_address',
                                                        'emp_post', 'emp_salary', 'emp_join_date'])

                    selected2 = option_menu(
                           menu_title=None,
                           options=["Search by Name", "Search by Designation"],
                           orientation='horizontal')

                    if selected2=="Search by Name":       
                           name_search = st.text_input("Enter the name")
                           btn4 = st.button("search")
                           if btn4:
                                
                               st.dataframe(df2[["emp_name","emp_email","emp_phone","emp_post"]].where(df2["emp_name"].str.contains(name_search,case=False)==True))

                    if selected2=="Search by Designation":
                            designation=st.text_input("Enter the designation")
                            btn8=st.button("search")
                            df3=pd.DataFrame()
                            if btn8:
                                 
                                 df3=df2[["emp_name","emp_email","emp_phone","emp_post"]].where(df2["emp_post"].str.contains(designation,case=False)==True)
                                 st.dataframe(df3)
                                
                    






                elif choice == "Show all":
                    mydb2 = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',
                                                database='employee')
                    e = mydb2.cursor()
                    e.execute("select * from emp_data")
                    count=0
                    l = []
                    for i in e:
                        l.append(i)
                        count=count+1
                    df2 = pd.DataFrame(data=l,columns=['emp_id', 'emp_name', 'emp_email', 'emp_phone', 'emp_address', 'emp_post','emp_salary', 'emp_join_date'])
                    st.dataframe(df2[["emp_name", "emp_post", "emp_phone", "emp_email"]])
                    st.write("Total no of Employees",count)


            elif selected == "Projects":
                selected2 = option_menu(
                    menu_title=None,
                    options=["Current Projects", "New Projects"],
                    orientation='horizontal')

                if selected2 == "Current Projects":
                    mydb5 = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',
                                                    database='employee')
                    f = mydb5.cursor()
                    f.execute("select * from working_projects")
                    s = []
                    for i in f:
                        s.append(i)
                    df5 = pd.DataFrame(data=s, columns=['empl_id','pname', 'p_comp'])
                    df6=df5[df5['empl_id']==id_emp]
                    st.dataframe(df6)
                    p=st.text_input("Enter name of project whose completion you have to report")
                    if p in df6.values:
                         
                                
                                st.subheader("Enter Project Completion Percentage")
                                

                                comp = st.slider("Choose between range 0 to 100:")
                                comp=str(comp)
                                btn9=st.button("Update")
                                if btn9:
                                     f.execute("update working_projects set p_comp=%s where pname=%s",(comp,p))
                                     mydb5.commit()
                                     toaster.show_toast("Updation Complete", "You have succesfully updated your project completion report", duration=2)
                                     st. experimental_rerun()


                if selected2=="New Projects":
                      mydb5 = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',
                                                    database='employee')
                      f = mydb5.cursor()
                      f.execute("select * from new_projects")
                      s = []
                      for i in f:
                         s.append(i)
                      df5 = pd.DataFrame(data=s, columns=['npname'])
                      st.write("These are new projects pending with company, if any employee have finished their past projects and is intrested in working on them please contact the admin from message section:")
                      st.dataframe(df5)

            elif selected=="Messages":
                selected3 = option_menu(
                    menu_title=None,
                    options=["Message From Admin", "Contact Admin","Contact other Employees","Message from Employees"],
                    )
                if selected3=="Message From Admin":
                      mydb8 = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',
                                                    database='employee')
                      y = mydb8.cursor()
                      y.execute("select * from message_to_emp order by date_time DESC")
                      s = []
                      for i in y:
                         s.append(i)
                      df7 = pd.DataFrame(data=s, columns=['employ_id','message','date_time'])
                      df8=  df7[df7['employ_id']==id_emp]
                      st.dataframe(df8)
                      
                elif selected3=="Contact Admin":
                      mydb14 = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',
                                                    database='employee')
                      
                      
                      y = mydb14.cursor()
                      y.execute("select * from emp_data")
                      name=""
                      des=""
                      for rw in y:
                          if rw[0]== id_emp:
                              name=rw[1]
                              des=rw[5]
                              
                      mes=st.text_input("Enter your message:")
                      btn15=st.button("Send")
                      if btn15:
                          y.execute("insert into message_to_admin values(%s,%s,%s,%s,now())",(id_emp,name,des,mes,))
                          mydb14.commit()
                          st.write("Message sent")
                      

                elif selected3=="Contact other Employees":
                      mydb14 = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',
                                                    database='employee')
                      
                      
                      y = mydb14.cursor()
                      y.execute("select * from emp_data")
                      name=""
                      des=""
                      for rw in y:
                          if rw[0]== id_emp:
                              name=rw[1]
                              des=rw[5]
                      empl_id=st.text_input("Enter employees id you want to message")        
                      mes=st.text_input("Enter your message:")
                      btn16=st.button("Send")
                      if btn16:
                          y.execute("insert into message_to_other_emp values(%s,%s,%s,%s,%s,now())",(empl_id,id_emp,name,des,mes,))
                          mydb14.commit()
                          st.write("Message sent")

                elif selected3=="Message from Employees":
                      mydb14 = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',
                                                    database='employee')
                      
                      
                      y = mydb14.cursor()
                      y.execute("select * from message_to_other_emp order by date_time DESC")
                      s = []
                      for i in y:
                         s.append(i)
                      df14 = pd.DataFrame(data=s, columns=['sent_to','sent_from','employee_name','employee_post','emp_message','date_time'])
                      
                      df15=  df14[df14['sent_to']==id_emp]
                      st.dataframe(df15)

elif selected=="Admin":
    if 'login' not in st.session_state:
        st.session_state['login'] = False
    id_admin = st.text_input("Enter Admin Id:")
    admin_pass = st.text_input("Enter Password:", type="password")
    btn = st.button("Login")
    if btn:
        mydb = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@', database='employee')
        c = mydb.cursor()
        c.execute("select * from founders")
        for row in c:
            if (row[0] == id_admin and row[1] == admin_pass):
                st.session_state['login'] = True
                toaster.show_toast("Successful", "You are now logged in", duration=2)
                break

        if (st.session_state['login'] == False):
            toaster.show_toast("Login Unsuccessful", "Incorrect ID or Password", duration=2)

    if (st.session_state['login'] == True):
        logout_button = col6.button("Logout")
        if logout_button:
            st.session_state['login'] = False

        else:
            selected4 = option_menu(
                    menu_title=None,
                    options=["Employee Database", "Message","Projects","Reports"],
                    orientation='horizontal')

            if selected4=="Employee Database":
                selected5=option_menu(
                    menu_title="Features",
                    options=["Show all Database","Search Database","Update Database","Remove Entry"],
                    )

                if selected5=="Show all Database":
                    mydb2 = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',
                                                database='employee')
                    e = mydb2.cursor()
                    e.execute("select * from emp_data")
                    count=0
                    l = []
                    for i in e:
                        l.append(i)
                        count=count+1
                    df2 = pd.DataFrame(data=l,columns=['emp_id', 'emp_name', 'emp_email', 'emp_phone', 'emp_address', 'emp_post','emp_salary', 'emp_join_date'])
                    btn19=st.button("SHOW")
                    if btn19:
                        st.dataframe(df2)
                        st.write("Total no of Employees",count)

                if selected5=="Search Database":
                    mydb2 = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',
                                                database='employee')
                    e = mydb2.cursor()
                    e.execute("select * from emp_data")
                    
                    l = []
                    for i in e:
                        l.append(i)
                        
                    df2 = pd.DataFrame(data=l,columns=['emp_id', 'emp_name', 'emp_email', 'emp_phone', 'emp_address', 'emp_post','emp_salary', 'emp_join_date'])
                    
                    selected6 = option_menu(
                           menu_title=None,
                           options=["Search by Name", "Search by Designation"],
                           orientation='horizontal')

                    if selected6=="Search by Name":       
                           name_search = st.text_input("Enter the name")
                           btn4 = st.button("search")
                           if btn4:
                                
                               st.dataframe(df2.where(df2["emp_name"].str.contains(name_search,case=False)==True))

                    if selected6=="Search by Designation":
                            designation=st.text_input("Enter the designation")
                            btn8=st.button("search")
                            df3=pd.DataFrame()
                            if btn8:
                                 df3=df2.where(df2["emp_post"].str.contains(designation,case=False)==True)
                                 st.dataframe(df3)

                if selected5=="Update Database":
                                      choice = st.selectbox("Features", ("None", "New Entry", "Update Entry"))
                                      if choice == "New Entry":
                                          emp_id=st.text_input("Employee Id:")
                                          emp_name=st.text_input("Employee Name:")
                                          emp_email=st.text_input("Email:")
                                          emp_phone=st.text_input("Phone No:")
                                          emp_address=st.text_input("Address:")
                                          emp_post=st.text_input("Post:")
                                          emp_salary=st.text_input("Salary(per month):")
                                          emp_joining=st.text_input("Joining date(yyyy-mm-dd):")
                                          emp_password=st.text_input("Password",type='password')
                                          mydb2 = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',database='employee')
                                          e = mydb2.cursor()
                                          
                                          btn16=st.button("Update")
                                          if btn16:
                                              e.execute("insert into emp_data values(%s,%s,%s,%s,%s,%s,%s,%s)",(emp_id,emp_name,emp_email,emp_phone,emp_address,emp_post,emp_salary,emp_joining))
                                              e.execute("insert into emp_pass values(%s,%s)",(emp_id,emp_password))
                                              mydb2.commit()
                                              toaster.show_toast("New Data Update", "Updation Complete", duration=2)
                                          st.experimental_rerun()   

                                      if choice=="Update Entry":
                                            emp_id=st.text_input("Employee Id:")
                                            mydb3=mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',database='employee')
                                            f=mydb3.cursor()
                                            f.execute("select * from emp_data")
                    
                                            m = []
                                            for j in f:
                                               m.append(j)
                        
                                            df7 = pd.DataFrame(data=m,columns=['emp_id', 'emp_name', 'emp_email', 'emp_phone', 'emp_address', 'emp_post','emp_salary', 'emp_join_date'])
                                            
                                            
                                            if emp_id in df7.values:
                                                    
                                                    emp_name=st.text_input("Employee Name:")
                                                    emp_email=st.text_input("Email:")
                                                    emp_phone=st.text_input("Phone No:")
                                                    emp_address=st.text_input("Address:")
                                                    emp_post=st.text_input("Post:")
                                                    emp_salary=st.number_input("Salary(per month):")
                                                    emp_joining=st.date_input("Joining date(yyyy-mm-dd):")
                                                    emp_password=st.text_input("Password",type='password')
                                                    btn18=st.button("Update")
                                                    if btn18:
                                                        
                                                        f.execute("update emp_data set emp_name=%s,emp_email=%s,emp_phone=%s,emp_address=%s,emp_post=%s,emp_salary=%s,emp_join_date=%s where emp_id=%s",
                                                                  (emp_name,emp_email,emp_phone,emp_address,emp_post,emp_salary,emp_joining,emp_id))
                                                        f.execute("update emp_pass set pass=%s where emp_id=%s",(emp_password,emp_id))
                                                        mydb3.commit()
                                                        toaster.show_toast("New Data Update", "Updation Complete", duration=2)
                                                        
                                            else:
                                                  st.write("Invalid ! Id not found in database")

                                                  
                if selected5=="Remove Entry":
                    t=st.text_input("Enter Book Id you want to remove:")
                    btn21=st.button("Remove-")
                    if btn21:
                      mydb7=mysql.connector.connect(host='localhost',user='root',password='Saurabh2103@',database='employee')
                      e=mydb7.cursor()
                      f="delete from emp_data where emp_id='"+t+"'"
                      e.execute(f)
                      mydb7.commit()
                      st.caption("Updated")

            if selected4=="Message":
               selected9 = option_menu(
                           menu_title=None,
                           options=["Message Employees", "Inbox"]
                           )
               if selected9=="Message Employees":
                   
                      mydb17 = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',
                                                    database='employee')
                      
                      
                      y = mydb17.cursor()
                      y.execute("select * from emp_data")
                      
                      idd=st.text_input("Enter Employee id:")
                      m=[]
                      for j in y:
                          m.append(j)
                      df7 = pd.DataFrame(data=m,columns=['emp_id', 'emp_name', 'emp_email', 'emp_phone', 'emp_address', 'emp_post','emp_salary', 'emp_join_date'])
                      if idd in df7.values:
                              
                          mes=st.text_input("Enter your message:")
                          btn15=st.button("Send")
                          if btn15:
                              y.execute("insert into message_to_emp values(%s,%s,now())",(idd,mes,))
                              mydb17.commit()
                              st.write("Message sent")

               if selected9=="Inbox":
                    mydb17 = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',
                                                    database='employee')
                      
                      
                    y = mydb17.cursor()
                    y.execute("select * from message_to_admin order by date_time DESC")
                    s=[]
                    for t in y:
                        s.append(t)
                    df7=pd.DataFrame(data=s,columns=['employee_id','employee_name','employee_post','emp_message','date_time'])
                    st.dataframe(df7)


            if selected4=="Projects":
                selected11 = option_menu(
                           menu_title=None,
                           options=["Currently Working","New Projects"])

                if selected11=="Currently Working":
                    mydb17 = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',
                                                    database='employee')
                      
                      
                    y = mydb17.cursor()
                    y.execute("select * from working_projects")
                    s=[]
                    for i in y:
                        s.append(i)
                    df7=pd.DataFrame(data=s,columns=['empl_id','pname','p_comp'])
                    choice11=st.selectbox("Features",("None","Show all","Add new"))
                    if choice11=="Show all":       
                        st.dataframe(df7)
                    elif choice11=="Add new":
                        empid=st.text_input("Enter Employee Id:")
                        pro=st.text_input("Enter Project name:")
                        comp=st.text_input("Enter Project Completion Percentage")
                        btn23=st.button("Update")
                        if btn23:
                            y.execute("insert into working_projects values(%s,%s,%s)",(empid,pro,comp))
                            st.write("updation successful !!!")
                if selected11=="New Projects":
                     mydb17 = mysql.connector.connect(host='localhost', user='root', password='Saurabh2103@',
                                                    database='employee')
                      
                      
                     y = mydb17.cursor()
                     choice11=st.selectbox("Features",("None","Show all","Add a new Project"))
                     if choice11=="Show all":
                           y.execute("select * from new_projects")
                           g=[]
                           for k in y:
                               g.append[k]
                           df9=pd.DataFrame(data=g,columns=['npname'])
                           st.dataframe(df9)
                     elif choice11=="Add a new Project":
                            m=st.text_input("Enter Project name:")
                            btn29=st.button("Update")
                            if btn29:
                                y.execute("insert into new_projects values(%s)",(m))
                                st.write("Succesfully updated !!!")


elif selected=="Contact":
    st.write("Email:    xxxx@companyltd")
    st.write("Phn No:   xxxxxx")
    st.write("Address:  xxxxx")

elif selected=="About":
    st.write("This company was established in year xxxxx.........")
                     
                     
                            
                    
                    
                
                      

                
                   

                    
                                                  

                                            
                                                        
                                          
                                          


                                 


            
                    
                      
                          
                      
                      
                     
                      
                          
                    
        
                          
                                
