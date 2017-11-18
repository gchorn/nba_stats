import React, { Component } from 'react';
import {Input} from 'react-materialize'
import './App.css';
import PlayerTable from './PlayerTable';
import TeamTable from './TeamTable';

var _ = require('lodash')

class App extends Component {
  constructor() {
    super();
    this.playerSearchUpdate = this.playerSearchUpdate.bind(this);
    this.playerSearchInputChanged = this.playerSearchInputChanged.bind(this);
    this.navBarSelect = this.navBarSelect.bind(this);
    this.state = {
        searchValue: null,
        viewPlayers: true,
        viewTeams: false
    };
  }
  
  playerSearchInputChanged(event, value) {
      this.handleSearchDebounced(value);
  }

  playerSearchUpdate(value) {
      this.setState({ searchValue: value });
  }

  componentWillMount() {
      this.handleSearchDebounced = _.debounce(this.playerSearchUpdate, 350);
  }

  navBarSelect(e) {
      e.preventDefault();
      if (e.target.id === 'playerNavItem') {
          this.setState({viewPlayers: true});
          this.setState({ viewTeams: false });
      } else if (e.target.id === 'teamNavItem') {
          this.setState({viewPlayers: false});
          this.setState({viewTeams: true})
      }
  }

  componentDidUpdate(prevProps, prevState) {

  }

  render() {
    return (
      <div className="appContainer">
        <nav className="nbastatsnav">
            <div className="nav-wrapper">
                    <a href="" className="brand-logo"><img src="https://vignette.wikia.nocookie.net/logopedia/images/4/4c/NBA_Horizontal_Logo_.svg/revision/latest?cb=20160207144301" className="NBALogo"/></a>
                <ul id="nav-mobile" className="right hide-on-med-and-down">
                    <li><Input className="playerSearch" placeholder="Search all players" onChange={this.playerSearchInputChanged} /></li>
                    <li><a id="playerNavItem" href="" onClick={this.navBarSelect}>Players</a></li>
                    <li><a id="teamNavItem" href="" onClick={this.navBarSelect}>Teams</a></li>
                </ul>
            </div>
        </nav>
            {
                this.state.viewPlayers
                    ? <PlayerTable searchValue={this.state.searchValue} />
                    : null
            }
            {
                this.state.viewTeams
                    ? <TeamTable />
                    : null
            }
      </div>
    );
  }
}
export default App;
