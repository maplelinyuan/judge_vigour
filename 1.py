if time_1200_handicap_difference == 0:
    if time_1200_home_odd_difference - time_1200_away_odd_difference < 0:
        if handicap_result > 0.25:
            total_point += 1
            total_right += 1
        elif handicap_result > 0:
            total_point += 0.5
            total_right += 1
        elif handicap_result == 0:
            pass
        else:
            total_point -= 1
        total_num += 1
    elif time_1200_home_odd_difference - time_1200_away_odd_difference > 0:
        if handicap_result < -0.25:
            total_point += 1
            total_right += 1
        elif handicap_result < 0:
            total_point += 0.5
            total_right += 1
        elif handicap_result == 0:
            pass
        else:
            total_point -= 1
        total_num += 1