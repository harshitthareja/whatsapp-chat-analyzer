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



# import streamlit as st
# import preprocessor, helper
# import matplotlib.pyplot as plt
# import seaborn as sns
# from wordcloud import WordCloud
# from io import BytesIO
# import numpy as np
#
# # Apply a modern theme
# st.set_page_config(page_title="WhatsApp Chat Analyzer", page_icon="📊", layout="wide")
#
# # Custom CSS for Styling
# st.markdown("""
#     <style>
#         /* General Layout */
#         .stApp {
#             background-color: #0E1117;
#             color: #E1E1E1;
#         }
#         /* Titles & Headers */
#         .stTitle, .stHeader {
#             font-size: 30px;
#             font-weight: bold;
#             color: #58A6FF;
#         }
#         /* Metric Styling */
#         div[data-testid="metric-container"] {
#             background: linear-gradient(120deg, #1F2937, #374151);
#             padding: 15px;
#             border-radius: 10px;
#             box-shadow: 0 4px 8px rgba(0,0,0,0.2);
#         }
#         /* Dataframe Styling */
#         .dataframe {
#             background-color: #1F2937 !important;
#             border-radius: 10px;
#             color: white;
#         }
#     </style>
# """, unsafe_allow_html=True)
#
# # Sidebar
# st.sidebar.title("📊 WhatsApp Chat Analyzer")
# st.sidebar.markdown("🚀 Upload your chat file to begin analysis!")
#
# uploaded_file = st.sidebar.file_uploader("📂 Upload a WhatsApp Chat File (.txt)")
# if uploaded_file is not None:
#     bytes_data = uploaded_file.getvalue()
#     data = bytes_data.decode("utf-8")
#     df = preprocessor.preprocess(data)
#
#     # Fetch unique users
#     user_list = df['user'].unique().tolist()
#     user_list = [user for user in user_list if user != "group_notification"]
#     user_list.sort()
#     user_list.insert(0, "Overall")
#
#     selected_user = st.sidebar.selectbox("📌 Select User", user_list)
#
#     if st.sidebar.button("🔍 Analyze"):
#
#         # --- 🟢 Top Statistics ---
#         num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
#         st.title("📈 Chat Statistics")
#         col1, col2, col3, col4 = st.columns(4)
#         col1.metric("💬 Total Messages", num_messages)
#         col2.metric("📝 Total Words", words)
#         col3.metric("📸 Media Shared", num_media_messages)
#         col4.metric("🔗 Links Shared", num_links)
#
#         # --- 📅 Monthly Timeline ---
#         st.subheader("📆 Monthly Activity")
#         timeline = helper.monthly_timeline(selected_user, df)
#         fig, ax = plt.subplots(figsize=(10, 4))
#         sns.lineplot(data=timeline, x="time", y="message", marker="o", color="#58A6FF", linewidth=2)
#         ax.set_xlabel("Month", fontsize=12)
#         ax.set_ylabel("Messages", fontsize=12)
#         plt.xticks(rotation=45)
#         st.pyplot(fig)
#
#         # --- 📊 Daily Timeline ---
#         st.subheader("📅 Daily Activity")
#         daily_timeline = helper.daily_timeline(selected_user, df)
#         fig, ax = plt.subplots(figsize=(10, 4))
#         sns.lineplot(data=daily_timeline, x="only_date", y="message", marker="o", color="#FF7F50", linewidth=2)
#         ax.set_xlabel("Date", fontsize=12)
#         ax.set_ylabel("Messages", fontsize=12)
#         plt.xticks(rotation=45)
#         st.pyplot(fig)
#
#         # --- 🔥 Most Active Users ---
#         if selected_user == 'Overall':
#             st.subheader("👥 Most Active Users")
#             x, new_df = helper.most_busy_users(df)
#             col1, col2 = st.columns([1, 2])
#             with col1:
#                 st.dataframe(new_df.style.set_properties(**{'background-color': '#1F2937', 'color': 'white'}))
#             with col2:
#                 fig, ax = plt.subplots(figsize=(8, 4))
#                 sns.barplot(y=x.index, x=x.values, palette="coolwarm", ax=ax)
#                 ax.set_xlabel("Messages", fontsize=12)
#                 st.pyplot(fig)
#
#         # --- ☁️ WordCloud ---
#         st.subheader("☁️ Most Common Words")
#         df_wc = helper.create_wordcloud(selected_user, df)
#         fig, ax = plt.subplots(figsize=(8, 4))
#         ax.imshow(df_wc, interpolation="bilinear")
#         ax.axis("off")
#         st.pyplot(fig)
#
#         # --- 🔡 Most Common Words ---
#         st.subheader("🔡 Frequently Used Words")
#         most_common_df = helper.most_common_words(selected_user, df)
#         fig, ax = plt.subplots(figsize=(8, 4))
#         sns.barplot(y=most_common_df[0], x=most_common_df[1], palette="Blues_r", ax=ax)
#         ax.set_xlabel("Count", fontsize=12)
#         ax.set_ylabel("Words", fontsize=12)
#         st.pyplot(fig)
#
#         # --- 😂 Emoji Analysis ---
#         st.subheader("😂 Emoji Analysis")
#         emoji_df = helper.emoj_helper(selected_user, df)
#         col1, col2 = st.columns([1, 1])
#         with col1:
#             st.dataframe(emoji_df.style.set_properties(**{'background-color': '#1F2937', 'color': 'white'}))
#         with col2:
#             fig, ax = plt.subplots(figsize=(5, 5))
#             colors = sns.color_palette("pastel")
#             ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f%%", colors=colors, shadow=True)
#             ax.set_title("Top Emojis", fontsize=14, fontweight="bold")
#             st.pyplot(fig)


