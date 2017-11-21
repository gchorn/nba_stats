import React, { Component } from 'react';
import {Col, Pagination, ProgressBar, Row} from 'react-materialize'
import './PlayerTable.css';

var _ = require('lodash')

class PlayerTable extends Component {
  constructor() {
    super();
    this.changePage = this.changePage.bind(this);
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
    if (this.props.searchValue) {
      fetchUrl = 'http://localhost/players/search?format=json&name=' + this.props.searchValue
    } else if (this.props.teamId) {
      fetchUrl = 'http://localhost/players/search?format=json&teamId=' + this.props.teamId
    }

    fetch(fetchUrl)
      .then(results => {
        return results.json();
      }).then(data => {
        let players = data.results.map((pl) => {
          return (
            <tr className="playerRow" key={pl.id} onClick={() => this.props.onPlayerSelect(pl.id)}>
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
        let pageNum = _.ceil(data.count/data.results.length);

        if (this.state.pages !== pageNum) {
          this.setState({ pages: pageNum });
          if (pageNum <= 1) {
            this.setState({ pagination: 'Pagination-hidden' });
          } else {
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

  componentWillMount() {
    this.fetchPlayers();
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.state.page !== prevState.page || this.props.searchValue !== prevProps.searchValue || this.props.teamId !== prevProps.teamId) {
      this.fetchPlayers();
    }
  }

  render() {
    return (
      <div className="tableContainer">
        <Row>
          <Col s={7}><h1 className="pageTitle">{this.props.tableTitle}</h1></Col>
          <Col s={5}
            ><Pagination className={"tablePaginator " + this.state.pagination} items={this.state.pages} activePage={this.state.page} maxButtons={8} onSelect={this.changePage} />
          </Col>
        </Row>
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
