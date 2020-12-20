import React, { Component } from 'react';

const styles = {
    tableStyle: {
        marginTop: "3vh",
        marginLeft: "3vw"
    }
}

class NussinovTable extends Component {
    constructor(props) {
        super(props);

        var traceback = this.props.traceback;
        var _row_col_dict = {};

        if (traceback != null) {
            for (var i = 0; i < traceback.length; i++) {
                var row_col_list = traceback[i];
                if (row_col_list[0] in _row_col_dict) {
                    _row_col_dict[row_col_list[0]].push(row_col_list[1]);
                } else {
                    _row_col_dict[row_col_list[0]] = [row_col_list[1]];
                }
            }
        }

        this.state = {
            dp_table: this.props.dp_table_prop,
            row_col_dict: _row_col_dict,
            sequence: this.props.sequence
        };
    }

    renderSequenceRow() {
        if (this.state.sequence == null) {
            return null;
        }
        var cells = this.state.sequence.split('').map((c, i) => {
            return (<td className='sequenceCell'>{c}</td>);
        });
        return (
            <tr>
                <td></td>
                {cells}
                <td></td>
            </tr>
        );
    }

    renderTableData() {
        if (this.state.dp_table == null) {
            return null;
        }
        return this.state.dp_table.map((row, i) => {
           var entry = row.map((element, j) => {
                return (
                    <td className={i in this.state.row_col_dict && this.state.row_col_dict[i].includes(j) ? 'highlightedCell' : ''} key={j}>{element}</td>
                );
           });
           return (
              <tr key={i}>
                  <td className='sequenceCell'>{this.state.sequence[i]}</td>
                  {entry}
                  <td className='sequenceCell'>{this.state.sequence[i]}</td>   
              </tr>
           );
        });
    }
  
    render() {
        return (
            <div>
                <table style={styles.tableStyle} id='nussinov'>
                    <tbody>
                        {this.renderSequenceRow()}
                        {this.renderTableData()}
                    </tbody>
                </table>
            </div>
        );
    }
}

export default NussinovTable;