import React from 'react';

/**
 * A table of NBA Players
 */
class PlayerTable extends React.Component {
    constructor() {
        super();
        this.state = {
            players: [],
        };
    }

    componentWillMount() {
        fetch('http://localhost/players?format=json')
        .then(results => {
            return results.json();
        }).then(data => {
            let players = data.results.map((pl) => {
                return(
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
            this.setState({ players: players });
            console.log("state", this.state.players);
        })
    }

    render() {
        return (
            <div className="tableContainer">
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
