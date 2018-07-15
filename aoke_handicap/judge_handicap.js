// 使用利记亚盘页面
// 变化限制时间180min
// 最小截至时间8hour, 最大截至时间48h
// 临界概率变化0.03
// 取截至时间前的最新值
// support_direction：0为主队盘口，1为客队盘口

function convert_handicap(handicap_name) {
    handicap_name_dict = {
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
    };
    return handicap_name_dict[handicap_name]
}

function isInArray(arr,val){
　　var testStr=','+arr.join(",")+",";
　　return testStr.indexOf(","+val+",")!=-1;
}

function compute_result() {
	limit_time = 180;
	min_time = 480;
	max_time = 2880;
	limit_pro = 0.02;
	result_arr = [];
	first_table = $('table').eq(0);
	// 先存储所有时间
	all_time_arr = [];
	first_table.find('tr:not(.titlebg)').each(function () {
		var first_tr = $(this);
		if (first_tr.find('td').length === 0){
				return true
		}
		cur_hour = parseInt(first_tr.find('td').eq(1).text().split('赛前')[1].split('时')[0]);
		cur_minute = parseInt(first_tr.find('td').eq(1).text().split('赛前')[1].split('时')[1].split('分')[0]);
		cur_time = cur_hour * 60 + cur_minute;
		all_time_arr.push(cur_time);
    });
	table_index = 0;
	$('.ahChangeTable').each(function(){
		index = 0;
		prev_home_pro = '-';
		var table = $(this);
		table.find('tr:not(.titlebg)').each(function(){
			var tr = $(this);
			if (tr.find('td').length === 0 || $.trim(tr.find('td').eq(0).text()) === '-'){
				index += 1;
				return true
			}
			if (first_table.find('tr:not(.titlebg)').eq(index).find('td').eq(1).text().split('赛前')[1] === undefined){
                return true
            }
			cur_hour = parseInt(first_table.find('tr:not(.titlebg)').eq(index).find('td').eq(1).text().split('赛前')[1].split('时')[0]);
			cur_minute = parseInt(first_table.find('tr:not(.titlebg)').eq(index).find('td').eq(1).text().split('赛前')[1].split('时')[1].split('分')[0]);
			cur_time = (cur_hour*60+cur_minute);
			need_analysis_time_arr = [];
			// 去总时间数组中遍历得到小于当前时间，大于等于(当前时间-limit_time)的index
			for(i = 0; i < all_time_arr.length; i++){
				if (all_time_arr[i] < cur_time && all_time_arr[i] >= (cur_time-limit_time)){
					need_analysis_time_arr.push(i)
				}
			}

			cur_odd_home = parseFloat($.trim(tr.find('td').eq(0).text()));
			cur_odd_away = parseFloat($.trim(tr.find('td').eq(1).text()));
			return_rate = parseFloat((cur_odd_home*cur_odd_away/(cur_odd_home + cur_odd_away)).toFixed(3));
			home_pro = parseFloat((return_rate/cur_odd_home) .toFixed(3));
			cur_handicap_num = convert_handicap(($.trim(table.find('tr.tableh').eq(0).text())));
			current_table_trs = $('.ahChangeTable').eq(table_index).find('tr:not(.titlebg)');
			for(i = 0; i < need_analysis_time_arr.length; i++){
				need_analysis_tr = current_table_trs.eq(need_analysis_time_arr[i] + 1);
				need_analysis_odd_home = parseFloat($.trim(need_analysis_tr.find('td').eq(0).text()));
				need_analysis_odd_away = parseFloat($.trim(need_analysis_tr.find('td').eq(1).text()));
				need_analysis_return_rate = parseFloat((need_analysis_odd_home*need_analysis_odd_away/(need_analysis_odd_home + need_analysis_odd_away)).toFixed(3));
				need_analysis_home_pro = parseFloat((need_analysis_return_rate/need_analysis_odd_home) .toFixed(3));
				if (Math.abs(need_analysis_home_pro - home_pro) > limit_pro){
					pro_change = parseFloat((need_analysis_home_pro - home_pro).toFixed(3));
					if (pro_change > 0){
						cur_info = {
							'cur_time': cur_time,
							'last_time': all_time_arr[need_analysis_time_arr[i]],
							'cur_handicap_num': cur_handicap_num,
							'pro_change': pro_change,
							'support_direction': 0
						};
						result_times = [];
						for (j in result_arr){
							result_times.push(result_arr[j]['cur_time'])
						}
						if (all_time_arr[need_analysis_time_arr[i]] >= min_time && all_time_arr[need_analysis_time_arr[i]] <= max_time){
							if (result_times.length === 0){
								if (!isInArray(result_times, cur_time)){
									result_arr.push(cur_info)
								}
							} else {
								if (cur_time > result_times[0]){
									result_arr = [cur_info]
								}
							}
						}
					} else {
						cur_info = {
							'cur_time': cur_time,
							'last_time': all_time_arr[need_analysis_time_arr[i]],
							'cur_handicap_num': cur_handicap_num,
							'pro_change': pro_change,
							'support_direction': 1
						};
						result_times = [];
						for (j in result_arr){
							result_times.push(result_arr[j]['cur_time'])
						}
						if (all_time_arr[need_analysis_time_arr[i]] >= min_time && all_time_arr[need_analysis_time_arr[i]] <= max_time) {
                            if (result_times.length === 0) {
                                if (!isInArray(result_times, cur_time)) {
                                    result_arr.push(cur_info)
                                }
                            } else {
                                if (cur_time > result_times[0]) {
                                    result_arr = [cur_info]
                                }
                            }
                        }
					}
				}
			}
			index += 1
		});
		table_index += 1
	});
	return result_arr[0];
}
compute_result();

