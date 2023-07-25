/*------------------------------------
  Copyright (c) Microsoft Corporation.
  Licensed under the MIT License.
  All rights reserved.
------------------------------------ */
import React from "react";
import { create } from "react-test-renderer";
import { IColumn, IGroup, ThemeProvider } from "@fluentui/react";
import { Icon } from "@fluentui/react/lib/Icon";
import {
  getTheme,
  mergeStyleSets,
  setIconOptions,
} from "@fluentui/react/lib/Styling";
import { TooltipHost } from "@fluentui/react/lib/Tooltip";

import { IItem, IState, TableComponent } from "../Table";
// Suppress icon warnings.
setIconOptions({
  disableWarnings: true,
});

const classNames = mergeStyleSets({
  cellText: {
    overflow: "hidden",
    textOverflow: "ellipsis",
  },
  tooltipHost: {
    marginLeft: "8px",
    cursor: "default",
  },
  infoIcon: {
    width: "12px",
    height: "12px",
    display: "inline-block",
    verticalAlign: "-0.1rem",
    fill: getTheme().semanticColors.infoIcon,
  },
});

describe("Table tests", () => {
  it("Verify Table", () => {
    const tableItems: IItem[] = [
      {
        name: "Total physical qubits",
        value: "12",
        description:
          "Total physical qubits required for algorithm and T factories.",
      },
      {
        name: "Physical T factory qubits",
        value: "20",
        description: "Number of physical qubits for the T factories.",
      },
      {
        name: "Number of T factory copies",
        value: "100",
        description:
          "Number of T factories capable of producing the demanded T states during the algorithm's runtime.",
      },
      {
        name: "Physical qubits for single T factory",
        value: "2",
        description: "",
      },
    ];

    const tableGroups: IGroup[] = [
      {
        key: "1",
        name: "Group 1",
        startIndex: 0,
        count: 1,
      },
      {
        key: "2",
        name: "Group 2",
        startIndex: 1,
        count: 2,
      },
      {
        key: "3",
        name: "Group 3",
        startIndex: 3,
        count: 1,
      },
    ];

    const tableProps: IState = {
      items: tableItems,
      groups: tableGroups,
      showItemIndexInView: false,
      isCompactMode: false,
    };

    const columns: IColumn[] = [
      {
        key: "name",
        name: "Name",
        onRender: (item: IItem) => {
          return (
            <div className={classNames.cellText} data-is-focusable={true}>
              {item.name}
              {item.description ? (
                <TooltipHost
                  hostClassName={classNames.tooltipHost}
                  content={item.description}
                >
                  <Icon iconName="Info" className={classNames.infoIcon} />
                </TooltipHost>
              ) : (
                <></>
              )}
            </div>
          );
        },
        minWidth: 220,
        flexGrow: 3,
      },
      {
        key: "value",
        name: "Value",
        onRender: (item: IItem) => {
          return (
            <div className={classNames.cellText} data-is-focusable={true}>
              {item.value}
            </div>
          );
        },
        minWidth: 50,
        flexGrow: 1,
      },
    ];

    const component = create(
      <ThemeProvider>
        <TableComponent state={tableProps} columns={columns} />
      </ThemeProvider>,
    );

    expect(component.toJSON()).toMatchSnapshot("Table");
  });
});
