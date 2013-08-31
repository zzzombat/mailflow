/**
 * Created with PyCharm.
 * User: numelion
 * Date: 31.08.13
 * Time: 16:53
 * To change this template use File | Settings | File Templates.
 */
angular.module('inboxServices', ['ngResource'])
    .factory('Inbox', function ($resource) {
        return $resource('/static/js/inboxData:inboxId.json', {}, {
            query: {method: 'GET', params: {inboxId: ''}, isArray: false, cache: false, responseType: 'json'}
        });
    });

