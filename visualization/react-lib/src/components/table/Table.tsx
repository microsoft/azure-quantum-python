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

export interface TableData {
  id: string;
  name: string;
  type: number;
  value?: number;
}

export interface TableComponentProps {
  nodes: TableData[];
  width: number;
  height: number;
}

function TableComponent({ nodes, width, height }: TableComponentProps) {
  const data = { nodes };

  const customTheme = {
    HeaderCell: `font-family: 'Segoe UI';
    font-style: normal;
    font-weight: 600;
    font-size: 16px;
    line-height: 21px; 
    color: #201F1E;
    padding: 10px `,
    BaseCell: `
    padding: 6px 20px;
    
    font-family: 'Segoe UI';
    font-style: normal;
    font-weight: 400;
    font-size: 13px;
    line-height: 17px;

    &:last-of-type {
      text-align: right;
    }
  `,
    Row: `&:nth-child(n){.td:nth-child(n){ border-bottom: none}} `,
  };
  const materialTheme = getTheme(DEFAULT_OPTIONS);
  const theme = useTheme([materialTheme, customTheme]);

  return (
    <div style={{ width: width, height: height }}>
      <Table data={data} theme={theme}>
        {(tableList) => (
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
                      <Tooltip title={item.name}>
                        <Button>
                          <InfoIcon fontSize="small"></InfoIcon>
                        </Button>
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
