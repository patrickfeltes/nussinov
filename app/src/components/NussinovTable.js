import React, { Component } from 'react';

class NussinovTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            dp_table: [
                [0, 0, 0, 0, 0, 0, 1, 2, 3],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1,
                    2,
                    3
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1,
                    2,
                    2
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1,
                    1,
                    1
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1,
                    1,
                    1
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1,
                    1,
                    1
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ]
            ]
        };
    }

    renderTableData() {
        return this.state.dp_table.map((row, i) => {
           var entry = row.map((element, j) => {
                return (
                    <td key={j}>{element}</td>
                );
           });
           return (
              <tr key={i}>
                  {entry}   
              </tr>
           );
        });
    }
  
    render() {
        return (
            <div>
                <table id='nussinov'>
                    <tbody>
                        {this.renderTableData()}
                    </tbody>
                </table>
            </div>
        );
    }
}

export default NussinovTable;