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
    
    revertApp: function(appID) {
        var app = this.findAppByID(appID);
        app.status = "unchanged";
        
        return app;
    },
    
    tagApp: function(app, tag, msg) {
        app.tag = tag;
        app.msg = msg;
        app.status = 'tagged';
    },
    
    findAppByID: function(appID) {
        for (var i=0; i < this.applications.length; i++) {
            if(this.applications[i].id == appID) {
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