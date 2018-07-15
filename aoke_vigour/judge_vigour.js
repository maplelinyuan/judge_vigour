limit_day = 15;     // 限制为limit_day天内的比赛
current_timestamp = new Date('20'+$('#lunci').next().find('p').eq(0).text().replace(/-/g,'/').replace(' ', " ")).getTime()/ 1000;
home_name = $('#matchTeam').find('.qb2_t_1').eq(0).find('div').eq(1).text();
away_name = $('#matchTeam').find('.qb2_t_1').eq(1).find('div').eq(0).text();

// 返回返还率
function compute_returnrate(home_odd, draw_odd, away_odd){
    return parseFloat((home_odd*draw_odd*away_odd/(home_odd*draw_odd + home_odd*away_odd + draw_odd*away_odd)).toFixed(3))
}
// 判断主队赛果
function home_match_result(home_Position, match_result){
    if (match_result === 1){
        return 1
    } else {
         if (home_Position === 0){
            if (match_result === 3){
                return 3;
            } else {
                return 0;
            }
        } else {
             if (match_result === 3){
                return 0;
            } else {
                return 3;
            }
         }
    }
}

// 计算分数
function compute_vigour_change(position, result, home_pro, draw_pro, away_pro, goal_differ) {
    var vigour = 0;
    if (result === 3){
        if (position === 0){
            vigour -= draw_pro*(Math.log(goal_differ)+1);
            vigour -= away_pro*(Math.log(goal_differ)+1);
        } else{
             vigour -= home_pro*(Math.log(goal_differ)+1);
            vigour -= draw_pro*(Math.log(goal_differ)+1);
        }
    } else if(result === 1){
         if (position === 0){
            vigour -= draw_pro/2;
            vigour -= away_pro/2;
        } else{
             vigour -= home_pro/2;
             vigour -= draw_pro/2;
        }
    } else{
         if (position === 0){
            vigour -= away_pro/(Math.log(goal_differ)+1);
        } else{
            vigour -= home_pro/(Math.log(goal_differ)+1);
        }
    }
    return vigour
}

function compute_vigour() {
    // 最终的精力分数
    home_vigour = 0;
    away_vigour = 0;

    is_latest_match = true;
    $('.homecomp tr:not(:hidden)').each(function(){
        cur_tr = $(this);
        if (cur_tr.attr('class') === "titlebg" || cur_tr.attr('class') === "tableh"){
            return true;
        }
        match_timestamp = new Date(cur_tr.find('td').eq(1).find('a').text().replace(/-/g,'/')).getTime()/ 1000;
        if ((current_timestamp - match_timestamp) > limit_day*86400){
            return true;
        }
        differ_day = (current_timestamp - match_timestamp)/86400;       // 距今几天
        multi_num = Math.pow(1.1, -differ_day);        // 分数乘积
        score = cur_tr.find('td').eq(3).text();
        home_goal = parseInt(score.split('-')[0]);
        away_goal = parseInt(score.split('-')[1]);
        goal_differ = Math.abs(home_goal - away_goal);      // 进球差
        match_home_name = cur_tr.find('td').eq(2).find('a').text();
        home_position = (match_home_name === home_name) ? 0 : 1;
        match_result = (home_goal >= away_goal) ? ((home_goal > away_goal) ? 3 : 1) : 0;
        home_result = home_match_result(home_position, match_result);       // 主队该场比赛赛果
        if (match_result === 3){
            home_odd = cur_tr.find('td').eq(6).find('span').text();
        } else {
            home_odd = cur_tr.find('td').eq(6).text();
        }
        if (home_odd === '-' || home_odd === ''){
            return true;
        }
         if (match_result === 1){
            draw_odd = cur_tr.find('td').eq(7).find('span').text();
        } else {
            draw_odd = cur_tr.find('td').eq(7).text();
        }
        if (match_result === 0){
            away_odd = cur_tr.find('td').eq(8).find('span').text();
        } else {
            away_odd = cur_tr.find('td').eq(8).text();
        }
        match_returnrate = compute_returnrate(home_odd, draw_odd, away_odd);
        // console.log(match_returnrate)
        home_pro = match_returnrate/home_odd;
        draw_pro = match_returnrate/draw_odd;
        away_pro = match_returnrate/away_odd;
        home_vigour += multi_num * compute_vigour_change(home_position, home_result, home_pro, draw_pro, away_pro, goal_differ);
        is_latest_match = false
    });
    is_latest_match = true;
    $('.awaycomp tr:not(:hidden)').each(function(){
        cur_tr = $(this);
        if (cur_tr.attr('class') === "titlebg" || cur_tr.attr('class') === "tableh"){
            return true;
        }
        match_timestamp = new Date(cur_tr.find('td').eq(1).find('a').text().replace(/-/g,'/')).getTime()/ 1000;
        if ((current_timestamp - match_timestamp) > limit_day*86400){
            return true;
        }
        differ_day = (current_timestamp - match_timestamp)/86400;       // 距今几天
        multi_num = Math.pow(1.1, -differ_day);        // 分数乘积
        score = cur_tr.find('td').eq(3).text();
        home_goal = parseInt(score.split('-')[0]);
        away_goal = parseInt(score.split('-')[1]);
        goal_differ = Math.abs(home_goal - away_goal);      // 进球差
        match_home_name = cur_tr.find('td').eq(2).find('a').text();
        away_position = (match_home_name === away_name) ? 0 : 1;
        match_result = (home_goal >= away_goal) ? ((home_goal > away_goal) ? 3 : 1) : 0;
        away_result = home_match_result(away_position, match_result);       // 客队该场比赛赛果
        if (match_result === 3){
            home_odd = cur_tr.find('td').eq(6).find('span').text();
        } else {
            home_odd = cur_tr.find('td').eq(6).text();
        }
         if (home_odd === '-' || home_odd === ''){
            return true;
        }
         if (match_result === 1){
            draw_odd = cur_tr.find('td').eq(7).find('span').text();
        } else {
            draw_odd = cur_tr.find('td').eq(7).text();
        }
        if (match_result === 0){
            away_odd = cur_tr.find('td').eq(8).find('span').text();
        } else {
            away_odd = cur_tr.find('td').eq(8).text();
        }
        match_returnrate = compute_returnrate(home_odd, draw_odd, away_odd)
        // console.log(match_returnrate)
        home_pro = match_returnrate/home_odd;
        draw_pro = match_returnrate/draw_odd;
        away_pro = match_returnrate/away_odd;
        away_vigour += multi_num * compute_vigour_change(away_position, away_result, home_pro, draw_pro, away_pro, goal_differ);
        is_latest_match = false
    });
    // console.log(home_vigour.toFixed(3));
    // console.log(away_vigour.toFixed(3));
    // console.log(home_vigour - away_vigour);
    vigour_dict = {
        'vigour_difference' : parseFloat((home_vigour - away_vigour).toFixed(3))
    };
    return vigour_dict
}
compute_vigour();
