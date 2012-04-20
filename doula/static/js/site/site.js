var Site = (function() {
  // The main Site Module
  var Site = {
    init: function() {
        SiteData.init();
        UI.init();
        
        this.bindEvents();
    },
    
    bindEvents: function() {
      $('input.tag').on('change', this.validateTag);
      $('textarea.commit').on('change', this.validateMsg);
      $('form').on('submit', this.tagApplication);
      $('a.deploy').on('click', this.deployApplication);
    },

    deployApplication: function() {
        var app = SiteData.findAppByID($(this).attr('app-id'));
        SiteData.deployApplication(app);
        
        return false;
    },
    
    tagApplication: function(event) {
        var app = SiteData.findAppByID($(this).attr('app-id'));
        var tag = $('#tag_' + app.name_url)[0].value;
        var msg = $('#msg_' + app.name_url)[0].value;
        
        UI.onTagApp(app);
        SiteData.tagApp(app, tag, msg);
        
        return false;
    },
    
    successfulTagApp: function(app) {
        UI.tagApp(app);
        UI.updateDeploySiteBtn(SiteData.isReadyForDeploy());
    },
    
    validateTag: function(event) {
      if(!this.value) {
        var app = SiteData.findAppByID(this.id.replace('tag_', ''));
        SiteData.revertAppTag(app, '', app.msg);
        UI.tagApp(app);
      }
    },
    
    validateMsg: function() {
      if(!this.value) {
        var app = SiteData.findAppByID(this.id.replace('msg_', ''));
        SiteData.revertAppTag(app, app.tag, '');
        UI.tagApp(app);
      }
    }
  };
  // This ends the main Site module
  
  return Site;
})();

$(document).ready(function() {
  Site.init();
});