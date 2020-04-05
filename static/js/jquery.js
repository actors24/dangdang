/*
 * imgMask
 * ����jQuery����չ��ʵ��һ�������¶����Ԫ��͸�����ɰ�Ч��
 * ���÷�ʽ��obj.imgMask(options);
 * ����˵����opacity������ƶ���֮����ɰ�͸���ȣ���Χ��0-1��Ĭ�ϡ�0.3��
 *           html_element����Ԫ�ص�html������Ĭ���ǡ�div��
 * �����ߣ����
 * �汾��0.1
 * ������ʱ�� 2012��3��22�� 14:21:57
 */
(function($){
    var ver = 0.1;
    /*
     * make_mask
     * �����ɰ����
     * obj��Ҫ�����ɰ�Ķ���
     * settings,����
     */
    function make_mask(obj,settings){
        obj.children().each(function(){
            var o = $(this);
            var a = o.children();
            var mask = $("<div></div>");
            mask.css({
                width:function(){
                    return o.css("width");
                },
                height:function(){
                    return o.css("height");
                },
                top:"0px",
                left:"0px",
                background:'#000',
                opacity:'0',
                position:'absolute',
                display:'block',
                overflow:'hidden',
                filter:'alpha(opacity=0)',
                cursor:'pointer'
            });

            mask.appendTo(o);
            bind(mask,settings);
        });
        
        obj.bind("mouseout",function(){
            $(this).children().find("div").css("opacity","0");
        });
    }
    /*
     * bind
     * ���ɰ��¼�
     * mask,�ɰ����
     * settings������
     */
    function bind(mask,settings){
        mask.bind("mouseover",function(){
            $(mask.parents(settings.html_element)[0]).siblings().find("div").css("opacity",settings.opacity);
            mask.css("opacity","0");
        });
    };

    $.fn.imgMask = function(options){
        if(this.children().length<2)
            return this;
        var settings = {
            opacity:'0.3',
            html_element:'a'
        };
        if(options){
            $.extend(settings,options);
        }
        make_mask(this,settings);
        return this;
    };
    $.fn.imgMask.ver = function(){
        return ver;
    };
})
