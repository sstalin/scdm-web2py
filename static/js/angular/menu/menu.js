'use strict';

angular.module('myApp.menu', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
//        $routeProvider.when('/view1', {
//            templateUrl: 'view1/view1.html',
//            controller: 'View1Ctrl'
//        });
    }])

    .controller('MenuCtrl',
    [
        '$scope', '$http',
        function ($scope) {
            //TODO
            var MAP_SCOPE = angular.element('#map-canvas').scope();

            $scope.layToggle = function (layer) {
                var kmlLayer, url;

                if (layer.l.isSelected) {
                    // Hide the Data layer.
                    map.data.setStyle({visible: false});
                    layer.l.isSelected = false;
                } else {
                    map.data.setStyle(
                        {
                            visible: true,
                            icon: "/scdm/static/images/icon-control-unselected-1-hori.png"
                    });

                    url = '/scdm/map/download/' + layer.l.filename;

                    // Load a GeoJSON from the same server as our demo.
                    map.data.loadGeoJson(url);
                    layer.l.isSelected = true;
                }
            };


        }])

    .service('MenuSrvs', [function () {

    }]);
