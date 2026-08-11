import streamlit as st

from balancer import (
    make_team_recommendations,
    get_team_average,
    get_team_job_bonus,
    get_team_special_bonus,
    get_team_player_penalty,
)

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

    # 닉네임을 입력하지 않은 경우
    if name.strip() == "":
        st.warning("닉네임을 입력해주세요.")

    # 이미 같은 닉네임이 등록되어 있는 경우
    elif any(
        player["name"] == name.strip()
        for player in st.session_state.players
    ):
        st.warning("이미 등록된 참가자입니다.")

    else:
        player = {
            "name": name.strip(),
            "combat_power": combat_power,
            "job": job,
            "magic_resistance": magic_resistance,
            "is_sub": is_sub,
            "is_newbie": is_newbie
        }

        st.session_state.players.append(player)

        st.success(f"{name.strip()} 참가자가 추가되었습니다.")

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

        if len(recommendations) == 0:
            st.warning("추천 가능한 팀 조합을 찾지 못했습니다.")

        else:
            for index, result in enumerate(recommendations, start=1):
                st.subheader(f"추천안 {index}")

                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown("### A팀")

                    for player in result["team_a"]:
                        st.write(
                            f'{player["name"]} | {player["job"]}'
                        )

                    st.write(
                        f'마도저항 반영 평균 전투력: '
                        f'{get_team_average(result["team_a"]):.2f}'
                    )

                    st.write(
                        f'직업 보너스: '
                        f'{get_team_job_bonus(result["team_a"]):+.2f}'
                    )

                    st.write(
                        f'특수 캐릭터 보너스: '
                        f'{get_team_special_bonus(result["team_a"]):+.2f}'
                    )

                    st.write(
                        f'부캐/뉴비 보정: '
                        f'{get_team_player_penalty(result["team_a"]):+.2f}'
                    )

                    st.write(
                        f'**팀 평균 전투력: '
                        f'{result["team_a_score"]:.2f}**'
                    )

                with col_b:
                    st.markdown("### B팀")

                    for player in result["team_b"]:
                        st.write(
                            f'{player["name"]} | {player["job"]}'
                        )

                    st.write(
                        f'마도저항 반영 평균 전투력: '
                        f'{get_team_average(result["team_b"]):.2f}'
                    )

                    st.write(
                        f'직업 보너스: '
                        f'{get_team_job_bonus(result["team_b"]):+.2f}'
                    )

                    st.write(
                        f'특수 캐릭터 보너스: '
                        f'{get_team_special_bonus(result["team_b"]):+.2f}'
                    )

                    st.write(
                        f'부캐/뉴비 보정: '
                        f'{get_team_player_penalty(result["team_b"]):+.2f}'
                    )

                    st.write(
                        f'**팀 평균 전투력: '
                        f'{result["team_b_score"]:.2f}**'
                    )
    

                st.info(
                    f'두 팀 평균 전투력 차이: '
                    f'{result["score_difference"]:.2f}'
                )
                # =========================
                # 채팅용 팀 구성
                # =========================

                team_a_names = " / ".join(
                    player["name"] for player in result["team_a"]
                )

                team_b_names = " / ".join(
                    player["name"] for player in result["team_b"]
                )

                copy_text = (
                    f"A팀 - {team_a_names}\n"
                    f"B팀 - {team_b_names}"
                )

                st.text_area(
                    "채팅용 팀 구성",
                    copy_text,
                    height=80,
                    key=f"chat_copy_{index}"
                )

                st.divider()