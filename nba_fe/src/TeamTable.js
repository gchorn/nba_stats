import React, { Component } from 'react';
import {ProgressBar} from 'react-materialize'
import './TeamTable.css';


class TeamTable extends Component {
  constructor() {
    super();
    this.state = {
      teams: [],
      loading: 'ProgressBar-hidden',
    };
  }

  fetchTeams() {
    this.setState({ loading: null });

    let fetchUrl = 'http://localhost/teams?format=json'

    fetch(fetchUrl)
      .then(results => {
        return results.json();
      }).then(data => {
        let teams = data.results.map((tm) => {
          return (
            <tr className="teamRow" key={tm.id} onClick={() => this.props.onTeamSelect(tm.id, tm.name)}>
              <td>{tm.name}</td>
              <td>{tm.short_name}</td>
              <td>{tm.city}</td>
              <td>{tm.division.name}</td>
              <td>{tm.wins}</td>
              <td>{tm.losses}</td>
            </tr>
          )
        })
        this.setState({ teams: teams });
        this.setState({ loading: 'ProgressBar-hidden' });
      })
  }

  componentWillMount() {
    this.fetchTeams();
  }

  render() {
    return (
      <div className="tableContainer">
        <h1 className="pageTitle">NBA Teams</h1>
        <ProgressBar className={this.state.loading}/>
        <table className="teamTable highlight bordered">
          <thead>
            <tr>
              <th>Name</th>
              <th>Short Name</th>
              <th>City</th>
              <th>Division</th>
              <th>Wins</th>
              <th>Losses</th>
            </tr>
          </thead>
          <tbody>
            {this.state.teams}
          </tbody>
        </table>
      </div>
    );
  }
}
export default TeamTable;
