/**
 * Created with PyCharm.
 * User: numelion
 * Date: 31.08.13
 * Time: 16:53
 * To change this template use File | Settings | File Templates.
 */
angular.module('inboxServices', ['ngResource'])
    .factory('Messages', function ($resource) {
        return $resource('/static/data/messages/:inboxId.json', {}, {
            get: {method: 'GET', params: {}, isArray: true, cache: false, responseType: 'json'}
        });
    }).factory('Message', function($resource){
        return $resource('/static/data/message/:messageId.json', {})
    }).factory('Inboxes', function($resource){
        return $resource('/static/data/inboxes.json', {},  {
            get: {method: 'GET', params: {}, isArray: true, cache: false, responseType: 'json'}
        });
    }).factory('Inbox', function($resource){
        return $resource('/static/data/inbox/:inboxId.json', {})
    });
