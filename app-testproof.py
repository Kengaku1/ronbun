# 以下を「app.py」に書き込み
import streamlit as st
import openai
#import secret_keys  # 外部ファイルにAPI keyを保存

#openai.api_key = secret_keys.openai_api_key

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
ou are an excellent academic paper writer. 
Write an academic paper based on some of the given arguments.
If the paper is entered in Japanese or any other language, it will be output in English.
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築


st.title(" 「いい感じに英語論文を書いてくれる」ボット🤖")

st.write("論文の内容を箇条書きで書いて下さい。英語で書いた方が良い感じに出力されますが、日本語で書いても英語で出力してくれます。")

with st.sidebar:
    st.subheader("導きの問い")
    st.write("論文の骨子は固まっていますか？")
    tab1, tab2, tab3, tab4 = st.tabs(["Data Accuracy", "Correctness", "Significance", "Necessity"])

    with tab1:
        st.subheader("このデータは正しい(信頼できる)")
        st.write("1.データはどのように収集しましたか？（どのような実験？測定？出典？）")
        st.write("2.データをどのように加工しましたか？（どのような統計手法？表？グラフ？）") 
    with tab2:
        st.subheader("この研究は正しい（根拠づけられている）")
        st.write("1.この論文で検証したいことは何ですか？")
        st.write("2.データから言えることは何ですか？")
        st.write("3.どんなデータが得られましたか？")    
        st.write("4.この論文で明らかにできたことは何ですか？")
        st.write("5.この論文で明らかにできなかったこと，今後の課題は何ですか？")    
    with tab3:
        st.subheader("この研究は意義がある（学問的コンテキストに対する位置づけ）")
        st.write("1.この論文のテーマに関連する先行研究にはどんなものがありますか？")
        st.write("2.先行研究によって明らかになっていることは，どんなことですか？")
        st.write("3.先行研究によって解明されていないことは，どんなことですか？")    
        st.write("4.この論文は，未解明点についてどのような貢献ができますか？")
        st.write("5.この論文は何を明らかにする研究の一部（ひとつ）ですか？（同種の研究と共通する課題は何ですか？）")    
        st.write("6.この論文独自の着眼点は何ですか？（この論文は同種の研究とどこが違いますか？）")    
    with tab4:
        st.subheader("この研究は必要である（社会的コンテキストに対する位置づけ）")
        st.write("１．この研究は，どのような問題を解決するのに役立ちますか？")  


user_input = st.text_area("入力してください👇", key="user_input",on_change=communicate)


if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])

