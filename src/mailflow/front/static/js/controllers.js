/**
 * Created with PyCharm.
 * User: numelion
 * Date: 31.08.13
 * Time: 13:30
 * To change this template use File | Settings | File Templates.
 */

function DashboardInboxesCtrl($scope, $rootScope, $routeParams, $location, $timeout, Inboxes, Inbox) {
    $scope.goToFirst = function(inboxes) {
        if (inboxes && inboxes.data.length > 0){
            $location.path('/' + inboxes.data[0].id);
        };
    };

    $scope.getInboxes = function(callback) {
        return Inboxes.get(callback);
    };

    $scope.addInbox = function() {
        Inboxes.post(this.inbox, function() {
            $scope.inboxes = Inboxes.get();
            $scope.inbox = {name: ''};
        });
    };

    $scope.syncInboxes = function(delay) {
        $scope.inboxesWatcher = $timeout(function(){
            $scope.getInboxes(function(inboxes){
                $scope.inboxes = inboxes;
                $scope.syncInboxes(delay);
            });
        }, delay);
    };

    $scope.inboxes = $scope.getInboxes(function(inboxes) {
        if (!$routeParams.inboxId) {
            $scope.goToFirst(inboxes);
        };
    });

    $scope.$on('$routeChangeSuccess', function() {
        $scope.currentInboxId = $routeParams.inboxId;
    });

    $scope.$on('inboxUpdate', function () {
        $scope.getInboxes(function(inboxes) {
            $scope.inboxes = inboxes;
        });
    });

    $scope.$on('inboxGetError', function () {
        $scope.goToFirst($scope.inboxes);
    });

    $scope.$broadcast('inboxUpdate');
    $scope.syncInboxes(5000);
    $scope.$watch('inboxes', function(oldValues, newValues) {
        var oldInbox, newInbox, length;
        length = Math.max(newValues.count, oldValues.count);
        for (var i=0; i<length; i++) {
            if (oldValues.data[i] && oldValues.data[i].id == $scope.currentInboxId) {
                oldInbox = oldValues.data[i];
            }
            if (newValues.data[i] && newValues.data[i].id == $scope.currentInboxId) {
                newInbox = newValues.data[i];
            }
        };
        if (oldInbox && newInbox && oldInbox.total_messages != newInbox.total_messages) {
            $rootScope.$broadcast('messagesUpdate');
        }
    });

    $scope.$on('$destroy', function(){
        $timeout.cancel($scope.inboxesWatcher);
    });
};

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
    $scope.$on('messagesUpdate', function () {
        $scope.getInbox(function (inbox) {
            $scope.inbox = inbox;
        });
    });
}

function MessageInfoCtrl($scope, $routeParams, $sce, Message, Inbox) {
    $scope.inbox = Inbox.get({inboxId: $routeParams.inboxId});
    $scope.message = Message.get({messageId: $routeParams.messageId}, function (message) {
        message.body_html = $sce.trustAsHtml(message.body_html);
    });
}
