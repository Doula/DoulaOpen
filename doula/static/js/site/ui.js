var UI = {
          
    statusClassHash: {
        'deployed'                : 'deployed',
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
    
    // Execute before the ajax call to server
    onTagApp: function(app) {
        $('#form_' + app.name_url + ' input.btn').attr('disabled', 'disabled');
    },
    
    deployApp: function(app) {
        $('#deploy_' + app.name_url).hide();
        this.updateStatus(app);
    },

    tagApp: function(app) {
        $('#panel_' + app.name_url).click();
        // You can longer tag an app after it's been tagged
        $('#panel_' + app.name_url).on('click', function() { return false; });
        $('#panel_' + app.name_url + ' em').hide();

        this.updateStatus(app);
    },

    failedTag: function(app) {
        $('#form_' + app.name_url + ' input.btn').attr('disabled', '');
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