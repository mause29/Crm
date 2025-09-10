def award_points(user, action):
    points_map = {
        "add_client": 10,
        "close_deal": 50,
        "send_email": 5
    }
    user.points += points_map.get(action, 0)
    return user.points

def leaderboard(users):
    return sorted(users, key=lambda u: u.points, reverse=True)
