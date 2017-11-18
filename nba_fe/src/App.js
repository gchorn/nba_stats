import React, { Component } from 'react';
import {Input} from 'react-materialize'
import './App.css';
import PlayerTable from './PlayerTable';
import PlayerDetail from './PlayerDetail';
import TeamTable from './TeamTable';

var _ = require('lodash')

class App extends Component {
  constructor() {
    super();
    this.playerSearchUpdate = this.playerSearchUpdate.bind(this);
    this.playerSearchInputChanged = this.playerSearchInputChanged.bind(this);
    this.onPlayerSelect = this.onPlayerSelect.bind(this);
    this.navBarSelect = this.navBarSelect.bind(this);
    this.state = {
        searchValue: null,
        playerId: null,
        views: {
            Players: true,
            Teams: false,
            PlayerDetail: false
        }
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

  changeView(views, selectedView) {
      var newViews = {}
      _.forIn(views, function (value, key) {
          if (key === selectedView) {
              newViews[key] = true
          } else {
              newViews[key] = false
          }
      })
      return newViews;
  }

  navBarSelect(e) {
      e.preventDefault();
      let newViews = this.changeView(this.state.views, e.target.id);
      this.setState({ views: newViews });
  }

  onPlayerSelect(playerId) {
    this.setState({ playerId: playerId });
    let newViews = this.changeView(this.state.views, 'PlayerDetail');
    this.setState({ views: newViews });

  }

  render() {
    return (
      <div className="appContainer">
        <nav className="nbastatsnav">
            <div className="nav-wrapper">
                    <a href="" className="brand-logo"><img src="https://vignette.wikia.nocookie.net/logopedia/images/4/4c/NBA_Horizontal_Logo_.svg/revision/latest?cb=20160207144301" className="NBALogo" alt="NBA"/></a>
                <ul id="nav-mobile" className="right hide-on-med-and-down">
                    { this.state.views.Players 
                        ? <li><Input className="playerSearch" placeholder="Search all players" onChange={this.playerSearchInputChanged} /></li>
                        : null
                    }
                    <li><a id="Players" href="" onClick={this.navBarSelect}>Players</a></li>
                    <li><a id="Teams" href="" onClick={this.navBarSelect}>Teams</a></li>
                </ul>
            </div>
        </nav>
            {
                this.state.views.Players
                    ? <PlayerTable searchValue={this.state.searchValue} onPlayerSelect={this.onPlayerSelect}/>
                    : null
            }
            {
                this.state.views.Teams
                    ? <TeamTable />
                    : null
            }
            {
                this.state.views.PlayerDetail
                    ? <PlayerDetail playerId={this.state.playerId}/>
                    : null
            }
      </div>
    );
  }
}
export default App;
