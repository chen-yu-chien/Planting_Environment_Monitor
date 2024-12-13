 $(function(){
    var iottalk_url = 'https://class.iottalk.tw';   // 'http://DomainName:port'; or 'https://DomainName';
    var mqtt_url = 'wss://iot.iottalk.tw:8866/mqtts'; // 'ws://IP:port/mqtt'; or 'wss://DomainName:port/mqtts'; 
    var mqtt_user =  'iottalk';
    var mqtt_password = 'iottalk2023';
    var exec_interval = 500;

    var profile = {
	    'dm_name': 'Bulb',          
		'idf_list':[],  // 用變數
		// 'odf_list':[Color_O, Luminance], // "-"要改成"_"
        'odf_list':[Luminance],
		'd_name': 'yc_Bulb',
    };

    var r = 255 ;
    var g = 255;
    var b = 0;
    var lum = 0;

    // function Luminance_I(data){
    //     console.log(data);
    // }

    function draw () {
        var rr = Math.floor((r * lum) / 100);
        var gg = Math.floor((g * lum) / 100);
        var bb = Math.floor((b * lum) / 100);
        $('.bulb-top, .bulb-middle-1, .bulb-middle-2, .bulb-middle-3, .bulb-bottom, .night').css(
            {'background': 'rgb('+ rr +', '+ gg +', '+ bb +')'}
        );
    }

    // function Color_O(data){
    //     r = data[0];
    //     g = data[1];
    //     b = data[2];
    //     draw();
    // }
    
    function Luminance(data){
        console.log("luminance:", data[0]);
        if(data[0] <= 0){
            lum = 0;
        }
        else if(data[0] > 0 && data[0] <= 25){
            lum = 25;
        }
        else if(data[0] > 25 && data[0] <= 50){
            lum = 50;
        }
        else if(data[0] > 50 && data[0] <= 75){
            lum = 75;
        }
        else {
            lum = 99;
        }
        draw();
    }
/*******************************************************************/                
    function sa_init(){
	    console.log(profile.d_name);
		$('.Device_name')[0].innerText = profile.d_name;
	}
    var sa = {
        'sa_init': sa_init,
        'iottalk_url': iottalk_url,
        'mqtt_url': mqtt_url,
        'mqtt_user': mqtt_user,
        'mqtt_password': mqtt_password,
        'exec_interval': exec_interval,
    }; 
    dai(profile, sa);     
});
