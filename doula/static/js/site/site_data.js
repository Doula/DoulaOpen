// The SiteData Module
var SiteData = {
    
    name: '',
    name_url: '',
    nodes: { },
    applications: { },
    status: '',
    
    
    init: function() {
        this.mixin();
    },
    
    mixin: function() {
        for(var x in __site) {
            this[x] = __site[x];
        }
    },
    
    tagApp: function(app, tag, msg) {
        params = {
            'site'        : SiteData.name_url,
            'application' : app.name_url,
            'tag'         : tag,
            'msg'         : msg
        }
        
        // alextodo, use a personal version of ajax
        $.ajax({
              url: '/tag',
              type: 'POST',
              data: this.getDataValues(params),
              success: function(rslt) {
                  var obj = $.parseJSON(rslt);
                  
                  if(obj.success) {
                      app = SiteData.findAppByID(obj.app.name_url);
                      app.tag = obj.app.last_tag_app;
                      app.msg = obj.app.msg;
                      app.status = obj.app.status;
                      
                      Site.successfulTagApp(app);
                  }
                  else {
                      // alextodo, need to make call to UI.failed whatever
                      alert(obj.msg);
                  }
              }
        });
    },

    deployApplication: function(app) {
        params = {
            'site'        : SiteData.name_url,
            'application' : app.name_url
        }
        
        $.ajax({
              url: '/deploy.json',
              type: 'POST',
              data: this.getDataValues(params),
              success: function(rslt) {
                  var obj = $.parseJSON(rslt);
                  
                  // should be implemented on index page
                  if(obj.success) {
                      app = SiteData.findAppByID(obj.app.name_url);
                      app.status = obj.app.status;
                      UI.deployApp(app);
                  }
                  else {
                      // alextodo, need to make call to UI. failed whatever
                      alert(obj.msg);
                  }
              }
        });
    },
    
    getDataValues: function(params) {
        var dataValues = '';
        var count = 0;
        
        for(var key in params) {
            if(dataValues != '') dataValues += '&';
            dataValues += key + '=' + encodeURIComponent(params[key]);
        }
        
        return dataValues;
    },
    
    revertAppTag: function(app, tag, msg) {
      app.tag = tag;
      app.msg = msg;
      app.status = app.originalStatus;
    },
    
    findAppByID: function(name_url) {
        return this.applications[name_url];
    },
    
    isReadyForDeploy: function() {
        var isReadyForDeploy = true;
        
        for (var i=0; i < this.applications.length; i++) {
            if( this.applications[i].status != 'deployed' &&
                this.applications[i].status != 'tagged' ) {
                isReadyForDeploy = false;
                break;
            }
        }
        
        return isReadyForDeploy;
    }
};