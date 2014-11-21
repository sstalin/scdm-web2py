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
                        MENU_SCOPE.$eval(function (scope) {
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

//            $scope.$watch('map', function (value) {
//                if (value) {
//                    // adding click event handler
//                    $scope.map.data.addListener('click', function (event) {
//                    //   console.log(event.feature.getProperty('pid'));
//                        MODAL_SCOPE.pop(event.feature);
//
//                    });
//
//                }
//            });


        }])

    .service('MapSrvs', [function () {
        /**
         * Reset map.data object by removing all features and click handlers.
         */
        this.resetDataLayer = function () {
            if(map){
                map.data.forEach(function (next) {
                    map.data.remove(next);
                }
            );
            google.maps.event.clearListeners(map.data, 'click');
            }
        };
    }]);