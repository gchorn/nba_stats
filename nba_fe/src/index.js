import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import PlayerTable from './PlayerTable';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<PlayerTable />, document.getElementById('root'));
registerServiceWorker();
