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
