/**
 * Created with PyCharm.
 * User: numelion
 * Date: 31.08.13
 * Time: 13:30
 * To change this template use File | Settings | File Templates.
 */

function DashboardInboxesCtrl($scope, $location, Inboxes, Inbox) {
    $scope.inboxes = Inboxes.get(function(inboxes) {
        if(inboxes.data.length > 0){
            $location.path('/' + inboxes.data[0].id);
        };
    });

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
};

function DashboardInboxCtrl($scope, $http, $routeParams, $timeout, Messages, Inbox) {
    $scope.inbox = Inbox.get({inboxId: $routeParams.inboxId});

    var page = $routeParams.page || 1;

    $scope.getMessages = function(callback) {
        return Messages.get({inbox_id: $routeParams.inboxId, page: page}, callback);
    };

    $scope.truncateInbox = function() {
        $http.post('/api/inbox/' + $routeParams.inboxId + '/truncate')
            .success($scope.getMessages);
    };

    $scope.watchMessages = function(delay) {
        $scope.messageWatcher = $timeout(function(){
            $scope.getMessages(function(messages){
                $scope.messages = messages;
                $scope.watchMessages(delay);
            });
        }, delay);
    };

    $scope.messages = $scope.getMessages();
    $scope.watchMessages(5000);
    $scope.$on('$destroy', function(){
        $timeout.cancel($scope.messageWatcher);
    });
}

function MessageInfoCtrl($scope, $routeParams, Message, Inbox) {
    $scope.inbox = Inbox.get({inboxId: $routeParams.inboxId});
    $scope.message = Message.get({messageId: $routeParams.messageId});
}
