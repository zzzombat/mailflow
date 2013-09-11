/**
 * Created with PyCharm.
 * User: numelion
 * Date: 31.08.13
 * Time: 13:30
 * To change this template use File | Settings | File Templates.
 */

function DashboardInboxesCtrl($scope, $routeParams, $location, Inboxes, Inbox) {
    $scope.goToFirst = function(inboxes) {
        if(inboxes.data.length > 0){
            $location.path('/' + inboxes.data[0].id);
        };
    };

    $scope.getInboxes = function(callback) {
        $scope.inboxes = Inboxes.get(callback);
    };

    $scope.addInbox = function() {
        Inboxes.post(this.inbox, function() {
            $scope.inboxes = Inboxes.get();
            $scope.inbox = {name: ''};
        });
    };

    $scope.deleteInbox = function(id) {
        Inbox.delete({inboxId: id}, function() {
            $scope.getInboxes(function(inboxes) {
                if ($routeParams.inboxId == id) {
                    $scope.goToFirst($scope.inboxes);
                };
            });
        });
    };

    $scope.getInboxes(function(inboxes) {
        if (!$routeParams.inboxId) {
            $scope.goToFirst(inboxes);
        };
    });

    $scope.$on('$routeChangeSuccess', function() {
        $scope.currentInboxId = $routeParams.inboxId;
    });

    $scope.$on('inboxUpdated', function () {
        $scope.getInboxes();
    });
};

function DashboardInboxCtrl($scope, $rootScope, $http, $routeParams, $timeout, Messages, Inbox) {
    var page = $routeParams.page || 1;
    $scope.getInbox = function (callback) {
        return Inbox.get({inboxId: $routeParams.inboxId}, function(data) {
            $scope.inboxEdit = angular.copy(data);
            if (callback) {
                callback(data);
            }
        });
    };

    $scope.getMessages = function(callback) {
        return Messages.get({inbox_id: $routeParams.inboxId, page: page}, callback);
    };

    $scope.truncateInbox = function() {
        $http.post('/api/inbox/' + $routeParams.inboxId + '/truncate')
            .success($scope.getMessages);
    };

    $scope.updateInbox = function() {
        Inbox.put($scope.inboxEdit, function() {
            $rootScope.$broadcast('inboxUpdated');
        });
    };

    $scope.watchMessages = function(delay) {
        $scope.messageWatcher = $timeout(function(){
            $scope.getMessages(function(messages){
                $scope.messages = messages;
                $scope.watchMessages(delay);
            });
        }, delay);
    };

    $scope.inbox = $scope.getInbox();
    $scope.messages = $scope.getMessages();
    $scope.watchMessages(5000);

    $scope.$on('inboxUpdated', function () {
        $scope.inbox = $scope.getInbox();
    });
    $scope.$on('$destroy', function(){
        $timeout.cancel($scope.messageWatcher);
    });
}

function MessageInfoCtrl($scope, $routeParams, $sce, Message, Inbox) {
    $scope.inbox = Inbox.get({inboxId: $routeParams.inboxId});
    $scope.message = Message.get({messageId: $routeParams.messageId}, function (message) {
        message.body_html = $sce.trustAsHtml(message.body_html);
    });
}
