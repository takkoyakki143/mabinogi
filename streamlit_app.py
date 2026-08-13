import streamlit as st
from datetime import date
from supabase import create_client
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

from balancer import (
    make_team_recommendations,
    get_team_average,
    get_team_job_bonus,
    get_team_special_bonus,
    get_team_player_penalty,
)

# =========================
# 사이트 디자인
# =========================

st.markdown(
    """
    <style>

    /* 전체 배경 */
    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(65, 115, 130, 0.45) 0%,
                rgba(35, 67, 78, 0.30) 30%,
                rgba(18, 31, 37, 0.15) 60%
            ),
            linear-gradient(
                135deg,
                #202b30 0%,
                #172126 50%,
                #121a1e 100%
            );

        color: #f7f8f8;
    }

    /* 화면 전체 폭 */
    .block-container {
        max-width: 1050px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    /* 기본 제목 색상 */
    h1, h2, h3 {
        color: #f4f7f7;
    }

    /* 작은 길드 이름 */
    .guild-name {
        color: #ff7355;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    /* 메인 제목 */
    .raid-title {
        color: #fff8f3;
        font-size: 2.8rem;
        font-weight: 800;
        line-height: 1.15;
        margin-bottom: 0.6rem;
    }

    /* 제목 아래 설명 */
    .raid-description {
        color: #aeb8bb;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* 반투명 카드 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(23, 35, 41, 0.72);
        border: 1px solid rgba(143, 186, 198, 0.18);
        border-radius: 18px;
        padding: 18px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
    }

    /* 참가자 카드 */
    .player-card {
        background: rgba(22, 34, 40, 0.72);
        border: 1px solid rgba(145, 185, 195, 0.16);
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 10px;
        backdrop-filter: blur(10px);
    }

    .player-card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
    }

    .player-name {
        color: #ffffff;
        font-size: 1.15rem;
        font-weight: 800;
    }

    .player-job {
        color: #b7c4c8;
        font-size: 0.9rem;
    }

    .player-stats {
        display: flex;
        gap: 40px;
    }

    .stat-label {
        color: #98a9ae;
        font-size: 0.8rem;
        margin-right: 8px;
    }

    .combat-power {
        color: #ff7355;
        font-size: 1.15rem;
        font-weight: 800;
    }

    .magic-resistance {
        color: #62d6f5;
        font-size: 1.15rem;
        font-weight: 800;
    }

    /* 참가자 상태 태그 */
    .player-tags {
        display: flex;
        gap: 8px;
        margin-top: 14px;
        flex-wrap: wrap;
    }

    .player-tag {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .sub-tag {
        background: rgba(255, 183, 77, 0.16);
        color: #ffb74d;
        border: 1px solid rgba(255, 183, 77, 0.30);
    }

    .newbie-tag {
        background: rgba(255, 107, 85, 0.16);
        color: #ff7355;
        border: 1px solid rgba(255, 107, 85, 0.30);
    }

    .mobile-tag {
        background: rgba(98, 214, 245, 0.14);
        color: #62d6f5;
        border: 1px solid rgba(98, 214, 245, 0.28);
    }

    .team-card {
        background: rgba(21, 33, 39, 0.78);
        border: 1px solid rgba(150, 190, 200, 0.16);
        border-radius: 18px;
        padding: 18px 20px;
        backdrop-filter: blur(10px);
    }

    .team-card-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 14px;
    }

    .team-member {
        display: flex;
        justify-content: space-between;
        padding: 6px 0;
        color: #f5f7f7;
    }

    .team-job {
        color: #9fb2b8;
        font-size: 0.9rem;
    }

    .team-card-divider {
        height: 1px;
        background: rgba(255, 255, 255, 0.08);
        margin: 14px 0;
    }

    .team-stat {
        display: flex;
        justify-content: space-between;
        padding: 5px 0;
        color: #b7c4c8;
    }

    .team-stat strong {
        color: #ffffff;
    }

    .team-final {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 6px;
    }

    .team-final span {
        color: #cbd6d9;
        font-weight: 700;
    }

    .team-final strong {
        color: #ff7355;
        font-size: 1.35rem;
    }
    
    /* 추천안 제목 */
    .recommendation-header {
        margin-top: 26px;
        margin-bottom: 18px;
    }

    .recommendation-number {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 800;
    }

    .recommendation-description {
        color: #9fb2b8;
        font-size: 0.9rem;
        margin-top: 4px;
    }


    /* 두 팀 평균 전투력 차이 */
    .difference-card {
        margin-top: 18px;
        margin-bottom: 16px;
        padding: 16px 20px;

        background:
            linear-gradient(
                135deg,
                rgba(32, 57, 67, 0.82),
                rgba(21, 38, 45, 0.82)
            );

        border: 1px solid rgba(98, 214, 245, 0.22);
        border-radius: 16px;

        display: flex;
        justify-content: space-between;
        align-items: center;

        backdrop-filter: blur(10px);
    }

    .difference-label {
        color: #b9c9cd;
        font-size: 0.95rem;
        font-weight: 600;
    }

    .difference-value {
        color: #62d6f5;
        font-size: 1.7rem;
        font-weight: 900;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="guild-header">
        <div class="guild-name">장난감 길드</div>
        <div class="raid-title">레이드 준비실</div>
        <div class="raid-description">
            이번 주 출정 인원을 등록하고 팀을 편성해보세요!
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 참가자 목록이 아직 없으면 빈 리스트 만들기
if "players" not in st.session_state:
    st.session_state.players = []

if "current_step" not in st.session_state:
    st.session_state.current_step = 1

# 현재 수정 중인 참가자 기억하기
if "editing_index" not in st.session_state:
    st.session_state.editing_index = None

if st.session_state.current_step == 1:
    with st.container(border=True):
        st.subheader("참가자 등록")

        if st.session_state.editing_index is not None:
            editing_player = st.session_state.players[
                st.session_state.editing_index
            ]
        else:
            editing_player = None

        name = st.text_input(
            "닉네임",
            value=editing_player["name"] if editing_player else ""
        )

        st.caption("※ 아키/레키님은 본캐로 참가하는 경우 아키이즈/레키나로 기입해주세요.")
        st.caption("※ 리지님은 본캐/부캐 상관없이 꼭 '리지'로 기입해주세요.")

        combat_power = st.number_input(
            "전투력",
            min_value=0.0,
            step=0.01,
            format="%.2f",
            value=editing_player["combat_power"] if editing_player else 0.0
        )

        job_list = [
            "사제", "전사", "마법사", "수도사",
            "장궁병", "듀얼블레이드", "대검전사", "검술사",
            "기사", "궁수", "석궁사수", "빙결술사",
            "화염술사", "전격술사", "힐러", "암흑술사",
            "도적", "격투가", "음유시인", "악사", "댄서"
        ]

        job_index = 0

        if editing_player:
            job_index = job_list.index(editing_player["job"])

        job = st.selectbox(
            "직업",
            job_list,
            index=job_index
        )

        magic_resistance = st.number_input(
            "마도저항",
            min_value=0,
            step=1,
            value=editing_player["magic_resistance"] if editing_player else 0
        )

        is_sub = st.checkbox(
            "부캐",
            value=editing_player["is_sub"] if editing_player else False
        )

        is_newbie = st.checkbox(
            "뉴비",
            value=editing_player["is_newbie"] if editing_player else False
        )

        is_mobile = st.checkbox(
            "모바일",
            value=editing_player["is_mobile"] if editing_player else False
        )

        button_text = (
            "수정 저장"
            if st.session_state.editing_index is not None
            else "참가자 추가"
        )

        if st.button(button_text):

            cleaned_name = name.strip()

            # 닉네임을 입력하지 않은 경우
            if cleaned_name == "":
                st.warning("닉네임을 입력해주세요.")

            # 다른 참가자와 닉네임이 중복되는 경우
            elif any(
                player["name"] == cleaned_name
                and index != st.session_state.editing_index
                for index, player in enumerate(st.session_state.players)
            ):
                st.warning("이미 등록된 참가자입니다.")

            else:
                player_data = {
                    "name": cleaned_name,
                    "combat_power": combat_power,
                    "job": job,
                    "magic_resistance": magic_resistance,
                    "is_sub": is_sub,
                    "is_newbie": is_newbie,
                    "is_mobile": is_mobile
                }

                # 새 참가자 추가
                if st.session_state.editing_index is None:
                    st.session_state.players.append(player_data)
                    st.success(f"{cleaned_name} 참가자가 추가되었습니다.")

                # 기존 참가자 수정
                else:
                    st.session_state.players[
                        st.session_state.editing_index
                    ] = player_data

                    st.session_state.editing_index = None

                    st.success(f"{cleaned_name} 참가자 정보가 수정되었습니다.")
                    st.rerun()

        if st.session_state.editing_index is not None:
            if st.button("수정 취소"):
                st.session_state.editing_index = None
                st.rerun()

    st.subheader("참가자 목록")

    if st.session_state.editing_index is not None:
        editing_player = st.session_state.players[
            st.session_state.editing_index
        ]
    else:
        editing_player = None

    for index, player in enumerate(st.session_state.players):
        col1, col2 = st.columns([5, 1])

        with col1:
            tags = ""

            if player["is_sub"]:
                tags += '<span class="player-tag sub-tag">부캐</span>'

            if player["is_newbie"]:
                tags += '<span class="player-tag newbie-tag">뉴비</span>'

            if player["is_mobile"]:
                tags += '<span class="player-tag mobile-tag">모바일</span>'

            player_card = (
                f'<div class="player-card">'
                f'<div class="player-card-top">'
                f'<span class="player-name">{player["name"]}</span>'
                f'<span class="player-job">{player["job"]}</span>'
                f'</div>'
                f'<div class="player-stats">'
                f'<div>'
                f'<span class="stat-label">전투력</span>'
                f'<span class="combat-power">{player["combat_power"]:.2f}</span>'
                f'</div>'
                f'<div>'
                f'<span class="stat-label">마도저항</span>'
                f'<span class="magic-resistance">{player["magic_resistance"]:,}</span>'
                f'</div>'
                f'</div>'
                f'<div class="player-tags">{tags}</div>'
                f'</div>'
            )

            st.markdown(player_card, unsafe_allow_html=True)

        with col2:
            if st.button("수정", key=f"edit_{index}"):
                st.session_state.editing_index = index
                st.rerun()

            if st.button("삭제", key=f"delete_{index}"):
                st.session_state.players.pop(index)
                st.rerun()   

    st.divider()

    st.subheader("명단 저장")

    st.info(
        "💡 지난 참가자 명단을 불러온 뒤, 이번 주에 맞게 수정해서 사용할 수 있어요.\n\n"
        "불참자는 삭제하고 전투력·마도저항은 '수정'으로 변경한 뒤, "
        "새로운 명단 이름으로 저장해주세요."
    )

    list_name = st.text_input(
        "명단 이름",
        placeholder="예: 8월 2주차 레이드"
    )

    if st.button("현재 명단 저장"):
        if list_name.strip() == "":
            st.warning("명단 이름을 입력해주세요.")

        elif len(st.session_state.players) == 0:
            st.warning("저장할 참가자가 없습니다.")

        else:
            save_data = {
                "list_name": list_name.strip(),
                "players": st.session_state.players
            }

            supabase.table("raid_lists").insert(
                save_data
            ).execute()

            st.success(
                f"'{list_name.strip()}' 명단을 저장했습니다."
            )

    saved_lists_response = (
        supabase
        .table("raid_lists")
        .select("id, list_name, created_at")
        .order("created_at", desc=True)
        .execute()
    )

    saved_lists = saved_lists_response.data

    st.subheader("저장된 명단")

    st.caption(
        "지난 명단을 선택해 불러오면 참가자 목록에 적용됩니다."
    )

    if len(saved_lists) == 0:
        st.info("저장된 명단이 없습니다.")

    else:
        saved_list_names = [
            saved_list["list_name"]
            for saved_list in saved_lists
        ]

        selected_list_name = st.selectbox(
            "불러올 명단",
            saved_list_names
        )

        if st.button("선택한 명단 불러오기"):
            selected_list = next(
                saved_list
                for saved_list in saved_lists
                if saved_list["list_name"] == selected_list_name
            )

            selected_id = selected_list["id"]

            response = (
                supabase
                .table("raid_lists")
                .select("players")
                .eq("id", selected_id)
                .single()
                .execute()
            )

            st.session_state.players = response.data["players"]

            st.session_state.editing_index = None

            st.success(
                f"'{selected_list_name}' 명단을 불러왔습니다."
            )

            st.rerun()

if st.button("팀 추천하기"):
    if len(st.session_state.players) < 2:
        st.warning("팀 편성을 위해 참가자를 2명 이상 등록해주세요.")

    else:
        recommendations = make_team_recommendations(
            st.session_state.players
        )
        st.session_state.recommendations = recommendations
        st.session_state.current_step = 2
        st.rerun()

if st.session_state.current_step == 2: 

    if st.button("← 이전", key="back_to_players"):
        st.session_state.current_step = 1
        st.rerun()       

    if "recommendations" in st.session_state:
        recommendations = st.session_state.recommendations 

        if len(recommendations) == 0:
            st.warning("추천 가능한 팀 조합을 찾지 못했습니다.")

        else:
            for index, result in enumerate(recommendations, start=1):
                st.markdown(
                    f"""
                    <div class="recommendation-header">
                        <div class="recommendation-number">추천안 {index}</div>
                        <div class="recommendation-description">
                            균형 점수가 좋은 편성입니다.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                col_a, col_b = st.columns(2)

                with col_a:
                    team_a_names = ""

                    for player in result["team_a"]:
                        team_a_names += (
                            f'<div class="team-member">'
                            f'<span>{player["name"]}</span>'
                            f'<span class="team-job">{player["job"]}</span>'
                            f'</div>'
                        )

                    team_a_card = (
                        f'<div class="team-card">'
                        f'<div class="team-card-title">A팀</div>'
                        f'{team_a_names}'
                        f'<div class="team-card-divider"></div>'
                        f'<div class="team-stat"><span>MR 반영 평균 전투력</span>'
                        f'<strong>{get_team_average(result["team_a"]):.2f}</strong></div>'
                        f'<div class="team-stat"><span>직업 보너스</span>'
                        f'<strong>{get_team_job_bonus(result["team_a"]):+.2f}</strong></div>'
                        f'<div class="team-stat"><span>특수 캐릭터 보너스</span>'
                        f'<strong>{get_team_special_bonus(result["team_a"]):+.2f}</strong></div>'
                        f'<div class="team-stat"><span>부캐/뉴비/모바일 보정</span>'
                        f'<strong>{get_team_player_penalty(result["team_a"]):+.2f}</strong></div>'
                        f'<div class="team-card-divider"></div>'
                        f'<div class="team-final">'
                        f'<span>팀 평균 전투력</span>'
                        f'<strong>{result["team_a_score"]:.2f}</strong>'
                        f'</div>'
                        f'</div>'
                    )

                    st.markdown(team_a_card, unsafe_allow_html=True)

                with col_b:
                    team_b_names = ""

                    for player in result["team_b"]:
                        team_b_names += (
                            f'<div class="team-member">'
                            f'<span>{player["name"]}</span>'
                            f'<span class="team-job">{player["job"]}</span>'
                            f'</div>'
                        )

                    team_b_card = (
                        f'<div class="team-card">'
                        f'<div class="team-card-title">B팀</div>'
                        f'{team_b_names}'
                        f'<div class="team-card-divider"></div>'
                        f'<div class="team-stat"><span>MR 반영 평균 전투력</span>'
                        f'<strong>{get_team_average(result["team_b"]):.2f}</strong></div>'
                        f'<div class="team-stat"><span>직업 보너스</span>'
                        f'<strong>{get_team_job_bonus(result["team_b"]):+.2f}</strong></div>'
                        f'<div class="team-stat"><span>특수 캐릭터 보너스</span>'
                        f'<strong>{get_team_special_bonus(result["team_b"]):+.2f}</strong></div>'
                        f'<div class="team-stat"><span>부캐/뉴비/모바일 보정</span>'
                        f'<strong>{get_team_player_penalty(result["team_b"]):+.2f}</strong></div>'
                        f'<div class="team-card-divider"></div>'
                        f'<div class="team-final">'
                        f'<span>팀 평균 전투력</span>'
                        f'<strong>{result["team_b_score"]:.2f}</strong>'
                        f'</div>'
                        f'</div>'
                    )

                    st.markdown(team_b_card, unsafe_allow_html=True)


                difference_card = (
                    f'<div class="difference-card">'
                    f'<div class="difference-label">두 팀 평균 전투력 차이</div>'
                    f'<div class="difference-value">{result["score_difference"]:.2f}</div>'
                    f'</div>'
                )

                st.markdown(difference_card, unsafe_allow_html=True)

                if st.button(
                    f"추천안 {index}으로 편집하기",
                    key=f"select_recommendation_{index}"
                ):
                    st.session_state.final_team_a = result["team_a"].copy()
                    st.session_state.final_team_b = result["team_b"].copy()
                    st.session_state.selected_recommendation = index

                    st.session_state.current_step = 3
                    st.rerun()


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

if st.session_state.current_step == 3:

    if st.button("← 이전", key="back_to_recommendations"):
        st.session_state.current_step = 2
        st.rerun()

    if "final_team_a" in st.session_state and "final_team_b" in st.session_state:
        st.subheader("⚔️ 최종 편성")

        st.caption(
            f"추천안 {st.session_state.selected_recommendation}을 기준으로 편집 중"
        )

        final_col_a, final_col_b = st.columns(2)

        with final_col_a:
            st.markdown("### A팀")

            for player in st.session_state.final_team_a:
                st.write(f'{player["name"]} / {player["job"]}')

            selected_a = st.selectbox(
                "A팀에서 이동할 사람",
                [player["name"] for player in st.session_state.final_team_a],
                key="move_from_a"
            )

            if st.button("A → B 이동"):
                player_to_move = next(
                    player
                    for player in st.session_state.final_team_a
                    if player["name"] == selected_a
                )

                st.session_state.final_team_a.remove(player_to_move)
                st.session_state.final_team_b.append(player_to_move)

                st.rerun()

        with final_col_b:
            st.markdown("### B팀")

            for player in st.session_state.final_team_b:
                st.write(f'{player["name"]} / {player["job"]}')

            selected_b = st.selectbox(
                "B팀에서 이동할 사람",
                [player["name"] for player in st.session_state.final_team_b],
                key="move_from_b"
            )

            if st.button("B → A 이동"):
                player_to_move = next(
                    player
                    for player in st.session_state.final_team_b
                    if player["name"] == selected_b
                )

                st.session_state.final_team_b.remove(player_to_move)
                st.session_state.final_team_a.append(player_to_move)

                st.rerun()

        final_a_average = get_team_average(st.session_state.final_team_a)
        final_b_average = get_team_average(st.session_state.final_team_b)

        final_a_job_bonus = get_team_job_bonus(st.session_state.final_team_a)
        final_b_job_bonus = get_team_job_bonus(st.session_state.final_team_b)

        final_a_special_bonus = get_team_special_bonus(st.session_state.final_team_a)
        final_b_special_bonus = get_team_special_bonus(st.session_state.final_team_b)

        final_a_penalty = get_team_player_penalty(st.session_state.final_team_a)
        final_b_penalty = get_team_player_penalty(st.session_state.final_team_b)

        final_a_score = (
            final_a_average
            + final_a_job_bonus
            + final_a_special_bonus
            + final_a_penalty
        )

        final_b_score = (
            final_b_average
            + final_b_job_bonus
            + final_b_special_bonus
            + final_b_penalty
        )

        final_score_difference = abs(final_a_score - final_b_score)

        selected_index = st.session_state.selected_recommendation - 1

        original_recommendation = st.session_state.recommendations[selected_index]

        original_score_difference = original_recommendation["score_difference"]

        difference_change = original_score_difference - final_score_difference

        st.markdown("### 📊 최종 편성 계산")

        result_col_a, result_col_b = st.columns(2)

        with result_col_a:
            st.write(f"A팀 평균 전투력: {final_a_average:.2f}")
            st.write(f"A팀 직업 보너스: {final_a_job_bonus:+.2f}")
            st.write(f"A팀 특수 보너스: {final_a_special_bonus:+.2f}")
            st.write(f"A팀 부캐/뉴비 보정: {final_a_penalty:+.2f}")
            st.write(f"**A팀 최종 점수: {final_a_score:.2f}**")

        with result_col_b:
            st.write(f"B팀 평균 전투력: {final_b_average:.2f}")
            st.write(f"B팀 직업 보너스: {final_b_job_bonus:+.2f}")
            st.write(f"B팀 특수 보너스: {final_b_special_bonus:+.2f}")
            st.write(f"B팀 부캐/뉴비 보정: {final_b_penalty:+.2f}")
            st.write(f"**B팀 최종 점수: {final_b_score:.2f}**")

        st.metric(
            "두 팀 최종 점수 차이",
            f"{final_score_difference:.2f}"
        )

        st.markdown("### 🔄 원래 추천안과 비교")

        compare_col_1, compare_col_2 = st.columns(2)

        with compare_col_1:
            st.metric(
                "원래 추천안 점수 차이",
                f"{original_score_difference:.2f}"
            )

        with compare_col_2:
            st.metric(
                "현재 최종안 점수 차이",
                f"{final_score_difference:.2f}"
            )

        if difference_change > 0:
            st.success(
                f"균형 차이가 {difference_change:.2f} 줄었습니다."
            )

        elif difference_change < 0:
            st.warning(
                f"균형 차이가 {abs(difference_change):.2f} 늘었습니다."
            )

        else:
            st.info("원래 추천안과 현재 최종안의 균형 차이가 같습니다.")

if st.button("✅ 이 편성으로 확정", type="primary"):
    st.session_state.confirmed_team_a = (
        st.session_state.final_team_a.copy()
    )
    st.session_state.confirmed_team_b = (
        st.session_state.final_team_b.copy()
    )
    st.session_state.team_confirmed = True

    st.session_state.current_step = 4
    st.rerun()

if st.session_state.current_step == 4:

    if st.button("← 이전", key="back_to_final_team"):
        st.session_state.current_step = 3
        st.rerun()

    if st.session_state.get("team_confirmed", False):
        st.success("최종 편성이 확정되었습니다! 레이드 결과를 입력해주세요.")

        st.markdown("### 🏁 레이드 결과 입력")

        result_a_col, result_b_col = st.columns(2)

        with result_a_col:
            st.markdown("#### A팀")

            a_clear_time = st.number_input(
                "A팀 클리어 시간(초)",
                min_value=0,
                step=1,
                key="a_clear_time"
            )

            a_team_names = [
                player["name"]
                for player in st.session_state.confirmed_team_a
            ]

            a_rank_1 = st.selectbox(
                "A팀 1등",
                a_team_names,
                key="a_rank_1"
            )

            a_rank_2 = st.selectbox(
                "A팀 2등",
                a_team_names,
                key="a_rank_2"
            )

            a_rank_3 = st.selectbox(
                "A팀 3등",
                a_team_names,
                key="a_rank_3"
            )

        with result_b_col:
            st.markdown("#### B팀")

            b_clear_time = st.number_input(
                "B팀 클리어 시간(초)",
                min_value=0,
                step=1,
                key="b_clear_time"
            )

            b_team_names = [
                player["name"]
                for player in st.session_state.confirmed_team_b
            ]

            b_rank_1 = st.selectbox(
                "B팀 1등",
                b_team_names,
                key="b_rank_1"
            )

            b_rank_2 = st.selectbox(
                "B팀 2등",
                b_team_names,
                key="b_rank_2"
            )

            b_rank_3 = st.selectbox(
                "B팀 3등",
                b_team_names,
                key="b_rank_3"
            )

        can_save_result = True

        a_ranks = [a_rank_1, a_rank_2, a_rank_3]
        b_ranks = [b_rank_1, b_rank_2, b_rank_3]

        a_has_duplicate = len(set(a_ranks)) < len(a_ranks)
        b_has_duplicate = len(set(b_ranks)) < len(b_ranks)

        if a_has_duplicate:
            st.warning("A팀 1·2·3등에 같은 사람이 중복 선택되었습니다.")

        if b_has_duplicate:
            st.warning("B팀 1·2·3등에 같은 사람이 중복 선택되었습니다.")


        if a_clear_time <= 0 or b_clear_time <= 0:
            st.warning("A팀과 B팀의 클리어 시간을 입력해주세요.")
            can_save_result = False

        if a_has_duplicate or b_has_duplicate:
            can_save_result = False

        if st.button(
            "💾 레이드 결과 저장",
            type="primary",
            disabled=not can_save_result
        ):
            raid_data = {
            "raid_date": str(date.today()),
            "a_clear_time": int(a_clear_time),
            "b_clear_time": int(b_clear_time),
        }

            response = (
                supabase
                .table("official_raid")
                .insert(raid_data)
                .execute()
            )

            raid_id = response.data[0]["id"]

            player_records = []

            for player in st.session_state.confirmed_team_a:
                player_rank = None

                if player["name"] == a_rank_1:
                    player_rank = 1
                elif player["name"] == a_rank_2:
                    player_rank = 2
                elif player["name"] == a_rank_3:
                    player_rank = 3

                player_records.append({
                    "raid_id": raid_id,
                    "team": "A",
                    "player_name": player["name"],
                    "rank": player_rank,
                })

            for player in st.session_state.confirmed_team_b:
                player_rank = None

                if player["name"] == b_rank_1:
                    player_rank = 1
                elif player["name"] == b_rank_2:
                    player_rank = 2
                elif player["name"] == b_rank_3:
                    player_rank = 3

                player_records.append({
                    "raid_id": raid_id,
                    "team": "B",
                    "player_name": player["name"],
                    "rank": player_rank,
                })

            players_response = (
                supabase
                .table("official_raid_players")
                .insert(player_records)
                .execute()
            )

            st.write(player_records)

            st.write(response)
