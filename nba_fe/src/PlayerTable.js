import React, { Component } from 'react';
import {Col, Input, Pagination, ProgressBar, Row} from 'react-materialize'
import './PlayerTable.css';

var _ = require('lodash')
var pageSize = 100;

class PlayerTable extends Component {
  constructor() {
    super();
    this.changePage = this.changePage.bind(this);
    this.playerSearchUpdate = this.playerSearchUpdate.bind(this);
    this.playerSearchInputChanged = this.playerSearchInputChanged.bind(this);
    this.state = {
      players: [],
      pages: 0,
      page: 1,
      loading: 'ProgressBar-hidden',
      pagination: 'Pagination-hidden',
      searchValue: null
    };
  }

  fetchPlayers() {
    this.setState({ loading: null });

    let fetchUrl = 'http://localhost/players?format=json&page=' + this.state.page
    if (this.state.searchValue) {
      fetchUrl = 'http://localhost/players/search?format=json&name=' + this.state.searchValue
    }

    fetch(fetchUrl)
      .then(results => {
        return results.json();
      }).then(data => {
        let players = data.results.map((pl) => {
          return (
            <tr key={pl.id}>
              <td>{pl.first_name}</td>
              <td>{pl.last_name}</td>
              <td>{pl.age}</td>
              <td>{pl.pos}</td>
              <td>{pl.current_team.name}</td>
              <td>{pl.height_feet}'{pl.height_inches}"</td>
              <td>{pl.weight} lbs</td>
              <td>{pl.years_pro}</td>
            </tr>
          )
        })
        let pageNum = _.ceil(data.count/pageSize);
        if (this.state.pages !== pageNum) {
          this.setState({ pages: pageNum });
          if (pageNum === 0) {
            console.log('hiding pagination!')
            this.setState({ pagination: 'Pagination-hidden' });
          } else {
            console.log('showing pagination!')
            this.setState({ pagination: null });
          }
        }
        this.setState({ players: players });
        this.setState({ loading: 'ProgressBar-hidden' });
      })
  }

  changePage(pageNumber) {
    this.setState({ page: pageNumber });
  }

  playerSearchInputChanged(event, value) {
    this.handleSearchDebounced(value);
  }

  playerSearchUpdate(value) {
    this.setState({ searchValue: value });
  }

  componentWillMount() {
    this.handleSearchDebounced = _.debounce(this.playerSearchUpdate, 350);
    this.fetchPlayers();
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.state.page !== prevState.page || this.state.searchValue !== prevState.searchValue) {
      this.fetchPlayers();
    }
  }

  render() {
    return (
      <div className="tableContainer">
        <Row>
          <Col s={7}><h1 className="pageTitle">NBA Players</h1></Col>
          <Input placeholder="Search players by name" s={5} onChange={this.playerSearchInputChanged}/>
        </Row>
        <Pagination className={"tablePaginator "+ this.state.pagination} items={this.state.pages} activePage={this.state.page} maxButtons={8} onSelect={this.changePage}/>
        <ProgressBar className={this.state.loading}/>
        <table className="playerTable highlight bordered">
          <thead>
            <tr>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Age</th>
              <th>Position</th>
              <th>Team</th>
              <th>Height</th>
              <th>Weight</th>
              <th>Years Pro</th>
            </tr>
          </thead>
          <tbody>
            {this.state.players}
          </tbody>
        </table>
      </div>
    );
  }
}
export default PlayerTable;
