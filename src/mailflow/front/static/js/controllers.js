/**
 * Created with PyCharm.
 * User: numelion
 * Date: 31.08.13
 * Time: 13:30
 * To change this template use File | Settings | File Templates.
 */

function DashboardInboxesCtrl($scope, $http, Inboxes) {
    $scope.inboxes = Inboxes.get();
}

function DashboardInboxCtrl($scope, $routeParams, Messages, Inbox) {
    $scope.inbox = Inbox.get({inboxId: $routeParams.inboxId});
    $scope.messages = Messages.get({inboxId: $routeParams.inboxId});
}
