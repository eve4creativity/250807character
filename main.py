import streamlit as st
import pandas as pd
import altair as alt

# 제목
st.title("🌍 국가별 MBTI 분포 시각화")
st.write("국가를 선택하면 해당 국가의 MBTI 유형 분포를 확인할 수 있어요!")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# 국가 선택
country_list = df['Country'].sort_values().tolist()
selected_country = st.selectbox("🔍 국가를 선택하세요", country_list)

# 선택한 국가의 데이터 필터링
row = df[df['Country'] == selected_country].iloc[0]
mbti_types = df.columns[1:]  # MBTI 유형 컬럼
values = row[1:]

# 시각화용 데이터프레임 생성
chart_data = pd.DataFrame({
    'MBTI 유형': mbti_types,
    '비율': values
}).sort_values(by='비율', ascending=False)

# Altair 그래프 생성
chart = alt.Chart(chart_data).mark_bar().encode(
    x=alt.X('MBTI 유형', sort='-y'),
    y=alt.Y('비율', title='비율'),
    color=alt.Color('MBTI 유형', legend=None)
).properties(
    title=f"{selected_country}의 MBTI 유형 분포",
    width=700,
    height=400
)

st.altair_chart(chart, use_container_width=True)

# 비율 데이터표 표시 (선택사항)
with st.expander("📋 데이터 보기"):
    st.dataframe(chart_data.set_index('MBTI 유형').style.format({"비율": "{:.2%}"}))
