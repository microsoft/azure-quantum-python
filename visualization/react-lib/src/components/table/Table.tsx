import * as React from "react";
import "./Table.css";
import {
  Table,
  HeaderRow,
  Body,
  Row,
  HeaderCell,
  Cell,
} from "@table-library/react-table-library/table";
import { useTheme } from "@table-library/react-table-library/theme";
import {
  DEFAULT_OPTIONS,
  getTheme,
} from "@table-library/react-table-library/material-ui";
import { Button, Tooltip } from "@mui/material";
import InfoIcon from "@mui/icons-material/Info";

export type TableData = {
  id: string;
  name: string;
  type: number;
  value?: string;
  description?: string;
};

export type TableComponentProps = {
  nodes: TableData[];
  width: number;
  height: number;
};

function TableComponent({ nodes, width, height }: TableComponentProps) {
  const data = { nodes };

  const customTheme = {
    HeaderCell: `font-family: 'Segoe UI';
    font-style: normal;
    font-weight: 600;
    font-size: 18px;
    line-height: 22px; 
    color: #201F1E;
    padding: 10px `,
    BaseCell: `
    padding: 0px 20px;
    
    font-family: 'Segoe UI';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 18px;

    &:last-of-type {
      text-align: right;
    }
  `,
    Table: `
 width: 700px;
`,
    Row: `&:nth-child(n){.td:nth-child(n){ border-bottom: none}} `,
  };
  const materialTheme = getTheme(DEFAULT_OPTIONS);
  const theme = useTheme([materialTheme, customTheme]);

  // TO DO: edit tooltip text so that font-size can be changed.

  return (
    <div style={{ width: width, height: height }}>
      <Table className="table-element" data={data} theme={theme}>
        {(tableList: any[]) => (
          <>
            <Body>
              {tableList.map((item) =>
                item.type === 0 ? (
                  <HeaderRow key={item.id} item={item}>
                    <HeaderCell> {item.name} </HeaderCell>
                    <HeaderCell> </HeaderCell>
                  </HeaderRow>
                ) : (
                  <Row key={item.id} item={item}>
                    <Cell>
                      {item.name}
                      <Tooltip
                        title={item.description ? item.description : null}
                      >
                        {item.description ? (
                          <Button>
                            <InfoIcon
                              data-show-if
                              fontSize="small"
                              style={{
                                fill: "#1a5d8c",
                              }}
                            ></InfoIcon>
                          </Button>
                        ) : (
                          <div></div>
                        )}
                      </Tooltip>
                    </Cell>
                    <Cell>{item.value.toLocaleString()}</Cell>
                  </Row>
                )
              )}
            </Body>
          </>
        )}
      </Table>
    </div>
  );
}

export default TableComponent;
