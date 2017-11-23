import React, { Component } from 'react';
import {ProgressBar} from 'react-materialize';
import TotalsTable from './TotalsTable';
import PerGameTable from './PerGameTable';
import './PlayerDetail.css';


class PlayerDetail extends Component {
  constructor() {
    super();
    this.state = {
      playerInfo: {},
      seasonStats: [],
      loading: 'ProgressBar-hidden',
    };
  }

  fetchPlayer() {
    this.setState({ loading: null });

    let fetchUrl = `http://localhost/players/${this.props.playerId}?format=json`

    fetch(fetchUrl)
      .then(results => {
        return results.json();
      }).then(data => {
        this.setState({ playerInfo: data });
        this.setState({ seasonStats: data.season_stats });
        this.setState({ loading: 'ProgressBar-hidden' });
      })
  }

  componentWillMount() {
    this.fetchPlayer();
  }

  render() {
    return (
      <div className="tableContainer">
        <h1 className="pageTitle">
          {this.state.playerInfo.first_name} {this.state.playerInfo.last_name}
        </h1>
        <ProgressBar className={this.state.loading}/>
        <TotalsTable stats={this.state.seasonStats}/>
        <PerGameTable stats={this.state.seasonStats}/>
      </div>
    );
  }
}
export default PlayerDetail;
