/**
 * Created with PyCharm.
 * User: numelion
 * Date: 31.08.13
 * Time: 16:53
 * To change this template use File | Settings | File Templates.
 */

angular.module('inboxServices', ['ngResource'])
    .factory('Messages', function ($resource) {
        return $resource('/api/message/', {}, {
            get: {method: 'GET', params: {}, isArray: false, cache: false, responseType: 'json'}
        });
    }).factory('Message', function($resource){
        return $resource('/api/message/:messageId', {});
    }).factory('Inboxes', function($resource){
        return $resource('/api/inbox', {},  {
            get: {method: 'GET', params: {}, isArray: false, cache: false, responseType: 'json'},
            post: {method: 'POST', params: {}, isArray: false, cache: false, responseType: 'json'}
        });
    }).factory('Inbox', function($resource){
        return $resource('/api/inbox/:inboxId', {}, {
            get: {method: 'GET', params: {}, isArray: false, cache: false, responseType: 'json'},
            put: {method: 'PUT', params: {'inboxId': '@id'}, isArray: false, cache: false, responseType: 'json'}
        });
    });
