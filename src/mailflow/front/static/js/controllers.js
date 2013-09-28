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

    $scope.syncInboxes = function() {
        $scope.message_source = new EventSource('/api/message/update');
        $scope.message_source.onmessage = function (event) {
            var message = JSON.parse(event.data);
            for (var i = 0; i < $scope.inboxes.count; i++) {
                if ($scope.inboxes.data[i].id == message.inbox_id) {
                    $scope.$apply(function(){
                        $scope.inboxes.data[i].total_messages += 1;
                        if (message.inbox_id == $scope.currentInboxId) {
                            $rootScope.$broadcast('newMessage', message);
                        }
                    });
                    break;
                };
            };
        };
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
    $scope.syncInboxes();
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
    $scope.$on('newMessage', function (event, message) {
        if (page == 1) {
            $scope.inbox.messages.unshift(message);
            $scope.inbox.total_messages += 1;
            $scope.inbox.total_pages = Math.ceil($scope.inbox.total_messages / $scope.inbox.messages_on_page);
        } else {
            $scope.getInbox(function (inbox) {
                $scope.inbox = inbox;
            });
        };
    });
}

function MessageInfoCtrl($scope, $routeParams, $sce, Message, Inbox) {
    $scope.inbox = Inbox.get({inboxId: $routeParams.inboxId});
    $scope.message = Message.get({messageId: $routeParams.messageId}, function (message) {
        message.body_html = $sce.trustAsHtml(message.body_html);
    });
}
