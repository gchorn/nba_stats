import React, { Component } from 'react';
import {ProgressBar} from 'react-materialize'
// import './PlayerDetail.css';


class PlayerDetail extends Component {
  constructor() {
    super();
    this.state = {
      playerInfo: {},
      playerStats: [],
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
        let playerStats = data.season_stats.map((ps) => {
          return (
            <tr key={ps.url}>
              <td>{ps.season_year}</td>
              <td>{ps.gp}</td>
              <td>{ps.mp}</td>
              <td>{ps.fg}</td>
              <td>{ps.fga}</td>
              <td>{ps.ft}</td>
              <td>{ps.fta}</td>
              <td>{ps.three_pointers}</td>
              <td>{ps.threes_attempted}</td>
              <td>{ps.orb}</td>
              <td>{ps.drb}</td>
              <td>{ps.ast}</td>
              <td>{ps.stl}</td>
              <td>{ps.blk}</td>
              <td>{ps.tov}</td>
              <td>{ps.pf}</td>
              <td>{ps.pts}</td>
            </tr>
          )
        })
        this.setState({ playerInfo: data });
        this.setState({ playerStats: playerStats });
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
        <table className="playerDetail highlight bordered">
          <thead>
            <tr>
              <th>Season</th>
              <th>GP</th>
              <th>MP</th>
              <th>FG</th>
              <th>FGA</th>
              <th>FT</th>
              <th>FTA</th>
              <th>3P</th>
              <th>3PA</th>
              <th>ORB</th>
              <th>DRB</th>
              <th>AST</th>
              <th>STL</th>
              <th>BLK</th>
              <th>TOV</th>
              <th>PF</th>
              <th>PTS</th>
            </tr>
          </thead>
          <tbody>
            {this.state.playerStats}
          </tbody>
        </table>
      </div>
    );
  }
}
export default PlayerDetail;
