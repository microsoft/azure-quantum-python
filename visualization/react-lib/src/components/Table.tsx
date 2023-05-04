import React from "react";

interface Props {
  rowGroups: RowGroup[];
}

export interface RowGroup {
  header: string;
  rows: Row[];
}

export interface Row {
  data: string[][];
}

const Table: React.FC<Props> = ({ rowGroups }) => {
  return (
    <table>
      {rowGroups.map((rowGroup, groupIndex) => (
        <tbody key={groupIndex}>
          <tr>
            <th style={{ textAlign: "left" }}>{rowGroup.header}</th>
          </tr>
          {rowGroup.rows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.data.map((cell, cellIndex) => (
                <>
                  <td
                    key={`${rowIndex}-${cellIndex}`}
                    style={{ paddingLeft: "10px" }}
                  >
                    {cell[0]}:
                  </td>
                  <td
                    key={`${rowIndex}-${cellIndex + 1}`}
                    style={{ paddingLeft: "10px" }}
                  >
                    <span style={{ fontWeight: "bold", textAlign: "right" }}>
                      {cell[1]}
                    </span>
                  </td>
                </>
              ))}
            </tr>
          ))}
        </tbody>
      ))}
    </table>
  );
};

export default Table;
