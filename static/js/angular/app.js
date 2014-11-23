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
    }])
    .directive('flash', function ($rootScope) {

        return function (scope, element, attrs) {
              $rootScope.$watch('flash', function(value){
                 if(value){
                     var html = value
                     + "<span id='closeflash'> × </span>";
                     element.html(html);
                     element.show();
                 }
              });

            element.click(function(){
               $rootScope.flash = '';
            });
        }
    });
