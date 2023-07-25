/*------------------------------------
  Copyright (c) Microsoft Corporation.
  Licensed under the MIT License.
  All rights reserved.
------------------------------------ */
export interface JobResults {
  errorBudget: ErrorBudget;
  jobParams: JobParams;
  logicalCounts: LogicalCounts;
  logicalQubit: LogicalQubit;
  physicalCounts: PhysicalCounts;
  physicalCountsFormatted: { [key: string]: string };
  reportData: ReportData;
  status: string;
  tfactory: Tfactory;
}

export interface ErrorBudget {
  logical: number;
  rotations: number;
  tstates: number;
}

export interface JobParams {
  errorBudget: number;
  qecScheme: QecScheme;
  qubitParams: QubitParams;
}

export interface QecScheme {
  crossingPrefactor: number;
  errorCorrectionThreshold: number;
  logicalCycleTime: string;
  name: string;
  physicalQubitsPerLogicalQubit: string;
}

export interface QubitParams {
  instructionSet: string;
  name: string;
  oneQubitGateErrorRate: number;
  oneQubitGateTime: string;
  oneQubitMeasurementErrorRate: number;
  oneQubitMeasurementTime: string;
  tGateErrorRate: number;
  tGateTime: string;
  twoQubitGateErrorRate: number;
  twoQubitGateTime: string;
}

export interface LogicalCounts {
  ccixCount: number;
  cczCount: number;
  measurementCount: number;
  numQubits: number;
  rotationCount: number;
  rotationDepth: number;
  tCount: number;
}

export interface LogicalQubit {
  codeDistance: number;
  logicalCycleTime: number;
  logicalErrorRate: number;
  physicalQubits: number;
}

export interface PhysicalCounts {
  breakdown: { [key: string]: number };
  physicalQubits: number;
  runtime: number;
}

export interface ReportData {
  assumptions: string[];
  groups: Group[];
}

export interface Group {
  alwaysVisible: boolean;
  entries: Entry[];
  title: string;
}

export interface Entry {
  description: string;
  explanation: string;
  label: string;
  path: string;
}

export interface Tfactory {
  codeDistancePerRound: number[];
  logicalErrorRate: number;
  numInputTstates: number;
  numRounds: number;
  numTstates: number;
  numUnitsPerRound: number[];
  physicalQubits: number;
  physicalQubitsPerRound: number[];
  runtime: number;
  runtimePerRound: number[];
  unitNamePerRound: string[];
}
