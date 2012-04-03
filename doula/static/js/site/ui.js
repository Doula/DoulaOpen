var UI = {
          
    statusTextHash: {
        'unchanged'           : 'Unchanged',
        'uncommitted_changes' : 'Uncommitted Changes',
        'change_to_config'    : 'Changes to Configuration',
        'change_to_app_env'   : 'Change to Application Environment',
        'tagged'              : 'Tagged'
    },

    init: function() {
        $("#accordion").accordion();
    },
    
    tagApp: function(app) {
        $('#panel_' + app.name_url).click();
        
        this.updateStatus(app);
    },
    
    updateStatus: function(app) {
        $('#stat_' + app.name_url).removeClass('stat-changed stat-error').addClass('stat-unchanged');
        $('#status_' + app.name_url).removeClass('status-changed status-error').addClass('status-unchanged');
    },
    
    updateDeploySiteBtn: function(isReadyForDeploy) {
        if(isReadyForDeploy) {
            $('#deploy_site_btn').removeClass('disabled').attr('disabled', '');
            $('.deployment p').addClass('hide');
        }
    }
    
};
// This ends the UI object