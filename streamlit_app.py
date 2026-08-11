import streamlit as st
from balancer import make_team_recommendations

st.title("장난감 길드")
# 참가자 목록이 아직 없으면 빈 리스트 만들기
if "players" not in st.session_state:
    st.session_state.players = []

st.subheader("참가자 등록")

name = st.text_input("닉네임")

combat_power = st.number_input(
    "전투력",
    min_value=0.0,
    step=0.01,
    format="%.2f"
)

job = st.selectbox(
    "직업",
    [
        "사제", "전사", "마법사", "수도사",
        "장궁병", "듀얼블레이드", "대검전사", "검술사",
        "기사", "궁수", "석궁사수", "빙결술사",
        "화염술사", "전격술사", "힐러", "암흑술사",
        "도적", "격투가", "음유시인", "악사", "댄서"
    ]
)

magic_resistance = st.number_input(
    "마도저항",
    min_value=0,
    step=1
)

is_sub = st.checkbox("부캐")
is_newbie = st.checkbox("뉴비")

if st.button("참가자 추가"):
    player = {
        "name": name,
        "combat_power": combat_power,
        "job": job,
        "magic_resistance": magic_resistance,
        "is_sub": is_sub,
        "is_newbie": is_newbie
    }

    st.session_state.players.append(player)

st.subheader("참가자 목록")

for index, player in enumerate(st.session_state.players):
    col1, col2 = st.columns([5, 1])

    with col1:
        st.write(
            f'{player["name"]} | '
            f'{player["job"]} | '
            f'전투력 {player["combat_power"]:.2f} | '
            f'마도저항 {player["magic_resistance"]}'
        )

    with col2:
        if st.button("삭제", key=f"delete_{index}"):
            st.session_state.players.pop(index)
            st.rerun()    

st.divider()

if st.button("팀 추천하기"):
    if len(st.session_state.players) < 2:
        st.warning("팀 편성을 위해 참가자를 2명 이상 등록해주세요.")

    else:
        recommendations = make_team_recommendations(
            st.session_state.players
        )

        st.write(recommendations)