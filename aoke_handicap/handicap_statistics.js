function convert_handicap(handicap_name) {
    handicap_name_dict = {
        '受四球': -4,
        '受三球半/四球': -3.75,
        '受三球半': -3.5,
        '受三球/三球半': -3.25,
        '受三球': -3,
        '受两球半/三球': -2.75,
        '受两球半': -2.5,
        '受两球/两球半': -2.25,
        '受两球': -2,
        '受球半/两球': -1.75,
        '受球半': -1.5,
        '受一球/球半': -1.25,
        '受一球': -1,
        '受半球/一球': -0.75,
        '受半球': -0.5,
        '受平手/半球': -0.25,
        '平手': 0,
        '平手/半球': 0.25,
        '半球': 0.5,
        '半球/一球': 0.75,
        '一球': 1,
        '一球/球半': 1.25,
        '球半': 1.5,
        '球半/两球': 1.75,
        '两球': 2,
        '两球/两球半': 2.25,
        '两球半': 2.5,
        '两球半/三': 2.75,
        '三球': 3,
        '三球/三球半': 3.25,
        '三球半': 3.5,
        '三球半/四球': 3.75,
        '四球': 4,
    };
    return handicap_name_dict[handicap_name]
}

function compute_result() {
	limit_time_arr = [600, 900, 1200];
	limit_time_arr_record = [0, 0, 0];
	all_handicap_dict = {};
	pre_home_odd = 0;
	pre_away_odd = 0;
	pre_handicap_num = 0;
	$('table:not(.ahChangeTable) tr:not(.titlebg').each(function(){
			var tr = $(this);
			if (tr.find('td').length === 0){
				return true;
			}
			cur_hour = parseInt(tr.find('td').eq(1).text().split('赛前')[1].split('时')[0]);
			cur_minute = parseInt(tr.find('td').eq(1).text().split('赛前')[1].split('时')[1].split('分')[0]);
			cur_time = cur_hour * 60 + cur_minute;
			if (tr.find('td').eq(2).children('span').eq(0).children('span').length === 0){
				home_odd = parseFloat(tr.find('td').eq(2).children('span').text().substr(0, 4));
			} else {
				home_odd = parseFloat(tr.find('td').eq(2).children('span').eq(0).children('span').text().substr(0, 4));
			}
			if (tr.find('td').eq(4).children('span').eq(0).children('span').length === 0){
				away_odd = parseFloat(tr.find('td').eq(4).children('span').text().substr(0, 4));
			} else {
				away_odd = parseFloat(tr.find('td').eq(4).children('span').eq(0).children('span').text().substr(0, 4));
			}
			handicap_num = convert_handicap(tr.find('td').eq(3).text());		// 盘口大小
			if (cur_time > limit_time_arr[0] && limit_time_arr_record[0] === 0){
				all_handicap_dict['600'] = {};
				all_handicap_dict['600']['home_odd'] = pre_home_odd;
				all_handicap_dict['600']['away_odd'] = pre_away_odd;
				all_handicap_dict['600']['handicap_num'] = pre_handicap_num;
				limit_time_arr_record[0] = 1
			}
			if (cur_time > limit_time_arr[1] && limit_time_arr_record[1] === 0){
				all_handicap_dict['900'] = {};
				all_handicap_dict['900']['home_odd'] = pre_home_odd;
				all_handicap_dict['900']['away_odd'] = pre_away_odd;
				all_handicap_dict['900']['handicap_num'] = pre_handicap_num;
				limit_time_arr_record[1] = 1
			}
			if (cur_time > limit_time_arr[2] && limit_time_arr_record[2] === 0){
				all_handicap_dict['1200'] = {};
				all_handicap_dict['1200']['home_odd'] = pre_home_odd;
				all_handicap_dict['1200']['away_odd'] = pre_away_odd;
				all_handicap_dict['1200']['handicap_num'] = pre_handicap_num;
				limit_time_arr_record[2] = 1
			}
			pre_home_odd = home_odd;
			pre_away_odd = away_odd;
			pre_handicap_num = handicap_num;
	});
	// 找出最多的盘口
	return all_handicap_dict;
}
compute_result();

