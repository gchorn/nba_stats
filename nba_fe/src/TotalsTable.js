import React, { Component } from 'react';


class TotalsTable extends Component {
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
        <h2 className="tableTitle">Season Totals</h2>
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
export default TotalsTable;
