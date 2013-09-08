/**
 * Created with PyCharm.
 * User: numelion
 * Date: 31.08.13
 * Time: 13:30
 * To change this template use File | Settings | File Templates.
 */

function DashboardInboxesCtrl($scope, Inboxes, Inbox) {
    $scope.inboxes = Inboxes.get();
    $scope.addInbox = function() {
        Inboxes.post(this.inbox, function() {
            $scope.inboxes = Inboxes.get();
        });
    };
    $scope.deleteInbox = function(id) {
        Inbox.delete({inboxId: id}, function() {
            $scope.inboxes = Inboxes.get();
        });
    };
}

function DashboardInboxCtrl($scope, $http, $routeParams, $timeout, Messages, Inbox) {
    $scope.inbox = Inbox.get({inboxId: $routeParams.inboxId});

    $scope.getMessages = function(callback) {
        $scope.messages = Messages.get({inbox_id: $routeParams.inboxId}, callback);
    };

    $scope.truncateInbox = function() {
        $http.post('/api/inbox/' + $routeParams.inboxId + '/truncate')
            .success($scope.getMessages);
    };

    $scope.watchMessages = function() {
        $scope.messageWatcher = $timeout(function(){
            $scope.getMessages($scope.watchMessages);
        }, 5000);
    };

    $scope.getMessages();
    $scope.watchMessages();
    $scope.$on('$destroy', function(){
        $timeout.cancel($scope.messageWatcher);
    });
}

function MessageInfoCtrl($scope, $routeParams, Message, Inbox) {
    $scope.inbox = Inbox.get({inboxId: $routeParams.inboxId});
    $scope.message = Message.get({messageId: $routeParams.messageId});
}
