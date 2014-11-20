'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
    'ngRoute',
    'myApp.map',
    'myApp.menu',
    'myApp.modal',
    'myApp.admin',
    'myApp.version'
]).
    config(['$routeProvider', '$interpolateProvider', function ($routeProvider, $interpolateProvider) {
//        $routeProvider.otherwise({redirectTo: '/'});
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
    }]);
