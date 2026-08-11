from itertools import combinations
from decimal import Decimal, ROUND_HALF_UP


# =========================
# 규칙 설정
# =========================

TEAM_JOB_BONUS = {
    "사제": 0.3,
    "전사": 0.2,
    "수도사": 0.2,
    "기사": 0.2,
    "빙결술사": 0.2,
    "힐러": 0.4
}

SPECIAL_PLAYER_BONUS = {
    "아키이즈": 0.7,
    "레키나": 0.15,
    "리지": -0.7
}

HEALER_JOBS = [
    "힐러",
    "사제",
    "수도사",
    "음유시인"
]

TANK_JOBS = [
    "전사",
    "빙결술사",
    "기사"
]


# =========================
# 기본 계산 함수
# =========================

def round_2(value):
    return float(
        Decimal(str(value)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )
    )


def get_mr_bonus(magic_resistance):
    if magic_resistance >= 6200:
        return 0.15
    elif magic_resistance >= 5400:
        return 0.10
    elif magic_resistance >= 4400:
        return 0.05
    elif magic_resistance >= 2500:
        return 0
    elif magic_resistance >= 2400:
        return -0.10
    elif magic_resistance >= 2300:
        return -0.15
    elif magic_resistance >= 2200:
        return -0.30
    elif magic_resistance >= 2100:
        return -0.40
    elif magic_resistance >= 2000:
        return -0.45
    elif magic_resistance >= 1900:
        return -0.55
    elif magic_resistance >= 1800:
        return -0.60
    elif magic_resistance >= 1700:
        return -0.70
    elif magic_resistance >= 1600:
        return -0.80
    else:
        return -0.90


def get_adjusted_combat_power(combat_power, magic_resistance):
    mr_bonus = get_mr_bonus(magic_resistance)

    adjusted_combat_power = combat_power * (1 + mr_bonus)

    return round_2(adjusted_combat_power)


# =========================
# 팀 점수 계산
# =========================

def get_team_average(team):
    adjusted_powers = []

    for player in team:
        adjusted_powers.append(
            player["adjusted_combat_power"]
        )

    average_power = sum(adjusted_powers) / len(adjusted_powers)

    return round_2(average_power)


def get_team_job_bonus(team):
    jobs = []

    for player in team:
        jobs.append(player["job"])

    total_bonus = 0

    for job in TEAM_JOB_BONUS:
        if job == "빙결술사":
            continue

        if job in jobs:
            total_bonus += TEAM_JOB_BONUS[job]

    ice_count = jobs.count("빙결술사")

    if ice_count >= 2:
        total_bonus += 0.4
    elif ice_count == 1:
        total_bonus += 0.2

    return round_2(total_bonus)


def get_team_special_bonus(team):
    total_bonus = 0

    for player in team:
        name = player["name"]

        if name in SPECIAL_PLAYER_BONUS:
            total_bonus += SPECIAL_PLAYER_BONUS[name]

    return round_2(total_bonus)


def get_team_player_penalty(team):
    total_penalty = 0

    for player in team:
        if player["is_sub"]:
            total_penalty -= 0.3

        if player["is_newbie"]:
            total_penalty -= 0.7

        if player["is_mobile"]:
            total_penalty -= 0.1

    return round_2(total_penalty)


def get_team_score(team):
    average_power = get_team_average(team)
    job_bonus = get_team_job_bonus(team)
    special_bonus = get_team_special_bonus(team)
    player_penalty = get_team_player_penalty(team)

    team_score = (
        average_power
        + job_bonus
        + special_bonus
        + player_penalty
    )

    return round_2(team_score)


# =========================
# 힐러 / 탱커 분배
# =========================

def count_role_players(team, role_jobs):
    count = 0

    for player in team:
        if player["job"] in role_jobs:
            count += 1

    return count


def is_role_distribution_valid(team_a, team_b):
    healer_a = count_role_players(team_a, HEALER_JOBS)
    healer_b = count_role_players(team_b, HEALER_JOBS)

    tank_a = count_role_players(team_a, TANK_JOBS)
    tank_b = count_role_players(team_b, TANK_JOBS)

    total_healers = healer_a + healer_b
    total_tanks = tank_a + tank_b

    healer_ok = True
    tank_ok = True

    if total_healers >= 2:
        healer_ok = healer_a >= 1 and healer_b >= 1

    if total_tanks >= 2:
        tank_ok = tank_a >= 1 and tank_b >= 1

    return healer_ok and tank_ok

def make_team_recommendations(players):
    # 참가자들의 MR 보정 전투력 계산
    for player in players:
        player["adjusted_combat_power"] = (
            get_adjusted_combat_power(
                player["combat_power"],
                player["magic_resistance"]
            )
        )

    team_size = len(players) // 2

    team_combinations = combinations(
        players,
        team_size
    )

    results = []

    for team_a_tuple in team_combinations:
        team_a = list(team_a_tuple)

        team_b = []

        for player in players:
            if player not in team_a:
                team_b.append(player)

        # 짝수 인원의 A/B 뒤집힌 중복 제거
        if len(team_a) == len(team_b):
            if players[0] not in team_a:
                continue

        # 힐러 / 탱커 몰림 방지
        if not is_role_distribution_valid(team_a, team_b):
            continue

        team_a_score = get_team_score(team_a)
        team_b_score = get_team_score(team_b)

        score_difference = round_2(
            abs(team_a_score - team_b_score)
        )

        results.append({
            "team_a": team_a,
            "team_b": team_b,
            "team_a_score": team_a_score,
            "team_b_score": team_b_score,
            "score_difference": score_difference
        })

    sorted_results = sorted(
        results,
        key=lambda result: result["score_difference"]
    )

    return sorted_results[:3]