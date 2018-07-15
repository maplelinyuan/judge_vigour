$('#Table3 tr[align="center"]').each(function(){
	get_id = $(this).find('td').eq(9).find('a').eq(0).attr('href')
	get_url = 'LPUSH qiutan_analysis:start_urls http://zq.win007.com' + get_id
	console.log(get_url)
})