import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px

import requests
import bs4 as bs

def scrape_page(search):
    json_data = []

    for page_number in range(3):
        url = f"https://www.blogdumoderateur.com/page/{page_number}/?s=" + search
        response = requests.get(url)
        soup = bs.BeautifulSoup(response.text, "html.parser")

        article = soup.find_all('article')

        for i in range(len(article)):
            title = article[i].find('h3').text.replace('\xa0', '')
            image = article[i].find('img')['src']
            link = article[i].find('h3').parent['href']
            theme = article[i].find('span', 'favtag').text
            date = article[i].find('time').get('datetime').split('T')[0]

            json_data.append({'title': title, 'image': image, 'link': link, 'theme': theme, 'date': date})


    return json_data

submitted = False

with st.form('Form 1'):
    name = st.text_input('Tape your search')

    if st.form_submit_button('Send Form'):
        scrape_data = scrape_page(name)

        df = pd.DataFrame(scrape_data)
        st.write(df)
        submitted = True


if submitted:
    st.download_button('Download Dataframe', df.to_csv(), 'data.csv', 'text/csv')