var Site = (function() {
    
    // The main Site Module
    var Site = {
       
       init: function() {
           SiteData.init();
           UI.init();
           
           this.bindEvents();
       },
       
       bindEvents: function() {
           $('form').on('submit', this.tagApplication);
       },
       
       tagApplication: function(event) {
           var app = SiteData.findAppByID(this.id.replace('form_', ''));
           
           var tag = $('#tag_' + app.name_url)[0].value;
           var msg = $('#msg_' + app.name_url)[0].value;
           
           SiteData.tagApp(app, tag, msg);
           UI.tagApp(app);
           UI.updateDeploySiteBtn(SiteData.isReadyForDeploy());
           
           return false;
       }
    };
    // This ends the main Site module
    
    return Site;
})();

$(document).ready(function() {
    Site.init();
});