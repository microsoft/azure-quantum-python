// import * as React from "react";

// import { DetailsHeader, IDetailsColumnRenderTooltipProps, IDetailsHeaderProps } from "@fluentui/react/lib/DetailsList";
// import { FontWeights, getTheme, mergeStyleSets } from "@fluentui/react/lib/Styling";

// import { Text } from "@fluentui/react/lib/Text";
// import { TooltipHost } from "@fluentui/react/lib/Tooltip";
// import { Icon } from '@fluentui/react/lib/Icon';

// const styles = mergeStyleSets({
//     cellText: {
//         fontfamily: 'Segoe UI',
//         fontWeight: FontWeights.regular,
//         fontSize: "14px",
//         lineHeight: "18px"
//     },
//     tooltipHost: {
//         marginLeft: "8px",
//     },
//     infoIcon: {
//         width: "12px",
//         height: "12px",
//         display: "inline-block",
//         verticalAlign: "-0.1rem",
//         fill: getTheme().semanticColors.infoIcon,
//     },
// });

// export const ColumnHeaderWithTooltip = (tooltipHostProps: IDetailsColumnRenderTooltipProps): JSX.Element => {
//     return <>
//             <Text className={styles.cellText}>{tooltipHostProps.column.name}</Text>
//             {!tooltipHostProps.column.data?.tooltipContent
//                 ? <></>
//                 : <TooltipHost hostClassName={styles.tooltipHost} content={tooltipHostProps.column.data.tooltipContent}>
//                     <Icon iconName="InfoSolid" className={styles.infoIcon}/>
//                 </TooltipHost>
//             }
//         </>;
// };

// export const DetailsHeaderWithTooltip = (props: IDetailsHeaderProps): JSX.Element => {
//     return <DetailsHeader
//         onRenderColumnHeaderTooltip = {ColumnHeaderWithTooltip}
//         {...props}
//     />;
// };