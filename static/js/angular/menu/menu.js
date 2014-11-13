'use strict';

angular.module('myApp.menu', ['ngRoute', 'myApp.map'])

    .config(['$routeProvider', function ($routeProvider) {
//        $routeProvider.when('/view1', {
//            templateUrl: 'view1/view1.html',
//            controller: 'View1Ctrl'
//        });
    }])

    .controller('MenuCtrl',
    [
        '$rootScope', '$scope', 'MenuSrvs', 'MapSrvs',
        function ($rootScope, $scope, MenuSrvs, MapSrvs) {
            var overlay = angular.element(".overlay"),
                menuBtn = angular.element("#menu-btn"),
                menuTray = angular.element('.menu-tray'),
                isMenuOn = false;

            /**
             * Toggles menu on/off
             */
            function toggleMenu() {
                isMenuOn = !isMenuOn;
                if (isMenuOn) {
                    overlay.addClass('on');
                    menuTray.addClass('on');
                } else {
                    overlay.removeClass('on');
                    menuTray.removeClass('on');
                    loadLayers();// loading geoJson data
                }
            }


            menuBtn.click(function (e) {
                if($rootScope.isModalOn){
                    $rootScope.toggleModal();
                }
                toggleMenu();
            });

            overlay.click(function (e) {
                toggleMenu();
            });

            /**
             * Reset map.data object and adds new selected layers data.
             */
            function loadLayers() {
                MapSrvs.resetDataLayer();
                MenuSrvs.processQueue();

                map.data.setStyle(
                    {
                        icon: "/scdm/static/images/icon-control-unselected-1-hori.png"
                    });

                map.data.addListener('click', $rootScope.popModal);
            }


            $scope.layToggle = function (layer) {
                if (layer.isSelected) {
                    layer.isSelected = false;
                } else {
                    layer.isSelected = true;
                }
            };


        }])

    .service('MenuSrvs',
    ['$http',
        function ($http) {
            var self = this;

            self.queue = [];

            function addGeoJSON(data, status, headers, config) {
                if (status == 200) {
                    self.queue[self.index] = data;
                }
            }

            function removeGeoJSON(index) {
                self.queue[index] = null;
            }

            /**
             * Add to map all selected layers(GeoJson files).
             */
            this.processQueue = function () {
                self.queue.forEach(function (next) {
                    if (next) {
                        map.data.addGeoJson(next);
                    }
                });
            };

            /**
             * Loads GeoJson file for selected layer from database, and puts it into
             * self.queue = [] array to be processed on menu close event
             * @param layer
             * @param index
             */
            this.loadGeoJSON = function (layer, index) {
                var lay_URL = '/scdm/map/download/' + layer.filename;

                self.index = index;
                // Load a GeoJSON
                $http.get(lay_URL).
                    success(addGeoJSON).
                    error(function (data, status, headers, config) {
                        // called asynchronously if an error occurs
                        // or server returns response with an error status.
                    });
            };

            this.unloadGeoJSON = function (index) {
                removeGeoJSON(index);
            };


        }])

    .directive('layMenuItem', function (MenuSrvs) {

        return function (scope, element, attrs) {
            scope.$watch('layer.isSelected', function (value) {
                if (value == true) {
                    MenuSrvs.loadGeoJSON(scope.layer, scope.$index);
                } else if (value == false) {
                    MenuSrvs.unloadGeoJSON(scope.$index);
                }
            });
        }
    });

