/*------------------------------------
  Copyright (c) Microsoft Corporation.
  Licensed under the MIT License.
  All rights reserved.
------------------------------------ */
import React from "react";
import { IColumn } from "@fluentui/react";
import { Icon } from "@fluentui/react/lib/Icon";
import { mergeStyleSets } from "@fluentui/react/lib/Styling";
import { TooltipHost, TooltipOverflowMode } from "@fluentui/react/lib/Tooltip";

import { IItem } from "./Table";

const classNames = mergeStyleSets({
  cellText: {
    overflow: "hidden",
    textOverflow: "ellipsis",
    color: "#343434",
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
    color: "#343434",
  },
});

export function GetColumns(): IColumn[] {
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
      minWidth: 190,
      flexGrow: 3,
    },
    {
      key: "value",
      name: "Value",
      onRender: (item: IItem) => {
        return (
          <div className={classNames.cellText} data-is-focusable={true}>
            <TooltipHost
              hostClassName={classNames.tooltipHost}
              content={item.value}
              overflowMode={TooltipOverflowMode.Parent}
            >
              {item.value}
            </TooltipHost>
          </div>
        );
      },
      minWidth: 80,
      flexGrow: 1,
    },
  ];
  return columns;
}
