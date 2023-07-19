import * as React from "react";
import {
  DetailsList,
  IColumn,
  IDetailsList,
  IGroup,
  IDetailsGroupRenderProps,
  SelectionMode
} from "@fluentui/react";
import { getTheme, mergeStyleSets } from "@fluentui/react/lib/Styling";

const ROW_HEIGHT: number = 42; // from DEFAULT_ROW_HEIGHTS in DetailsRow.styles.ts
const GROUP_HEADER_AND_FOOTER_SPACING: number = 8;
const GROUP_HEADER_AND_FOOTER_BORDER_WIDTH: number = 1;
const GROUP_HEADER_HEIGHT: number = 95;
const GROUP_FOOTER_HEIGHT: number =
  GROUP_HEADER_AND_FOOTER_SPACING * 4 +
  GROUP_HEADER_AND_FOOTER_BORDER_WIDTH * 2;

const theme = getTheme();

const classNames = mergeStyleSets({
  headerAndFooter: {
    borderTop: `${GROUP_HEADER_AND_FOOTER_BORDER_WIDTH}px solid ${theme.palette.neutralQuaternary}`,
    borderBottom: `${GROUP_HEADER_AND_FOOTER_BORDER_WIDTH}px solid ${theme.palette.neutralQuaternary}`,
    padding: GROUP_HEADER_AND_FOOTER_SPACING,
    margin: `${GROUP_HEADER_AND_FOOTER_SPACING}px 0`,
    background: theme.palette.neutralLighterAlt,
    // Overlay the sizer bars
    position: "relative",
    zIndex: 100,
  },
  headerTitle: [
    theme.fonts.large,
    {
      padding: "4px 0",
    },
  ],
});

export interface IItem {
  name: string;
  value: string;
  description: string;
}

export interface IState {
  items: IItem[];
  groups: IGroup[];
  showItemIndexInView: boolean;
  isCompactMode: boolean;
}

export class TableComponent extends React.Component<{ state: IState, columns: IColumn[] }, IState> {
  private _root = React.createRef<IDetailsList>();
  private _columns: IColumn[];

  constructor(props: { state: IState, columns: IColumn[] }) {
    super(props);

    this.state = props.state;
    this._columns = props.columns;
  }

  public componentWillUnmount() {
    if (this.state.showItemIndexInView) {
      const itemIndexInView = this._root.current!.getStartItemIndexInView();
      alert("first item index that was in view: " + itemIndexInView);
    }
  }

  public render() {
    const { items, groups } = this.state;

    return (
      <div>
        <DetailsList
          componentRef={this._root}
          items={items}
          groups={groups}
          columns={this._columns}
          groupProps={{
            onRenderHeader: this._onRenderGroupHeader,
            showEmptyGroups: false,
          }}
          compact={true}
          indentWidth={4}
          getGroupHeight={this._getGroupHeight}
          selectionMode={SelectionMode.none}
          isHeaderVisible={false}
        />
      </div>
    );
  }

  private _onRenderGroupHeader: IDetailsGroupRenderProps["onRenderHeader"] = (
    props
  ) => {
    if (props) {
      return (
        <div className={classNames.headerAndFooter}>
          <div className={classNames.headerTitle}>{`${props.group!.name}`}</div>
        </div>
      );
    }

    return null;
  };

  private _getGroupTotalRowHeight = (group: IGroup): number => {
    return group.isCollapsed ? 0 : ROW_HEIGHT * group.count;
  };

  private _getGroupHeight = (group: IGroup, _groupIndex: number): number => {
    return (
      GROUP_HEADER_HEIGHT +
      GROUP_FOOTER_HEIGHT +
      this._getGroupTotalRowHeight(group)
    );
  };
}
