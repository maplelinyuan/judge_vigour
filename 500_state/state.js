home_rate = 0;
away_rate = 0;
$('#team_jiaozhan table tr:not(:hidden)').each(function(){
	this_tr = $(this);
	this_tds = this_tr.find('td');
	if (this_tds.length>0){
		result = this_tds.eq(4).text();
		if(result == '胜'){
			home_rate += 3;
		}  else if(result == '平'){
			home_rate += 1;
			away_rate += 1;
		} else {
			away_rate += 3;
		}
	}
})

count = 0;
$('#zhanji_01 tr:not(:hidden)').each(function(){
	if(count > 5) return false;
	this_tr = $(this);
	this_tds = this_tr.find('td');
	if(this_tds.length>0){
		result = this_tds.eq(5).text();
		if(result == '胜'){
			home_rate += 3;
		}  else if(result == '平'){
			home_rate += 1;
		}
		count += 1;
	}
})

count = 0;
$('#zhanji_00 tr:not(:hidden)').each(function(){
	if(count > 5) return false;
	this_tr = $(this);
	this_tds = this_tr.find('td');
	if(this_tds.length>0){
		result = this_tds.eq(5).text();
		if(result == '胜'){
			away_rate += 3;
		}  else if(result == '平'){
			away_rate += 1;
		}
		count += 1;
	}
})
total_rate = home_rate + away_rate;
home_ratio = (home_rate/total_rate).toFixed(2);
console.log(home_ratio);