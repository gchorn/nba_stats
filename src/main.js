import React from 'react';
import ReactDOM from 'react-dom';
import PlayerTable from './PlayerTable';

document.addEventListener('DOMContentLoaded', function () {
    ReactDOM.render(
        React.createElement(PlayerTable),
        document.getElementById('mount')
    );
});