import matplotlib.pyplot as plt
import streamlit as st
import helper
import preprocessor

st.sidebar.title("WHATSAPP CHAT ANALYZER")
f = open("sample/sample.txt", "r",encoding="utf8")
sample_data = f.read()
uploaded_file = st.sidebar.file_uploader("Upload Your WhatsApp Group Exported (without Media) txt file",type="txt")

if uploaded_file is not None:
    # To read file as bytes:
    try:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        data = preprocessor.preprocess(data)
        st.dataframe(data)

        st.download_button(
            label="Download data as CSV",
            data=data.to_csv(),
            file_name='whatsapp_data_output.csv',
            mime='text/csv',
            help = "When You Click On Download Button Your WhatsApp Text Data Will Be Converted To Clean Downloadable CSV File"
        )

        user_list = data["user"].unique().tolist()
        user_list.sort()
        user_list.remove("group_notification")
        user_list.insert(0, "Overall")
        selected_user = st.sidebar.selectbox('Which user would you like to see Analysis(Select and Click Show Analysis button)',(user_list))

        if st.sidebar.button("Show Analysis"):
            num_messages, words, num_media_messages, link = helper.fetch_stats(selected_user, data)

            st.title("Top Statistics")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("Total Messages Contributed by {}".format(selected_user))
                st.title(num_messages)
            
            with col2:
                st.subheader("Total Words of Messages by {}".format(selected_user))
                st.title(words)
            with col3:
                st.subheader("Total Link Shared by {}".format(selected_user))
                st.title(link)
            
            if selected_user == "Overall":
                
                st.subheader("Top 5 Most Active Users and Percentage contribution made by user")

                x,percent_data = helper.fetch_most_active_user(data)
                fig, ax = plt.subplots()

                col1, col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values, color="green")
                    plt.xticks(rotation=80)
                    st.pyplot(fig)
                
                with col2:
                    st.dataframe(percent_data)
            
            st.subheader("Word Cloud for {}".format(selected_user))
            wc_image = helper.created_word_cloud(selected_user, data)

            fig, ax = plt.subplots()
            ax.imshow(wc_image)
            st.pyplot(fig)

            most_common_data = helper.most_common_words(selected_user, data)
            fig, ax = plt.subplots()
            ax.barh(most_common_data[0], most_common_data[1])
            plt.xticks(rotation=80)
            st.subheader("Most Common Words Used by {}".format(selected_user))
            st.pyplot(fig)

    except:
        st.error('Please Upload The WhatsApp Exported txt File not any other File.')
