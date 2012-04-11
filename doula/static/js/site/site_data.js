// The SiteData Module
var SiteData = {
    
    init: function() {
        this.mixin();
    },
    
    mixin: function() {
        for(var x in __site) {
            this[x] = __site[x];
        }
    },
    
    tagApp: function(app, tag, msg) {
        app.tag = tag;
        app.msg = msg;
        app.originalStatus = app.status;
        app.status = 'tagged';
        console.log(this);
        console.log(app);
        // $.ajax({
        //       url: '/tag',
        //       type: 'POST',
        //       data: 'content',
        //       success: function(rslt) {
        //           console.log(rslt);
        //           // alextodo, need to revert if we fail
        //       }
        // });
    },
    
    revertAppTag: function(app, tag, msg) {
      app.tag = tag;
      app.msg = msg;
      app.status = app.originalStatus;
    },
    
    findAppByID: function(name_url) {
        for (var i=0; i < this.applications.length; i++) {
            if(this.applications[i].name_url == name_url) {
                return this.applications[i];
            }
        }
    },
    
    isReadyForDeploy: function() {
        var isReadyForDeploy = true;
        
        for (var i=0; i < this.applications.length; i++) {
            if( this.applications[i].status != 'unchanged' &&
                this.applications[i].status != 'tagged' ) {
                isReadyForDeploy = false;
                break;
            }
        }
        
        return isReadyForDeploy;
    }
};