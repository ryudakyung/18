import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.linear_model import LinearRegression
import numpy as np

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
st.title("🌍 NOAA CO₂ 데이터 기반 인지력 예측 시뮬레이터")
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
