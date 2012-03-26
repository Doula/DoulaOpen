var UI = {
          
    statusTextHash: {
        'unchanged'           : 'Unchanged',
        'uncommitted_changes' : 'Uncommitted Changes',
        'change_to_config'    : 'Changes to Configuration',
        'change_to_app_env'   : 'Change to Application Environment',
        'tagged'              : 'Tagged'
    },

    init: function() {
        $(".collapse").collapse({
            toggle: false,
        });
    },
    
    revertApp: function(app) {
        $('#revert_' + app.id).hide();
        $('#application_details_' + app.id).collapse('hide');

        this.updateStatus(app);
        this.showFriendlyStatus(app);
        
        this.updateDeploySiteBtn();
    },
    
    tagApp: function(app) {
        $('#application_details_' + app.id).collapse('hide');

        this.updateStatus(app);
        this.showFriendlyStatus(app);
    },
    
    showFriendlyStatus: function(app) {
        var friendlyStatus = this.statusTextHash[app.status];
        $('#app_status_text_' + app.id).html(friendlyStatus);
    },
    
    updateStatus: function(app) {
        $('#app_status_' + app.id)[0].className = app.status;
    },
    
    updateDeploySiteBtn: function() {
        if(SiteData.isReadyForDeploy()) {
            $('#tag_deployment').removeClass('disabled');
            $('#tag_deployment').next().addClass('hide');
        }
    }
    
};
// This ends the UI object