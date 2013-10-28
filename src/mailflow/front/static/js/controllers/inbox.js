function DashboardInboxCtrl($scope, $rootScope, $http, $routeParams, Inbox) {
    var page = $routeParams.page || 1;

    $scope.getInbox = function (callback) {
        return Inbox.get({inboxId: $routeParams.inboxId, page: page}, function(data) {
            if (callback) {
                callback(data);
            }
        }, function(data) {
            $rootScope.$broadcast('inboxGetError');
        });
    };

    $scope.getInboxAndCopy = function() {
        $scope.inbox = $scope.getInbox(function(data) {
            $scope.inboxEdit = angular.copy(data);
        });
    };

    $scope.truncateInbox = function() {
        $http.post('/api/inbox/' + $routeParams.inboxId + '/truncate')
            .success(function() {
                $scope.getInbox(function (data) {
                    $scope.inbox = data;
                    $rootScope.$broadcast('inboxUpdate');
                });
            });
    };

    $scope.updateInbox = function() {
        Inbox.put($scope.inboxEdit, function() {
            $rootScope.$broadcast('inboxUpdate');
        });
    };

    $scope.deleteInbox = function() {
        Inbox.delete({inboxId: $routeParams.inboxId}, function() {
            $rootScope.$broadcast('inboxUpdate');
        });
    };

    $scope.getInboxAndCopy();
    $scope.$on('inboxUpdate', $scope.getInboxAndCopy);
    $scope.$on('newMessage', function (event, message) {
        if (page == 1) {
            $scope.inbox.messages.unshift(message);
            $scope.inbox.total_messages += 1;
            $scope.inbox.messages_on_page = Math.min(
                $scope.inbox.messages_on_page + 1,
                $scope.inbox.max_messages_on_page
            );
            $scope.inbox.total_pages = Math.ceil($scope.inbox.total_messages / $scope.inbox.messages_on_page);
        } else {
            $scope.getInbox(function (inbox) {
                $scope.inbox = inbox;
            });
        };
    });
}
