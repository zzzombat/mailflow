angular.module('dashboard', ['inboxServices']).
    config(['$routeProvider', function ($routeProvider) {
        $routeProvider.
            //when('', {templateUrl: '/static/templates/dashboard_inboxes.html', controller: DashboardInboxesCtrl}).
            when('/:inboxId', {templateUrl: '/static/templates/dashboard_inbox.html', controller: DashboardInboxCtrl}).
            otherwise({redirectTo: ''});
    }]);