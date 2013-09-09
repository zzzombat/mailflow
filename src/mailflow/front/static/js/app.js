angular.module('dashboard', ['inboxServices', 'dashboard.filters']).
    config(['$routeProvider', function ($routeProvider) {
        $routeProvider.
            when('/:inboxId', {templateUrl: '/static/templates/dashboard_inbox.html', controller: DashboardInboxCtrl}).
            when('/:inboxId/message/:messageId', {templateUrl: '/static/templates/dashboard_message.html', controller: MessageInfoCtrl}).
            otherwise({redirectTo: ''});
    }]);
