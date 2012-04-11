var UI = {
          
    statusClassHash: {
        'unchanged'                : 'unchanged',
        'uncommitted_changes'      : 'error',
        'change_to_config'         : 'changed',
        'change_to_app_env'        : 'changed',
        'change_to_app_and_config' : 'changed',
        'tagged'                   : 'tagged'
    },

    init: function() {
        $("#accordion").accordion();
        // If you cannot tag because of uncommitted changes
        // bind a function that will nullify the link click
        $('a.keyCloser').on('click', function() { return false; });
        $('.sm-side-tab').sideTab();
    },
    
    tagApp: function(app) {
        $('#panel_' + app.name_url).click();
        
        this.updateStatus(app);
    },
    
    updateStatus: function(app) {
        $('#stat_' + app.name_url).
          removeClass('stat-changed stat-error stat-tagged').
          addClass(this.getStatClass(app));
        
        $('#status_' + app.name_url).
          removeClass('status-changed status-error status-tagged').
          addClass(this.getStatusClass(app));
    },
    
    getStatusClass: function(app) {
      return 'status-' + this.statusClassHash[app.status];
    },
    
    getStatClass: function(app) {
      return 'stat-' + this.statusClassHash[app.status];
    },
    
    updateDeploySiteBtn: function(isReadyForDeploy) {
        if(isReadyForDeploy) {
            $('#deploy_site_btn').removeClass('disabled').attr('disabled', '');
            $('.deployment p').addClass('hide');
        }
    }
    
};
// This ends the UI object