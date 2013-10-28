function MessageInfoCtrl($scope, $routeParams, $sce, Message, Inbox) {
    $scope.inbox = Inbox.get({inboxId: $routeParams.inboxId});
    $scope.message = Message.get({messageId: $routeParams.messageId}, function (message) {
        message.body_html = $sce.trustAsHtml(message.body_html);
    });
}
