SM.Accordion =  {

    //SPECIAL PROPERTIES
    __NAME:"accordion",
    __private:{
        multiOpen:false
    },
    __init:function(){

        this
            ._cacheData()
            ._bindEvents();
    },


    //CONSTANTS
    KEY_ATTR:"data-panel-key",

    //PUBLIC METHODS
    close:function(panelKey){

        var panel;

        if(typeof panelKey !== "string"){
            panelKey = this._getKeyFromIndex(panelKey);
        }

        panel = this._panels[panelKey];

        if(panel && this._openPanels[panel.key]){
           this._close(panel);
        }

        return this;
    },
    open:function(panelKey){
        var panel;

        if(typeof panelKey !== "string"){
            panelKey = this._getKeyFromIndex(panelKey);
        }

        panel = this._panels[panelKey];

        if(panel && !this._openPanels[panel.key]){
            if(!this.__private.multiOpen){
                this._closeOpenPanels();
            }
            this._open(panel);
        }

        return this;
    },


    //PRIVATE PROPERTIES
    _openPanels:undefined,
    _panels:undefined,


   //PRIVATE METHODS
    _close:function(panel){
        panel.$panel.find(".accordion-arrow").removeClass("open");
        this.__trigger({type:"beforeClose", index:panel.index, id:panel.key});
        this._openPanels[panel.key] = false;
        panel.$section.animate({height:0}, 200, this._onClose);
    },
    _open:function(panel){
        var height;

        panel.$panel.find(".accordion-arrow").addClass("open");
        this.__trigger({type:"beforeOpen", index:panel.index, id:panel.key});

        this._openPanels[panel.key] = true;

        if(!this.$el.hasClass("static")){
            //temporarily set the div height to auto, record its height and
            //reset its height to zeror and animate its auto height
            height = panel.$section.css("height", "auto").height();
            panel.$section.css("height",0);

            // Need to set the height to auto once animation is complete
            this.$el.one("accordion.afterOpen",function(){
                panel.$section.css("height", "auto");
            });
        }else{
            //temporarily set the div height to what the open class defines,
            // record it and animate to it
            panel.$panel.addClass("open");
            height = panel.$section.height();
            panel.$panel.removeClass("open");
        }

        panel.$section.animate({height:height},200, this._onOpen);

    },
    _cacheData:function(){
        var i = 0,
            $panels,
            panelLen;

        //store reference to panels
        this._openPanels = {};
        this._panels = {};

        $panels = this.$el.children("div.key");
        panelLen = $panels.length;

        for(; i < panelLen; i++){
            $panel = $panels.eq(i);
            var keyOpenerLinks = $panel.children('header').find('a.keyOpener');
            
            if (keyOpenerLinks.length > 0) {
                id = keyOpenerLinks.attr("href").substr(1);
                $section = $("#" + id);

                this._panels[id]= {
                    index: i,
                    key:id,
                    $panel:$panel,
                    $section:$section
                };
            }

            if($panel.hasClass("open")){
                this._openPanels[id] = true;
            }

        }

        return this;
    },
    _closeOpenPanels:function(){
        var panels = this._panels,
            openPanels = this._openPanels,
            panel;

        for(panel in openPanels){
            if(openPanels[panel]){
                this._close(panels[panel]);
            }
        }
    },
    _bindEvents:function(){
        this.$el.on("click",".accordion > div > header > h3 a.keyOpener", {accordion:this} , this._onKeyClick);
        return this;
    },
    _getKeyFromIndex:function(index){
        var panel,
            panels = this._panels;

        for(panel in panels){
            if(panels[panel].index === index) return panels[panel].key;
        }
    },


    //EVENT HANDLERS
    _onClose:function(){
        var $section = $(this),
            self = $section.closest(".accordion").data(SM.Accordion.__NAME),
            panelKey = $section.attr("id"),
            panel = self._panels[panelKey];

        panel.$panel.removeClass("open");
        $section.removeAttr("style");

        self.__trigger({type:"afterClose", index:panel.index, id:panel.key});
    },
    _onOpen:function(){
        var $section = $(this),
            self = $section.closest(".accordion").data(SM.Accordion.__NAME),
            panelKey = $section.attr("id"),
            panel = self._panels[panelKey];

        panel.$panel.addClass("open");
        self.__trigger({type:"afterOpen", index:panel.index, id:panel.key});
    },
    _onKeyClick:function(e){
        var self = e.data.accordion,
            panelKey = $(this).attr("href").substring(1);

       e.preventDefault();

       if(self._openPanels[panelKey]){
           self.close(panelKey);
       }else{
           self.open(panelKey);
       }

    }
};

SM.Views.register(SM.Accordion);
