import streamlit as st
import json
from author import hash_password,autor
from datetime import datetime

def register_user(username, password):
    if 'users' not in st.session_state:
        st.session_state.users = {}
    st.session_state.users[username] = password
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'show_register' not in st.session_state:
    st.session_state.show_register = False 
    
    
    
if not st.session_state.logged_in:
    # Переключатель между формами входа и регистрации    
        
    if st.session_state.show_register:
        st.title("📝 Регистрация")
        new_username = st.text_input("Новый логин", key="reg_user")
        new_password = st.text_input("Новый пароль", type="password", key="reg_pass1")
        confirm_password = st.text_input("Повторите пароль", type="password", key="reg_pass2")
        
        if st.button("Зарегистрироваться"):
            with open('user2.json','r') as file:
                print('Test base working')
                d = json.load(file)
                
            # проверяю еслть ли такой пользователб или нет    
            if new_username in d:
                st.error('This username is already taken')
            else:   
                if not new_username or not new_password:
                    st.error("Заполните все поля")
                elif new_password != confirm_password:
                    st.error("Пароли не совпадают!")
                else:
                    register_user(new_username, new_password)
                    st.success("Регистрация успешна! Можете войти")
                    st.session_state.show_register = False
                    with open('user2.json','r', encoding="utf-8") as file:
                        data = json.load(file)
                    data[new_username] = hash_password(new_password) # записываем нового пользователя 
                    
                    
                    
                    # Запись в базу нового пользователя (уже обновляем базу)
                    with open('user2.json','w', encoding="utf-8") as file:
                        json.dump(data,file,indent=4, ensure_ascii=False)
                        
                        
                        
                    
        if st.button("← Назад к входу"):
            st.session_state.show_register = False
            st.rerun()
    
    else:
        # Форма входа
        st.title("🔒 Вход в систему")
        username = st.text_input("Логин")
        password = st.text_input("Пароль", type="password")
        us2 = username
        if st.button("Войти"):
            # Проверяю на подписку
            if autor(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Неверные данные")
        if st.button("Создать новый аккаунт"):
            st.session_state.show_register = True
            st.rerun()
    
    st.stop()
# Основной интерфейс после авторизации
st.success(f"✅ Welcome to Alexandria, {st.session_state.username}!")        


def create_post(title, author, content, tags=None):
    """
    Создает красивый пост в Streamlit с заданными параметрами
    
    Параметры:
    - title: заголовок поста
    - author: автор поста
    - content: содержание поста
    - tags: список тегов (необязательный)
    """
    if tags is None:
        tags = []
    
    st.markdown(f"""
    <div style="
        padding: 20px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    ">
        <h2 style="margin-top: 0; color: #2c3e50;">{title}</h2>
        <div style="
            color: #7f8c8d;
            font-size: 0.85em;
            margin-bottom: 15px;
        ">
            Автор: {author}
        </div>
        <p style="color: #34495e; line-height: 1.6;">{content}</p>
        {f'<div style="margin-top: 15px;">' + 
         ''.join([f'<span style="background: #e0f2fe; color: #0369a1; padding: 3px 8px; border-radius: 12px; margin-right: 5px; font-size: 0.8em;">{tag}</span>' 
                 for tag in tags]) + '</div>' if tags else ''}
    </div>
    """, unsafe_allow_html=True)
    
    
    
st.title(st.session_state.username)



title = st.text_input("Title for the post",placeholder="Create a title")
post = st.text_input("Make a post",placeholder="Today i...")
st.badge("Your posts")
with open("pages/posts.json",'r') as file:
    ps = json.load(file)
seen = []    
titles = []     
for user in ps:
    if st.session_state.username == user["username"]:
        for i in user["posts"]:
            if i not  in seen:
                seen.append(i)
        for j in user["titles"]:
            titles.append(j)                
d = datetime.now()
f = str(d).split()[0]           
if post != "":
    for i in ps:
        if st.session_state.username == user["username"]:
            user["posts"].append(post)
            user["time"].append(f)
            user["titles"].append(title)
            
    with open("pages/posts.json",'w') as file:
        json.dump(ps,file,indent=2)        
    seen.append(post)            
with open('pages/posts.json','r') as file:
    times = json.load(file)    
times2 = []        
for user in times:
    if st.session_state.username == user["username"]:
        for j in user["time"]:
            times2.append(j)   
print(f"Len of posts {list(set(seen))}")
print(f"Len of titles {list(set(titles))}")   
print(f"Len of times {list(set(times2))}")                    
for post in range(len(list(set(seen)))):   
    #tit = st.text(list(set(titles))[post])        
    #pss = st.text_area(f"Post{post},Time: {times2[post]}",seen[post])                
    create_post(list(set(titles))[post],st.session_state.username,seen[post],tags = times2[post] )
    
    