'use strict';

angular.module('myApp.map', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
//        $routeProvider.when('/view1', {
//            templateUrl: 'view1/view1.html',
//            controller: 'View1Ctrl'
//        });
    }])

    .controller('MapCtrl',
    ['$scope', '$http',
        function ($scope, $http) {
            var MENU_SCOPE = angular.element('.menu-container').scope();

            $scope.map = window.map || null;

            $http.get('layers/call/json/lay_all').
                success(function (data, status, headers, config) {
                    if (MENU_SCOPE.$$phase) {
                        MENU_SCOPE.$evalAsync(function (scope) {
                            scope.layers = data.layers;
                        });
                    } else {
                        MENU_SCOPE.$apply(function (scope) {
                            scope.layers = data.layers;
                        });
                    }

                }).
                error(function (data, status, headers, config) {
                    // called asynchronously if an error occurs
                    // or server returns response with an error status.
                });

            $scope.$watch('map', function (value) {
                if (value) {
                    // Set mouseover event for each feature.
                    $scope.map.data.addListener('click', function (event) {
                        console.log(event.feature.getProperty('pid'));
                    });
                }
            });


        }])

    .service('MapSrvs', [function () {

    }]);