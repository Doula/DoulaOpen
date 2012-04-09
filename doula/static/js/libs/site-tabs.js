SM.SideTab = {

    //SPECIAL PROPERTIES
    __NAME:"sideTab",
    __init:function(){
        var width,
            height,
            right;

        this.$el
            .css("display","block")
            .appendTo(document.body);

        width = this.$el.outerWidth();
        height = this.$el.outerHeight();

        if($.browser.msie && $.browser.version === "8.0"){
            right = -1 * ((height-width));
        } else if($.browser.msie && $.browser.version === "7.0"){
            right = 0;
        }else{
            right = -1 * ((width-height)/2);
        }

        this.$el.css("right",right);

    }
};

SM.Views.register(SM.SideTab);