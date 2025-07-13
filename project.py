import streamlit as st
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.linear_model import LinearRegression
import numpy as np

def draw_co2_gra():
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False


    # === 인지력 예측 함수 ===
    def predict_concentration(co2_ppm):
        if co2_ppm < 400:
            return 100
        elif co2_ppm < 600:
            return 100 - (co2_ppm - 400) * 0.05
        else:
            return 90 - (co2_ppm - 600) * 0.1

    # === CSV 파일 불러오기 ===
    df = pd.read_csv("co2_gr_gl.csv", comment="#")
    df = df.rename(columns={"year": "year", "ann inc": "co2_increase"})
    df["co2_ppm"] = 315.97 + df["co2_increase"].cumsum()  # 누적 CO2 농도 계산

    # === 데이터 준비 ===
    X = df["year"].values.reshape(-1, 1)
    y = df["co2_ppm"].values

    # === 선형 회귀로 미래 CO₂ 예측 ===
    model = LinearRegression()
    model.fit(X, y)

    future_years = np.arange(2025, 2101, 5).reshape(-1, 1)
    future_co2 = model.predict(future_years)

    # === 과거 + 미래 합치기 ===
    all_years = np.concatenate((X, future_years), axis=0).flatten()
    all_co2 = np.concatenate((y, future_co2), axis=0)
    all_scores = [predict_concentration(ppm) for ppm in all_co2]

    # === Streamlit 시작 ===
    st.set_page_config("NOAA CO₂ 기반 인지력 예측", page_icon="🧠")
    st.markdown("🌍 NOAA CO₂ 데이터 기반 인지력 예측 시뮬레이터")
    st.markdown("**실제 NOAA 연간 CO₂ 증가량 데이터**를 기반으로 누적 CO₂ 농도를 계산하고, 인지력 변화를 시뮬레이션합니다.")

    # === 그래프 출력 ===
    fig, ax1 = plt.subplots()

    color1 = 'tab:green'
    ax1.set_xlabel('연도')
    ax1.set_ylabel('CO₂ 농도 (ppm)', color=color1)
    ax1.plot(all_years, all_co2, color=color1, label="CO₂ 농도")
    ax1.tick_params(axis='y', labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('인지력 (%)', color=color2)
    ax2.plot(all_years, all_scores, color=color2, linestyle='--', label="인지력")
    ax2.tick_params(axis='y', labelcolor=color2)

    fig.tight_layout()
    st.pyplot(fig)

    st.caption("※ Global 기준 1959년 CO₂ 농도 315.97ppm에서 시작한 누적 계산입니다.")

# 페이지 설정
if "page" not in st.session_state:
    st.session_state.page = "lobby"

# 페이지 바꾸는 함수 설정
def change_to_page(page_name):
    st.session_state.page = page_name

# 제목 설정
st.title("기후 변화에 따른 미래 인체 예측기")

# 기본 화면
if st.session_state.page == 'lobby':
    st.subheader("인물 설정")
    # session_stateage.변수이름 : session_state로 설정한 다른 페이지여도 변수 사용 가능
    st.session_state.age = int(st.number_input('나이를 입력하세요'))
    st.session_state.gender = st.selectbox('성별을 선택하세요', ['남성', '여성'])
    if st.button('인물 설정 완료'):
        # 기본 정보 선택 시 selection 창으로 넘어 감
        if st.session_state.age < 0:
            st.write('나이를 다시 입력하세요')
        else:
            change_to_page('selection')


# selection 창으로 넘어 왔을 때 입력 정보에 따라 나누어짐
elif st.session_state.page == 'selection':

    if st.session_state.age <= 13:
        st.subheader("아동기 / " + "성별 : " + st.session_state.gender)
        temp = st.slider("기온 변화 (°C)", -5, 5, 0)
        co2 = st.slider("CO₂ 농도 (ppm)", 400, 600, 450)
        pollution = st.selectbox("대기오염 수준", ["낮음", "보통", "높음"])

        if temp >= 2.5:
            st.write("🌡️ 탈수 및 열사병 위험이 높아졌습니다.")
        elif temp >= 1.0:
            st.write("😓 불쾌지수 증가 및 수면 질 저하 가능성.")
        elif temp <= -2.0:
            st.write("🧊 저체온증과 순환기계 이상 위험이 있습니다.")
        else:
            st.write("✅ 성장에는 큰 영향 없음")

        # 철 결핍
        if co2 >= 500:
            st.write("🩸 **영양소 감소**: 철, 아연, 단백질 함량 ↓ → 피로감, 면역력 약화")
        else:
            st.write("✅ 영양소 수준은 안정적")
        # 호흡기 문제
        if pollution == "높음":
            st.write("🌫️ **호흡기 질환 위험** ↑: 천식, 폐 질환 증가 가능성")
        elif pollution == "보통":
            st.write("⚠️ 약한 호흡기 부담 예상")
        else:
            st.write("✅ 호흡기 건강에 큰 문제 없음")

        draw_co2_gra()
    

    elif st.session_state.age <= 19:
        st.subheader("청소년기 / " + "성별 : " + st.session_state.gender)
        temp = st.slider("기온 상승 (°C)", 0, 5, 2)
        co2 = st.slider("CO₂ 농도 (ppm)", 400, 600, 450)
        pollution = st.selectbox("대기오염 수준", ["낮음", "보통", "높음"])
        if temp >= 2.5:
            st.write("🌡️ 탈수 및 열사병 위험이 높아졌습니다.")
        elif temp >= 1.0:
            st.write("😓 불쾌지수 증가 및 수면 질 저하 가능성.")
        elif temp <= -2.0:
            st.write("🧊 저체온증과 순환기계 이상 위험이 있습니다.")
        else:
            st.write("✅ 성장에는 큰 영향 없음")

        # 철 결핍
        if co2 >= 500:
            st.write("🩸 **영양소 감소**: 철, 아연, 단백질 함량 ↓ → 피로감, 면역력 약화")
        else:
            st.write("✅ 영양소 수준은 안정적")
        # 호흡기 문제
        if pollution == "높음":
            st.write("🌫️ **호흡기 질환 위험** ↑: 천식, 폐 질환 증가 가능성")
        elif pollution == "보통":
            st.write("⚠️ 약한 호흡기 부담 예상")
        else:
            st.write("✅ 호흡기 건강에 큰 문제 없음")
        
        draw_co2_gra()

    else:
        st.subheader("성인 / " + "성별 : " + st.session_state.gender)
        temp = st.slider("기온 상승 (°C)", 0, 5, 2)
        co2 = st.slider("CO₂ 농도 (ppm)", 400, 600, 450)
        pollution = st.selectbox("대기오염 수준", ["낮음", "보통", "높음"])
        if temp >= 2.5:
            st.write("🌡️ 탈수 및 열사병 위험이 높아졌습니다.")
        elif temp >= 1.0:
            st.write("😓 불쾌지수 증가 및 수면 질 저하 가능성.")
        elif temp <= -2.0:
            st.write("🧊 저체온증과 순환기계 이상 위험이 있습니다.")
        else:
            st.write("✅ 성장에는 큰 영향 없음")

        # 철 결핍
        if co2 >= 500:
            st.write("🩸 **영양소 감소**: 철, 아연, 단백질 함량 ↓ → 피로감, 면역력 약화")
        else:
            st.write("✅ 영양소 수준은 안정적")
        # 호흡기 문제
        if pollution == "높음":
            st.write("🌫️ **호흡기 질환 위험** ↑: 천식, 폐 질환 증가 가능성")
        elif pollution == "보통":
            st.write("⚠️ 약한 호흡기 부담 예상")
        else:
            st.write("✅ 호흡기 건강에 큰 문제 없음")
        
        draw_co2_gra()