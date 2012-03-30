var Site = (function() {
    
    // The main Site Module
    var Site = {
       
       init: function() {
           SiteData.init();
           
           UI.init();
           this.bindEvents();
       },
       
       bindEvents: function() {
           // UI only events events
           
           // Data events
           $('button[value="revert"]').on('click', this.revertApplication);
           $('form').on('submit', this.tagApplication);
       },
       
       revertApplication: function(event) {
               event.stopPropagation();

           var appID = this.id.replace('revert_', '');
           // alextodo, need to revert on backend
           var app = SiteData.revertApp(appID);
           
           UI.revertApp(app);

           return false;
       },
       
       tagApplication: function() {
           event.stopPropagation();
           
            var app = SiteData.findAppByID(this.id.replace('tag_form_', ''));
           var tag = $('#' + this.id + ' input')[0].value;
           var msg = $('#' + this.id + ' textarea')[0].value;

           SiteData.tagApp(app, tag, msg);
            UI.tagApp(app);
           
           return false;
       }
    };
    // This ends the main Site module
    
    return Site;
})();

$(document).ready(function() {
    Site.init();
});