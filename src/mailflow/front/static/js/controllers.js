/**
 * Created with PyCharm.
 * User: numelion
 * Date: 31.08.13
 * Time: 13:30
 * To change this template use File | Settings | File Templates.
 */

function DashboardInboxesCtrl($scope, $http) {
    $scope.textR = 'dsfsdfsdfsdf';
    $scope.data = 123;

    $http.get('/static/js/inboxesData.json').success(function (data) {
        $scope.inboxes = data;
    });
}

function DashboardInboxCtrl($scope, $routeParams, Inbox) {
    $scope.inbox = Inbox.get({inboxId: $routeParams.inboxId});
}