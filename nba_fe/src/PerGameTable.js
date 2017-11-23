import React, { Component } from 'react';


var _ = require('lodash')

class PerGameTable extends Component {
  constructor() {
    super();
    this.createTableRows = this.createTableRows.bind(this);
    this.state = {
      playerStats: [],
    };
  }

  createTableRows() {
    let playerStats = this.props.stats.map((ps) => {
          return (
            <tr key={ps.url}>
              <td>{ps.season_year}</td>
              <td>{ps.gp}</td>
              <td>{ps.mp}</td>
              <td>{ps.fga? 
                    _.round(ps.fg / ps.fga, 3)
                    : "N/A"}</td>
              <td>{_.round(ps.fga / ps.gp, 1)}</td>
              <td>{ps.fta?
                    _.round(ps.ft / ps.fta, 3)
                    : "N/A"}</td>
              <td>{_.round(ps.fta / ps.gp, 1)}</td>
              <td>{ps.threes_attempted ? 
                    _.round(ps.three_pointers / ps.threes_attempted, 2)
                    : "N/A"}</td>
              <td>{_.round(ps.threes_attempted, 1)}</td>
              <td>{_.round(ps.orb / ps.gp, 1)}</td>
              <td>{_.round(ps.drb / ps.gp, 1)}</td>
              <td>{_.round((ps.orb + ps.drb) / ps.gp, 1)}</td>
              <td>{_.round(ps.ast / ps.gp, 1)}</td>
              <td>{_.round(ps.stl / ps.gp, 1)}</td>
              <td>{_.round(ps.blk / ps.gp, 1)}</td>
              <td>{_.round(ps.tov / ps.gp, 1)}</td>
              <td>{_.round(ps.pf / ps.gp, 1)}</td>
              <td>{_.round(ps.pts / ps.gp, 1)}</td>
            </tr>
          )
        })
        this.setState({ playerStats: playerStats });
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.props.stats !== prevProps.stats) {
        this.createTableRows();
    }
  }

  render() {
    return (
      <div className="tableContainer">
        <h2 className="tableTitle">Per Game Averages</h2>
        <table className="playerDetail highlight bordered">
          <thead>
            <tr>
              <th>Season</th>
              <th>GP</th>
              <th>MP</th>
              <th>FG%</th>
              <th>FGA</th>
              <th>FT%</th>
              <th>FTA</th>
              <th>3P%</th>
              <th>3PA</th>
              <th>ORB</th>
              <th>DRB</th>
              <th>TRB</th>
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
export default PerGameTable;
