import urllib.request

import streamlit as st
from PIL import Image
import plotly.express as px
from bs4 import BeautifulSoup
import requests
import pandas as pd


def request_url(url):
    url = requests.get(url)
    return url


def extract(page, n):
    global maqola_name
    soup = BeautifulSoup(page.text, 'html.parser')
    news = soup.find_all('a', class_='daily-block l-item')[n]['href']
    new_link = 'https://kun.uz' + str(news)
    new_request = BeautifulSoup(requests.get(new_link).text, 'html.parser')
    maqola_name = new_request.find(class_='single-header__title').text
    matn = new_request.find_all('p')
    s = ''
    for a in matn[:]:
        s += a.text + ' '
    arrange = [a for a in s.split()]
    return arrange


def ten_news_total(page):
    links = []
    soup = BeautifulSoup(page.text, 'html.parser')
    news = soup.find_all('a', class_='news-lenta')
    for a in range(5):
        link = 'https://kun.uz' + str(news[a]).split()[2][6:-2]
        new = BeautifulSoup(requests.get(link).text, 'html.parser')
        name = new.find(class_='single-header__title').text
        links.append({name: link})
    return links

def remove_stop_words(words, stop_words):
    result = []
    for a in words:
        if a.lower() not in stop_words:
            result.append(a.lower())
    for i in result[:]:
        if i[-2:] == 'di' or i[-2:] == 'ni' or i[-2:] == 'da' or i[-2:] == 'ga':
            a = result.index(i)
            b = result.pop(a)
            result.append(b[:-2])
        elif i[-5:] == 'yapti':
            a = result.index(i)
            b = result.pop(a)
            result.append(b[:-5])
        elif i[-4:] == 'dagi' or i[-4:] == 'gan.' or i[-4:] == 'imi?' or i[-4:] == 'ning':
            d = result.index(i)
            c = result.pop(d)
            result.append(c[:-4])
        elif i[-3:] == 'dan' or i[-3:] == 'gan' or i[-3:] == 'di.' or i[-3:] == 'da.' or i[-3:] == 'mi?':
            g = result.index(i)
            h = result.pop(g)
            result.append(h[:-3])
        # if i[-1] == ':' or i[-1] == '.' or i[-1] == ',':
        #     a = result.index(i)
        #     s = result.pop(a)
        #     result.append(s[:-1])
        try:
            if len(i) <= 2:
                del result[result.index(i)]
        except:
            pass
        try:
            num = int(i[-1])
            result.remove(i)
        except:
            pass

    return result


def count_words(filter_words):
    result = {}
    for a in filter_words:
        word_count = filter_words.count(a)
        if a not in result.keys():
            result[a] = word_count
    return result


def data_format(data):
    df = pd.DataFrame.from_dict(data, orient='index')
    df1 = df.rename(columns={0:'count'})
    df2 = df1.sort_values(
        'count')
    df3 = df2.tail(15).reset_index()
    df3.columns = ['Words', 'counts']
    return df3


def data_visual(df):
    fig = px.bar(df, x='counts', y="Words", title=f"{maqola_name}", color='counts', orientation='h', width=1500, height=800)
    # fig.show()
    fig.update_layout(
        xaxis_title="Soni",
        yaxis_title="Eng ko'p ishlatilgan so'zlar",
        legend_title="Soni",
        font=dict(
            # family="Courier New, monospace",
            size=18,
            # color="RebeccaPurple"
    ))
    return fig


def _main(n):
    url = 'https://kun.uz/uz/news/list'
    page = request_url(url)
    html_repos = extract(page, n)
    stop_words = ['ta', 'keyin', 'bermoqda?', 'deb', 'haqida', 'ko‘ra', 'ko‘ra', 'bo\'', 'bo`yicha', 'chechagi', 'bu', 'nima', 'kim', 'va', 'olib', 'o‘tkazish', 'hamda', 'bo‘ladi?', 'kengaymoqda,', 'lekin', 'biroq', 'chunki', 'esa', 'agar', 'uchun', 'gar', 'balki', 'go’yo', 'basharti', 'yana', 'garchi', 'go’yoki', 'holbuki', 'vaholanki', 'yoki', 'ham', 'ba`zan', 'uchun?', 'anglatadi?', '-', 'yana', 'bilan', 'nega']
    filter_words = remove_stop_words(html_repos, stop_words)
    clean_data = count_words(filter_words)
    tayyor = data_format(clean_data)
    return data_visual(tayyor)


# def add_logo(logo_path, width, height):
#     url = urllib.request.urlretrieve(logo_path)
#     logo = Image.open('logo.png')
#     modified_logo = logo.resize((width, height))
#     return modified_logo


def main_page():
    # st.sidebar.image(add_logo('https://logobank.uz:8005/media/logos_png/astrum-01.png', width=100, height=80))
    st.sidebar.markdown("# Tanlang 🔎")
    with st.sidebar:
        with st.form(key='my_form'):
            # st.write("Inside the form")
            slider_val = st.slider("Qaysi yangilik?", max_value=25)
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                # st.write("slider", slider_val)
                son = True
    # st.sidebar.number_input('enter', step=1, max_value=20, min_value=1)
    if slider_val == 0:
        st.markdown("<h2 style='text-align: left; color: blue'>Eng So'nggi Yanglik</h2>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2 style='text-align: left; color: blue'>Eng So'nggi {slider_val} Yanglik</h2>", unsafe_allow_html=True)

    st.markdown("""<style>
    .css-k1vhr4 
    {
    display: block;
    margin: 60px;
    }
    .css-hxt7ib {
    padding-top: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}
    .css-hxt7ib h1 {
    font-size: 2.5rem;
    font-weight: 600;
}
                </style>""", unsafe_allow_html=True)
    left, middle, right = st.columns((2, 5, 2))
    if slider_val is None:
        with left:
            st.plotly_chart(_main(0), use_container_width=False)
    else:
        st.plotly_chart(_main(slider_val), use_container_width=False)


main_page()