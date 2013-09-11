var csrftoken = $('meta[name=csrf-token]').attr('content');

angular.module('dashboard', ['inboxServices', 'dashboard.filters', 'ngRoute', 'ngSanitize']).
    config(['$routeProvider', function ($routeProvider) {
        $routeProvider.
            when('/:inboxId', {templateUrl: '/static/templates/dashboard_inbox.html', controller: DashboardInboxCtrl}).
            when('/:inboxId/message/:messageId', {templateUrl: '/static/templates/dashboard_message.html', controller: MessageInfoCtrl}).
            otherwise({redirectTo: ''});
    }]).
    config(['$httpProvider', function ($httpProvider) {
        $httpProvider.defaults.headers.put['X-CSRFToken'] = csrftoken;
        $httpProvider.defaults.headers.post['X-CSRFToken'] = csrftoken;
        // Doesn't have the defaults for delete method but definetly needs them
        // inb4 dirty hack
        $httpProvider.defaults.headers.delete = $httpProvider.defaults.headers.post;
    }]);
