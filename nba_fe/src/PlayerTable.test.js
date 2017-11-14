import React from 'react';
import ReactDOM from 'react-dom';
import PlayerTable from './PlayerTable';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<PlayerTable />, div);
});
