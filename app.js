var app = angular.module('jepExplorer', []);
app.controller('jepCtrl', function($scope, $http) {
    $scope.selected_version = 'Any';
    $scope.selected_status = 'Any';

    window.addEventListener('popstate', function (e) {
        var state = e.state || {version: 'Any', status: 'Any'};
        $scope.selected_version = state.version;
        $scope.selected_status = state.status;
        $scope.$apply();
    });

    function state(fn) {
        fn(
            {version: $scope.selected_version, status: $scope.selected_status},
            null,
            ['#', $scope.selected_version, '_', $scope.selected_status].join('')
        );
    }

    $scope.pickversion = function(x) {
        $scope.selected_version = x;
        state(history.pushState.bind(history));
    };
    $scope.pickstatus = function(x) {
        $scope.selected_status = x;
        state(history.pushState.bind(history));
    };

    $http.get("index.json?cache-bust=" + Date.now())
    .then(function (response) {
        $scope.jeps = response.data.jeps;
        $scope.possible_releases = response.data.possible_releases;
        $scope.possible_statuses = response.data.possible_statuses;

        var match = location.hash && location.hash.match(/^#([^_]+)_(.+)$/);

        if (match[1] && $scope.possible_releases.indexOf(match[1]) >= 0) {
            $scope.selected_version = match[1];
        }
        if (match[2] && $scope.possible_statuses.indexOf(match[2]) >= 0) {
            $scope.selected_status = match[2];
        }

        state(history.replaceState.bind(history));
    });
});
