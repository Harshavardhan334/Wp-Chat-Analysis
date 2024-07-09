import matplotlib.pyplot as plt
import streamlit as st
import preprocessor
import helper
import Sentiment
import matplotlib.pyplot as pt

st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)
    st.dataframe(df)

    user_list = df['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")
    # user_list.remove(df['users'].iloc(0))
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        #Stats

        numOfMessages, numOfWords = helper.fetch_stats(selected_user, df)
        numOfUrls = helper.countUrl(selected_user, df)
        imageCount, videoCount, stickerCount = helper.countMedia(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total messages")
            st.title(numOfMessages)
        with col2:
            st.header("Total words")
            st.title(numOfWords)
        with col3:
            st.header("Total media")
            st.title(imageCount + videoCount + stickerCount)
        with col4:
            st.header("Total URLs")
            st.title(numOfUrls)

        #user activity

        if selected_user == "Overall":
            st.title("User Activity")
            x, new_df = helper.fetchMostUsers(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # World Cloud

        st.header("Word Cloud")
        df_wc = helper.createWordCloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.header("Most used words")
        mostCommonDf = helper.mostCommonWords(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(mostCommonDf[0], mostCommonDf[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # most common emojis
        st.header("Common Emojis Used")
        mostCommonEmojis = helper.mostUsedEmojis(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(mostCommonEmojis)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(mostCommonEmojis.head()[1], labels=mostCommonEmojis.head()[0])
            st.pyplot(fig)

        if selected_user != 'Overall':
            st.header('Sentiment Analysis : ' + selected_user)
            sdf = Sentiment.Sentiment(df, selected_user)
            st.dataframe(sdf)
