import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

plt.rcParams['axes.unicode_minus'] = False  # Avoids Unicode issues
plt.rcParams['font.family'] = 'Segoe UI Emoji'  # Windows Emoji Font

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("### Total Messages")
            st.markdown(f"## {num_messages}")
        with col2:
            st.markdown("### Total Words")
            st.markdown(f"## {words}")
        with col3:
            st.markdown("### Media Shared")
            st.markdown(f"## {num_media_messages}")
        with col4:
            st.markdown("### Links Shared")
            st.markdown(f"## {num_links}")

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heat_map = helper.activity_heat_map(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heat_map)
        st.pyplot(fig)


        # finding the busiest user in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(new_df)
            with col2:
                ax.bar(x.index, x.values, color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

        # Wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation = 'vertical')

        st.title('Most common words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoj_helper(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        # with col2:
        #     fig,ax = plt.subplots()
        #     ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
        #     st.pyplot(fig)
        # Emoji Analysis

        with col2:
            fig, ax = plt.subplots(figsize=(6, 6))

            # Define Colors
            colors = sns.color_palette("pastel")

            # Creating Pie Chart
            wedges, texts, autotexts = ax.pie(
                emoji_df[1].head(),
                labels=emoji_df[0].head(),
                autopct="%0.2f%%",
                colors=colors,
                textprops={'fontsize': 14},
                wedgeprops={'edgecolor': 'black'},
                pctdistance=0.85,
                shadow=True
            )

            # Adjust label size
            for text in texts:
                text.set_fontsize(16)
                text.set_fontweight('bold')

            for autotext in autotexts:
                autotext.set_fontsize(12)
                autotext.set_color('black')

            ax.set_title("Top Used Emojis", fontsize=18, fontweight='bold', pad=20)
            st.pyplot(fig)


